'''
Created on Nov 1, 2012

@author: jasonleakey
'''

from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import wordnet as wn
import nltk
import re
import os
from propbankfeature.propbank import PropbankFeatureExtractor
#import LexicalFeatureExtractor
import framenet
import WordnetFeatureExtractor
import CosineSimmilarityFeatureExtractor
# #from svmutil import svm_train, svm_predict

class EMention():
    def __init__(self, parent_sent, mention = [], id = []):
        # mention word
        self._mention = mention
        # mention id
        self._id = id
        # the sentence that the event mention belongs to
        self._parent_sent = parent_sent

    def __str__(self):
        # print the mention word
        return self._mention

    def set_mention(self, mention):
        self._mention = mention

    def get_mention(self):
        return self._mention

    def set_id(self, id):
        self._id = id

    def get_id(self, id):
        return self._id

    def get_sent(self):
        # return the Sentence object
        return self._parent_sent

    def isCoref(self, other):
        '''
        if two event mentions are co-refering, return true
        otherwise return false
        '''
        return self._id == other._id

class Sentence():
    def __init__(self, str):
        self.load(str)

    def __str__(self):
        return self._str

    def get_string(self):
        return self._str

    def load(self, str):
        self._str = str
        # event mention list of this sentence
        self._em_list = []

        # analyse
        self._analyze_sent()

    def remove_anno(self):
        '''
        remove annotations in the sentence
        '''
        return re.sub('(<MENTION CHAIN=\"\d+\">)|(</MENTION>)', '', self._str)

    def _analyze_sent(self):
        # mention words
        for m in re.finditer("<MENTION CHAIN=\"(?P<id>\d+)\">(?P<em>.*?)</MENTION>", self._str):
            self._em_list.append(EMention(self, m.group('em'), m.group('id')))

    def get_all_mentions(self):
        '''
        return the event mention list.
        '''
        return self._em_list

    def get_emention(self, idx):
        '''
        Event Mention Chain # List
        '''
        return self._em_list[idx]

    def hasEM(self):
        '''
        if a sentence includes an event mention, return true
        otherwise return false
        '''
        return len(self._em_list) > 0

    def whereis(self):
        '''
        @return: a tuple (topic, doc, sent) indexing the number
        '''
        return self._loc

    def set_loc(self, loc):
        '''
        set the location of sentence, format: (topic, doc, sent)
        '''
        self._loc = loc

class DataUtil():
    def __init__(self):
        # path to dataset
        self._path = '../res/data'

    def load_data(self):
        # folders
        dataset = []
        for topic in sorted(os.listdir(self._path)):
            docs = []
            dirname = self._path + os.sep + topic
            for filename in sorted(os.listdir(dirname)):
                sents = []
#                wordlists = PlaintextCorpusReader(dirname, filename)
                file = open(dirname + os.sep + filename)
#                file = wordlists.raw()
                line_no = 1
                for line in file:
                    if line != '\n' and line != '':
                        sent = Sentence(line)
                        sent.set_loc(tuple([int(topic), int(filename.split('.')[0]), line_no]))
                        sents.append(sent)
                        line_no += 1
                docs.append(sents)

                file.close()
            dataset.append(docs)
        return dataset

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

class SampleFeatureExtractor(FeatureExtractorBase):
    def __init__(self):
        self._feature_no = 2

    def extract(self, em1, em2):
        '''
        sample feature extractor
        @param em1: Event mention 1
        @param em2: Event mention 2
        @return: Dictionary format features. key: feature name; value: feature value
        '''
        features = {}
        features['mention_no'] = 1
        # here is another feature.
#        features['sentence_len'] = 1
        # return features as a dictionary
        return features

    def __str__(self):
        '''
        Some information for your feature extractor
        '''
        return '%d Features: mention_no, sentence_len' % self._feature_no

class MainEngine():
    def __init__(self, ft_extors = []):
        self._ft_extors = ft_extors
        self._within_doc_feature_table = []
        self._cross_doc_feature_table = []

    def set_feature_extractors(self, ft_extors):
        self._ft_extors = ft_extors

    def run_within_doc(self):
        '''
        within document classification
        '''
        # load 1:43 topics as training data
        datautil = DataUtil()
        data = datautil.load_data()

        # these x and y lists, feature table and class vector, are intended for
        # the use of SVM
        x = []
        y = []
        # feature table, including features paramand classes.
        # [({x1: val,  x2: val,  x3: val},  1),
        #  ({x1: val2, x2: val2, x3: val2}, 0),
        #  ({x1: val3, x2: val3, x3: val3}, 0),
        #  ...
        #  ({x1: valn, x2: valn, x3: valn}, 1)]
        featuresets = []
        # for each folder
        for t in range(len(data)):
            # for each filemode
            for d in range(len(data[t])):
                # the number of sentences in this file
                no_of_sents = len(data[t][d])
                # sentence Si
                for sent_i in range(0, no_of_sents):
                    if data[t][d][sent_i].hasEM():
                        # sentence Sj
                        for sent_j in range(sent_i, no_of_sents):
                            # make a sentence pair only if both of thshell script grep multiple than one stringsem have event mentions
                            if data[t][d][sent_j].hasEM():
                                ################################
    #                            print data[t][d][sent_i], '|', data[t][d][sent_j]
                                ################################
                                for em1 in data[t][d][sent_i].get_all_mentions():
                                    for em2 in data[t][d][sent_j].get_all_mentions():
                                        feature = {}
                                        # since there are many feature extractors
                                        # we should iterate each feature extractor
                                        # and combine the features
                                        for ft in self._ft_extors:
                                            feature.update(ft.extract(em1, em2))
                                        x.append(feature)

                                        clazz = em1.isCoref(em2)
                                        y.append(clazz)
                                        featuresets.append((feature, clazz))

        self._within_doc_feature_table = featuresets

        # run cross validation
        self.cross_validation(featuresets)
    #    m = svm_train(y[:44], x[:44], '-c 4')
    #    p_label, p_acc, p_val = svm_predict(y[44:], x[44:], m)
    #    print p_label, p_acc, p_val

    def run_cross_doc(self):
        '''
        cross document classification
        '''
        # load 1:43 topics as training data
        datautil = DataUtil()
        data = datautil.load_data()

        # these x and y lists, feature table and class vector, are intended for
        # the use of SVM
        x = []
        y = []
        # feature table, including features and classes.
        # [({x1: val,  x2: val,  x3: val},  1),
        #  ({x1: val2, x2: val2, x3: val2}, 0),
        #  ({x1: val3, x2: val3, x3: val3}, 0),
        #  ...
        #  ({x1: valn, x2: valn, x3: valn}, 1)]
        featuresets = []
        # for each folder
        for t in range(len(data)):
            bigdoc = []
            # ## union the file into a big doc
            # for each file
            for d in range(len(data[t])):
                # for each sentence
                for s in range(len(data[t][d])):
                    # add
                    bigdoc.append(data[t][d][s])
            # the number of sentences in the big doc
            no_of_sents = len(bigdoc)
            # sentence Si
            for sent_i in range(0, no_of_sents):
                if bigdoc[sent_i].hasEM():
                    # sentence Sj
                    for sent_j in range(sent_i, no_of_sents):
                        # make a sentence pair only if both of them have event mentions
                        if bigdoc[sent_j].hasEM():
                            ################################
    #                            print data[t][d][sent_i], '|', data[t][d][sent_j]
                            ################################
                            for em1 in bigdoc[sent_i].get_all_mentions():
                                for em2 in bigdoc[sent_j].get_all_mentions():
                                    feature = {}
                                    # since there are many feature extractors
                                    # we should iterate each feature extractor
                                    # and combine the features
                                    for ft in self._ft_extors:
                                        feature.update(ft.extract(em1, em2))
                                    x.append(feature)

                                    clazz = em1.isCoref(em2)
                                    y.append(clazz)
                                    featuresets.append((feature, clazz))
        self.create_svm_file(featuresets)

        self._cross_doc_feature_table = featuresets
        # run cross validation
        #self.cross_validation(featuresets)
    #    m = svm_train(y[:44], x[:44], '-c 4')
    #    p_label, p_acc, p_val = svm_predict(y[44:], x[44:], m)
    #    print p_label, p_acc, p_val

    def create_svm_file(self,data):
##        folder_content = []
##        input_files = []
##        folder_content = os.listdir(self._path)
##        for content in folder_content:
##            if content.endswith(".txt"):
##                input_files.append(content)
##        svmFile = open(input_files[0],"w")
##        visualFile = open(input_files[1],"w")
        svm_file = open(r"C:\Prasanna\EventCoreference\nlp-event-coreference\res\svmEvent.txt","w")
        visual_file =  open(r"C:\Prasanna\EventCoreference\nlp-event-coreference\res\svmVisual.txt","w")
        feature=[]
        for i in range(len(data)-1):
         featVector = ""
         featVectorVisual = ""
         feature = data[i]
         clazz= str(int(feature[1]))
         featDict = dict(feature[0])
         featValues =[]
         featValues = featDict.values()
         for j in range(1,len(featValues)+1):
          if featValues[j-1] != 0:
           featVector = featVector+" "+str(j)+":"+str(featValues[j-1])
          featVectorVisual = featVectorVisual+" "+str(featValues[j-1])
          if j==len(featValues):
            featVector = featVector + "\n"
         svm_file.write(clazz+featVector)
         visual_file.write(featVectorVisual+" "+clazz+ "\n")


    def cross_validation(self, data):
#        '''
#        use leave-one-out strategy for cross-validation
#        '''
#        accu = 0.0
#        for i in range(len(data)):
#            # all topics except for i-th topic are used to train.
#            train_data, test_data = data[:i] + data[i + 1:], [data[i]]
#            # Use Naive Bayesian Classifier for test.
#            classifier = nltk.NaiveBayesClassifier.train(train_data)
#            accu += nltk.classify.accuracy(classifier, test_data)
#        accu /= len(data)

        '''
        use 10-folder cross-validation strategy
        '''
        accu = 0.0
        k = 10
        n = len(data)
        for i in range(k):
            # all topics except for i-th topic are used to train.
            train_data, test_data = data[:i * n / k] + data[(i + 1) * n / k:], data[i * n / k : (i + 1) * n / k]
            # Use Naive Bayesian Classifier for test.
            classifier = nltk.NaiveBayesClassifier.train(train_data)
            accu += nltk.classify.accuracy(classifier, test_data)
        accu /= k

        print 'Accurary:', accu

    def save_within_feature(self, filename):
        f = open('.' + os.sep + filename, 'w')
        for (feature, clazz) in self._within_doc_feature_table:
            f.writelines(str(feature) + ' ' + str(clazz) + '\n')
        f.close()

    def save_cross_feature(self, filename):
        f = open('.' + os.sep + filename, 'w')
        for (feature, clazz) in self._cross_doc_feature_table:
            f.writelines(str(feature) + ' ' + str(clazz) + '\n')
        f.close()

if __name__ == '__main__':
    ft_extors = []
    # initialize your feature extractor by inheriting from class "FeatureExtractorBase"
    # and add it to the feature extractor list.
    # then the program can automatically use your feature extractor.paramparam
##    lexi_ft_extor = SampleFeatureExtractor()
##    ft_extors.append(lexi_ft_extor)

    #propbank
    pb_ft_extor = PropbankFeatureExtractor()
    ft_extors.append(pb_ft_extor)

##    lx_ft_extor = LexicalFeatureExtractor()
##    ft_extors.append(lx_ft_extor)

##    cos_ft_extor = CosineSimilarityFeatureExtractor()
##    ft_extors.append(cos_ft_extor)

##    wn_ft_extor = WordnetFeatureExtractor()
##    ft_extors.append(wn_ft_extor)

##    lexi_ft_extor = SampleFeatureExtractor()
##    ft_extors.append(lexi_ft_extor)

    # propbank
#    pb_ft_extor = PropbankFeatureExtractor()
#    ft_extors.append(pb_ft_extor)

    engine = MainEngine(ft_extors)
    #engine.run_within_doc()
    #engine.save_within_feature('SampleFeatureWithin.txt')

    engine.run_cross_doc()
    engine.save_cross_feature('SampleFeatureCross.txt')
#    engine.run_cross_doc()
