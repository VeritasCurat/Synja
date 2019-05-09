'''
Created on 27.02.2019

@author: johan
'''

import spacy
import numpy
from spacy.attrs import ENT_IOB, ENT_TYPE

class NER(object):
 
  nlp = spacy.load('en_core_web_sm')
  
  def unsinn(self, input):
    1+1
  
  def name_extraction(self, input):    
    words = input.split(" ")
    for word in words:
      Word = word[0].upper()+word[1:]
      Input = input.replace(word, Word)
      doc = self.nlp(Input)
    
      for ent in doc.ents:
        print(ent.text.lower())
        return ent.text.lower()
            
    return ""
  
          
  def __init__(self):
    11+1
    
ner = NER()
ner.name_extraction("im called devin")    
