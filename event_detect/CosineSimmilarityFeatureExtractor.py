#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      PRASANNA
#
# Created:     06/12/2012
# Copyright:   (c) PRASANNA 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import wordnet as wn
import nltk
import re
import os
import porter
from numpy import zeros,dot
from numpy.linalg import norm

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
class CosineSimilarityFeatureExtractor(FeatureExtractorBase):
    def __init__(self):
     # import real stop words
      self.stop_words = [ 'i', 'in', 'a', 'to', 'the', 'it', 'have', 'haven\'t', 'was', 'but', 'is', 'be', 'from' ]
     #stop_words = [w.strip() for w in open('english.stop','r').readlines()]
     #print stop_words
      self.splitter=re.compile ( "[a-z\-']+", re.I )
      self.stemmer=porter.PorterStemmer()
      self.all_words=dict()

    def add_word(self,word):
     w=word.lower()
     if w not in self.stop_words:
      ws=self.stemmer.stem(w,0,len(w)-1)
      self.all_words.setdefault(ws,0)
      self.all_words[ws] += 1

    def doc_vec(self,doc,key_idx):
        v=zeros(len(key_idx))
        for word in self.splitter.findall(doc):
         keydata=key_idx.get(self.stemmer.stem(word,0,len(word)-1).lower(), None)
         if keydata: v[keydata[0]] = 1
        return v

    def compare(self,doc1,doc2):

    # strip all punctuation but - and '
    # convert to lower case
    # store word/occurance in dict


     for dat in [doc1,doc2]:
      [self.add_word(w) for w in self.splitter.findall(dat)]

    # build an index of keys so that we know the word positions for the vector
     key_idx=dict() # key-> ( position, count )
     keys=self.all_words.keys()
     keys.sort()
     #print keys
     for i in range(len(keys)):
      key_idx[keys[i]] = (i,self.all_words[keys[i]])
     del keys
     self.all_words={}

     v1=self.doc_vec(doc1,key_idx)
     v2=self.doc_vec(doc2,key_idx)
     return float(dot(v1,v2) / (norm(v1) * norm(v2)))


    def extract(self, em1,em2):
      cos={}
      features = {}
      sent1= em1.get_sent()
      sent2= em2.get_sent()
      sent1 = sent1.remove_anno()
      sent2 = sent2.remove_anno()
      cos[(sent1, sent2)]= self.compare(sent1,sent2)
      features['cosineSim'] = cos[(sent1,sent2)]
      return features

    def __str__(self):
        pass


def main():
    pass

if __name__ == '__main__':
    main()
