#!/usr/bin/python -B

import nltk
import commands
import re
import cosineSimilarity

class PropbankFeatureExtractor():
    """
    To extract the propbank feature.
    """
    def __init__(self):
        self.s1_in_file = "./propbankfeature/s1_in.txt"
	self.s1_out_file = "./propbankfeature/s1_out.txt"
	self.s2_in_file = "./propbankfeature/s2_in.txt"
	self.s2_out_file = "./propbankfeature/s2_out.txt"
	self.lines = []
	
        #ARG0,ARG1....for sentence 1
	self.s1_A0 = []
	self.s1_V  = []
	self.s1_A1 = []
	self.s1_A2 = []
	self.s1_A3 = []
	self.s1_LOC = []
	self.s1_TMP = []
  
        #ARG0,ARG1....for sentence 2 
	self.s2_A0 = []
	self.s2_V  = []
	self.s2_A1 = []
	self.s2_A2 = []
	self.s2_A3 = []
	self.s2_LOC = []
	self.s2_TMP = []
        
        #value
	self.value1 = None
	self.value2 = None
	self.value_arg0 = None
	self.value_arg1 = None
	self.value_arg2 = None
	self.value_arg3 = None
	self.value_loc = None
	self.value_tmp = None
	
        #final value
	self.final_value = None
	
    def __clean_files(self):
        command = "rm ./propbankfeature/s1_* ./propbankfeature/s2_*"
	commands.getoutput(command)
    
    def __write_to_file(self,sentence,file_name):
        try:
	    f = open(file_name, "w")
	    try:
	        f.write(sentence)
            finally:
	        f.close()
	except IOError:
	    pass
     
    def __read_from_file(self,file_name):
        try:
	    f = open(file_name)
	    self.lines = f.readlines()
	except IOError as e:
	    print ("I/O error({0}): {1}".format(e.errno, e.strerror))
	    raise
    
    def extract(self, em1, em2):
        """
        To extract the PropBank feature.
        """
	#get the sentence from event mention
	s1_obj = em1.get_sent()
	sentence1 = s1_obj.remove_anno()

	s2_obj = em2.get_sent()
	sentence2 = s2_obj.remove_anno()
        
        #for sentence1
	self.__write_to_file(sentence1,self.s1_in_file)
        command = './senna -srl <' + self.s1_in_file +'> ' + self.s1_out_file
        commands.getoutput(command)
        self.__read_from_file(self.s1_out_file)	
	for line in self.lines:
	    if line == '\n':
		break
            words = re.findall(r'\w+|\.', line)
	    if words == []:
	       continue
	    first_word = words[0]
            for word in words:
               if word == "A0":
                  self.s1_A0.append(first_word)
		  break
	       if word == "V":
		  self.s1_V.append(first_word)
		  break
	       if word == "A1":
		  self.s1_A1.append(first_word)
		  break
	       if word == "A2":
		  self.s1_A2.append(first_word)
		  break
	       if word == "A3":
		  self.s1_A3.append(first_word)
		  break
	       if word == "LOC":
		  self.s1_LOC.append(first_word)
		  break
	       if word == "TMP":
		  self.s1_TMP.append(first_word)
		  break

        #for sentence2	
	self.__write_to_file(sentence2,self.s2_in_file)
        command = './senna -srl <' + self.s2_in_file +'> ' + self.s2_out_file
        commands.getoutput(command)
        self.__read_from_file(self.s2_out_file)	
	for line in self.lines:
	    if line == '\n':
		break
            words = re.findall(r'\w+|\.', line)
	    if words == []:
	       continue
	    first_word = words[0]
            for word in words:
               if word == "A0":
                  self.s2_A0.append(first_word)
		  break
	       if word == "V":
		  self.s2_V.append(first_word)
		  break
	       if word == "A1":
		  self.s2_A1.append(first_word)
		  break
	       if word == "A2":
		  self.s2_A2.append(first_word)
		  break
	       if word == "A3":
		  self.s2_A3.append(first_word)
		  break
	       if word == "LOC":
		  self.s2_LOC.append(first_word)
		  break
	       if word == "TMP":
		  self.s2_TMP.append(first_word)
		  break

        #compute value
        self.__compute_value1()
	self.__compute_value2()
	self.__compute_arg0()
	self.__compute_arg1()
	self.__compute_arg2()
	self.__compute_arg3()
	self.__compute_arg_loc()
	self.__compute_arg_tmp()

        #compute the final value
	self.final_value = self.value1 * 0.05 + self.value2 * 0.1 + \
	                   self.value_arg0 * 0.2 + \
			   self.value_arg1 * 0.2 + \
			   self.value_arg2 * 0.2 + \
			   self.value_arg3 * 0.05 + \
			   self.value_loc * 0.1 + \
			   self.value_tmp * 0.1

        #clean procedure
	self.__clean_files()

        #record the result
	features = {}
	features['Propbank'] = self.final_value
	features['ARG0'] = self.value_arg0 
	features['ARG1'] = self.value_arg1
	features['ARG2'] = self.value_arg2
	features['ARG3'] = self.value_arg3
	features['LOC'] = self.value_loc
	features['TMP'] = self.value_tmp
	
	f_file = open("./propbankfeature/features.txt","a")
	feature_string = str(features['Propbank']) + ' ' +\
	                 str(features['ARG0']) + ' ' +\
			 str(features['ARG1']) + ' ' +\
			 str(features['ARG2']) + ' ' +\
			 str(features['ARG3']) + ' ' +\
			 str(features['LOC']) + ' ' +\
			 str(features['TMP']) + '\n'
	f_file.write(feature_string)
#	self.test()
        
	#reset
	self.__init__()

	return features

    def __compute_arg0(self):
        #arg0
	s1_arg0 = ""
	for s in self.s1_A0:
	    s1_arg0 += s + ' '
	
	s2_arg0 = ""
	for s in self.s2_A0:
            s2_arg0 += s + ' '
	if s1_arg0 == s2_arg0 and s1_arg0 != '':
	    self.value_arg0 = 1
	elif s1_arg0 == '' or s2_arg0 == '':
	    self.value_arg0 = 0.25
        else: 
	    result = cosineSimilarity.compare(s1_arg0 ,s2_arg0)
	    if result == result:
	        self.value_arg0 = result
            else:
		self.value_arg0 = 0.25

    def __compute_arg1(self):
        #arg1
	s1_arg1 = ""
	for s in self.s1_A1:
	    s1_arg1 += s + ' '
	
	s2_arg1 = ""
	for s in self.s2_A1:
            s2_arg1 += s + ' '
	if s1_arg1 == s2_arg1 and s1_arg1 != '':
	    self.value_arg1 = 1
	elif s1_arg1 == '' or s2_arg1 == '':
	    self.value_arg1 = 0.25
        else: 
	    result = cosineSimilarity.compare(s1_arg1 ,s2_arg1)
	    if result == result:
	        self.value_arg1 = result
            else:
		self.value_arg1 = 0.25

    def __compute_arg2(self):
        #arg2
	s1_arg2 = ""
	for s in self.s1_A2:
	    s1_arg2 += s + ' '
	
	s2_arg2 = ""
	for s in self.s2_A2:
            s2_arg2 += s + ' '
	if s1_arg2 == s2_arg2 and s1_arg2 != '':
	    self.value_arg2 = 1
	elif s1_arg2 == '' or s2_arg2 == '':
	    self.value_arg2 = 0.25
        else: 
	    result = cosineSimilarity.compare(s1_arg2 ,s2_arg2)
	    if result == result:
	        self.value_arg2 = result
            else:
		self.value_arg2 = 0.25

    def __compute_arg3(self):
        #arg3
	s1_arg3 = ""
	for s in self.s1_A3:
	    s1_arg3 += s + ' '
	
	s2_arg3 = ""
	for s in self.s2_A3:
            s2_arg3 += s + ' '
	if s1_arg3 == s2_arg3 and s1_arg3 != '':
	    self.value_arg3 = 1
	elif s1_arg3 == '' or s2_arg3 == '':
	    self.value_arg3 = 0.25
        else: 
	    result = cosineSimilarity.compare(s1_arg3 ,s2_arg3)
	    if result == result:
	        self.value_arg3 = result
            else:
		self.value_arg3 = 0.25
    
    def __compute_arg_loc(self):
        #arg_loc
	s1_arg_loc = ""
	for s in self.s1_LOC:
	    s1_arg_loc += s + ' '
	
	s2_arg_loc = ""
	for s in self.s2_LOC:
            s2_arg_loc += s + ' '
	if s1_arg_loc == s2_arg_loc and s1_arg_loc != '':
	    self.value_loc = 1
	elif s1_arg_loc == '' or s2_arg_loc == '':
	    self.value_loc = 0.25
        else: 
	    result = cosineSimilarity.compare(s1_arg_loc ,s2_arg_loc)
	    if result == result:
	        self.value_loc = result
            else:
		self.value_loc = 0.25
    
    def __compute_arg_tmp(self):
        #arg_tmp
	s1_arg_tmp = ""
	for s in self.s1_TMP:
	    s1_arg_tmp += s + ' '
	
	s2_arg_tmp = ""
	for s in self.s2_TMP:
            s2_arg_tmp += s + ' '
	if s1_arg_tmp == s2_arg_tmp and s1_arg_tmp != '':
	    self.value_tmp = 1
	elif s1_arg_tmp == '' or s2_arg_tmp == '':
	    self.value_tmp = 0.25
        else: 
	    result = cosineSimilarity.compare(s1_arg_tmp ,s2_arg_tmp)
	    if result == result:
	        self.value_tmp = result
            else:
		self.value_tmp = 0.25

    def __compute_value1(self):
        #value 1,the number of argument
	self.value1 = 0
	count1 = count2 = 0
	if self.s1_A0 != []:
	    count1 += 1
	if self.s1_A1 != []:
            count1 += 1
	if self.s1_A2 != []:
            count1 += 1
	if self.s1_A3 != []:
            count1 += 1
	if self.s1_LOC != []:
            count1 += 1
        if self.s1_TMP != []:
            count1 += 1
	
	if self.s2_A0 != []:
	    count2 += 1
	if self.s2_A1 != []:
            count2 += 1
	if self.s2_A2 != []:
            count2 += 1
	if self.s2_A3 != []:
            count2 += 1
	if self.s2_LOC != []:
            count2 += 1
        if self.s2_TMP != []:
            count2 += 1
	
	if count1 == count2:
            self.value1 = 1

    def __compute_value2(self):
        #value 2,the number of argument which are same
	self.value2 = 0
	if self.s1_A0 == self.s2_A0 and self.s1_A0 != []:
		self.value2 += 0.2
	if self.s1_A1 == self.s2_A1 and self.s1_A1 != []:
		self.value2 += 0.2
	if self.s1_A2 == self.s2_A2 and self.s1_A2 != []:
		self.value2 += 0.1
	if self.s1_A3 == self.s2_A3 and self.s1_A3 != []:
		self.value2 += 0.1
	if self.s1_LOC == self.s2_LOC and self.s1_LOC != []:
		self.value2 += 0.2
	if self.s1_TMP == self.s2_TMP and self.s1_TMP != []:
		self.value2 += 0.2


    def test(self):
	print "S1-----------------------"
	print self.s1_A0
	print self.s1_A1
	print self.s1_A2
	print self.s1_A3
	print self.s1_LOC
	print self.s1_TMP
	print "S2-----------------------"
	print self.s2_A0
	print self.s2_A1
	print self.s2_A2
	print self.s2_A3
	print self.s2_LOC
	print self.s2_TMP
#TODO
    def __str__(self):
        print "..."

if __name__ == "__main__":
    pb_feature = PropbankFeatureExtractor()
    sent1 = "Jone meet jack in Chine in 1988"
    sent2 = "Jay see Jone in Chine in 1988."
    pb_feature.extract(sent1,sent2)
    pb_feature.test() 
