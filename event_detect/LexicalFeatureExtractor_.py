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
        men_str1 = em1.get_mention()
        men_str2 = em2.get_mention()

        sign = 0

        if sign == 0:
            synsets1 = wn.synsets(men_str1, pos=wn.VERB)
	    synsets2 = wn.synsets(men_str2, pos=wn.VERB)
            features['mention_HW'] = self.get_similarity(synsets1, synsets2)
        else:
            if cmp(men_str1, men_str2) == 0:
                features['mention_HW'] = 1
            else:
                features['mention_HW'] = 0

        # HL feature extraction
        lemma_tool = WordNetLemmatizer()
        str1 = lemma_tool.lemmatize(em1.get_mention(), 'v')
        str2 = lemma_tool.lemmatize(em2.get_mention(), 'v')

        if sign == 0:
            synsets1 = wn.synsets(men_str1, pos=wn.VERB)
	    synsets2 = wn.synsets(men_str2, pos=wn.VERB)
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

        return features

    def __str__(self):
        print '%d Features: mention_no' % self._feature_no
