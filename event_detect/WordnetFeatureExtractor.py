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
class WordnetFeatureExtractor(FeatureExtractorBase):
    '''
    This is the base class of feature extractors
    You need to implement your own feature extractors,
    e.g. Class Features (CF), WordNet Features (WF)
    Semantic Features (SF).
    '''
    def __init__(self):
        self.pathSim={}

    def findMax(self,mensX,mensY):
            maxSim = 0
            for wnx in wn.synsets(mensX)[0:4]:
              for wny in wn.synsets(mensY)[0:4]:
                sim = wnx.path_similarity(wny)
                if sim>maxSim:
                    maxSim = sim
            return maxSim

    def extract(self, em1, em2):
       features = {}
       em1 = em1.get_mention()
       em2 = em2.get_mention()
       if not self.pathSim.has_key((em1,em2)):
        self.pathSim[(em1,em2)] = self.findMax(em1,em2)
        features['pathSim']= self.pathSim[(em1,em2)]
       return features

    def __str__(self):
        pass



def main():
    pass

if __name__ == '__main__':
    main()
