'''
Created on Nov 1, 2012

@author: jasonleakey
'''
import unittest
from svmutil import *


class Test(unittest.TestCase):
    def testSVM(self):
        y, x = svm_read_problem('heart_scale')
        m = svm_train(y[:200], x[:200], '-c 4')
        p_label, p_acc, p_val = svm_predict(y[200:], x[200:], m)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
