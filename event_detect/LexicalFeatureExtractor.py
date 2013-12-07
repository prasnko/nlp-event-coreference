import extract
from nltk.corpus import PlaintextCorpusReader
import nltk
import re
import os
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic

class FeatureExtractorBase():
    '''
    This is the base class of feature extractors
    You need to implement your own feature extractors,
    e.g. Class Features (CF), WordNet Features (WF)
    Semantic Features (SF).
    '''
    def __init__(self):
        pass

    def extract(self, em1, em2):
        pass

    def __str__(self):
        pass

class LexicalFeatureExtractor(FeatureExtractorBase):
    def __init__(self):
        self._feature_no = 4

    def get_similarity(self, synsets1, synsets2):
        brown_ic = wordnet_ic.ic('ic-brown.dat')
        max_value = 0
        for synset1 in synsets1:
            for synset2 in synsets2:
                value = wn.res_similarity(synset1, synset2, brown_ic)
                if value > max_value:
                    max_value = value
	return max_value

    def extract(self, em1, em2):

        # ... NOT IMPLEMENTED YET...
        features = {}

        # HW feature extraction
##        hw1 = em1.get_mention()
##        hw2 = em2.get_mention()

        men_sent1 = em1.get_sent().get_string()
        men_sent2 = em2.get_sent().get_string()

        hw1 = str(extract.head(men_sent1,"C:\Prasanna\Fall12\NLP\Project\stanford-parser-2012-11-12","stanford-parser.jar"))
        hw2 = str(extract.head(men_sent2,"C:\Prasanna\Fall12\NLP\Project\stanford-parser-2012-11-12","stanford-parser.jar"))
        sign = 0

        if sign == 0:
            synsets1 = wn.synsets(hw1,pos=wn.VERB)[0:4]
            synsets2 = wn.synsets(hw2,pos=wn.VERB)[0:4]
            features['mention_HW'] = self.get_similarity(synsets1, synsets2)
        else:
            if cmp(hw1, hw2) == 0:
                features['mention_HW'] = 1
            else:
                features['mention_HW'] = 0

        # HL feature extraction
        lemma_tool = WordNetLemmatizer()
        str1 = lemma_tool.lemmatize(em1.get_mention())
        str2 = lemma_tool.lemmatize(em2.get_mention())

        if sign == 0:
            synsets1 = wn.synsets(str1, pos=wn.VERB)
            synsets2 = wn.synsets(str2, pos=wn.VERB)
            features['mention_HL'] = self.get_similarity(synsets1, synsets2)
            #print str1
        else:
            if cmp(str1, str2) == 0 :
                features['mention_HL'] = 1
            else:
                features['mention_HL'] = 0

        # LHL and RHL features extraction
        word_list_1 = re.split(" ", em1.get_sent().remove_anno())
        word_list_2 = re.split(" ", em2.get_sent().remove_anno())

	i = 0
	index1 = 0
        for a in word_list_1:
	    i = i + 1
            if cmp(a, em1.get_mention()) == 0:
		index1 = i - 1
		break

	j = 0
	index2 = 0
        for a in word_list_2:
	    j = j + 1
            if cmp(a, em2.get_mention()) == 0:
		index2 = j - 1
		break

        lemma_1_left = lemma_tool.lemmatize(word_list_1[index1-1], 'v')
        lemma_1_right = lemma_tool.lemmatize(word_list_1[index1+1], 'v')
        lemma_2_left = lemma_tool.lemmatize(word_list_2[index2-1], 'v')
        lemma_2_right = lemma_tool.lemmatize(word_list_2[index2+1], 'v')

        if sign == 0:
            synsets1 = wn.synsets(lemma_1_left, pos=wn.VERB)
	    synsets2 = wn.synsets(lemma_2_left, pos=wn.VERB)
            features['mention_LHL'] = self.get_similarity(synsets1, synsets2)
        else:
            if cmp(lemma_1_left, lemma_2_left) == 0:
                features['mention_LHL'] = 1
            else:
                features['mention_LHL'] = 0

        if sign == 0:
            synsets1 = wn.synsets(lemma_1_right, pos=wn.VERB)
	    synsets2 = wn.synsets(lemma_2_right, pos=wn.VERB)
            features['mention_RHL'] = self.get_similarity(synsets1, synsets2)
        else:
            if cmp(lemma_1_right, lemma_2_right) == 0:
                features['mention_RHL'] = 1
            else:
                features['mention_RHL'] = 0

        # LHL and RHL features extraction
        mention_num1 = len(em1.get_sent().get_all_mentions())
        mention_num2 = len(em2.get_sent().get_all_mentions())
	mention_list1 =  em1.get_sent().get_all_mentions()
	mention_list2 =  em2.get_sent().get_all_mentions()



     # Part of Speech features extraction

    a = em1.get_sent().remove_anno()
    text1 = nltk.word_tokenize(a)
    pos_list1 = nltk.pos_tag(text1)
    pos_em1 = ''

    for pos in pos_list1:
           if cmp(pos[0], men_str1) == 0:
               pos_em1 = pos[1]

    b = em2.get_sent().remove_anno()
    text2 = nltk.word_tokenize(a)
    pos_list2 = nltk.pos_tag(text2)
    pos_em2 = ''

    for pos in pos_list2:
           if cmp(pos[0], men_str2) == 0:
               pos_em2 = pos[1]

    if cmp (pos_em1, pos_em2) == 0:
           features['partofspeech'] = 1
    else:
           features['partofspeech'] = 0


    #Word Class feature extraction...

    if (re.match('N', pos_em1) or (cmp(pos_em1, 'PRP') == 0)):
	    wc_1 = 'NOUN'
    elif re.match('V', pos_em1):
	    wc_1 = 'VERB'
    elif re.match('J', pos_em1):
	    wc_1 = 'ADJECTIVE'
    else:
	    wc_1 = 'OTHER'

    if (re.match('N', pos_em2) or (cmp(pos_em2, 'PRP') == 0)):
	    wc_2 = 'NOUN'
    elif re.match('V', pos_em2):
	    wc_2 = 'VERB'
    elif re.match('J', pos_em2):
	    wc_2 = 'ADJECTIVE'
    else:
	    wc_2 = 'OTHER'

    if cmp (wc_1, wc_2) == 0:
	    features['wordclass'] = 1
    else:
	    features['wordclass'] = 0
    return features

    def __str__(self):
        print '%d Features: mention_no' % self._feature_no
