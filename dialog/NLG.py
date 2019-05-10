'''
Created on 21.01.2019

@author: Johannes
'''
from lehre.Expertenmodell import Expertenmodell

source = "rasa\phrasesEN.json"
import random
import os
import re

class Dict_konzept_phrase:
  
  dict = {}
  
  def __init__(self):
    path = os.path.realpath(__file__)[:-14]+"\\dialog\\nlg\\translation_konzept_phrase.txt"
    file = open(path)
    while(True):
        line = file.readline()
        if(line==""):break
        #neuer Eintrag
        if(line.startswith('#')):continue
        if("=" in line):            
          pattern = r"="
          data = re.split(pattern, line)
          if(data[0] != None):
            name = data[0]
            while(name.startswith(' ') or name.startswith('\"')): name = name[1:]
            while(name.endswith(' ') or name.endswith('\"')): name = name[:-1]

          if(data[1] != None):
            phrase = data[1][:-1]
            while(phrase.startswith(' ') or phrase.startswith('\"')): phrase = phrase[1:]
            while(phrase.endswith(' ') or phrase.endswith('\"')): phrase = phrase[:-1]
          if(name != None and phrase != None):
              if(name not in self.dict.keys()): 
                self.dict[name] = ""
              self.dict[name] = phrase


class Genbase:
  
  dict = {}
  
  def __init__(self):
    path = os.path.realpath(__file__)[:-14]+"\\dialog\\nlg\\phrasesEN.txt"
    file = open(path)
    while(True):
        line = file.readline()
        if(line==""):break
        #neuer Eintrag
        if("=" in line):            
          pattern = r"="
          data = re.split(pattern, line)
          if(data[0] != None):
            name = data[0]
            while(name.startswith(' ') or name.startswith('\"')): name = name[1:]
            while(name.endswith(' ') or name.endswith('\"')): name = name[:-1]

          if(data[1] != None):
            phrase = data[1][:-1]
            while(phrase.startswith(' ') or phrase.startswith('\"')): phrase = phrase[1:]
            while(phrase.endswith(' ') or phrase.endswith('\"')): phrase = phrase[:-1]
          if(name != None and phrase != None):
              if(name not in self.dict.keys()): 
                self.dict[name] = []
              self.dict[name].append(phrase)
    
    
    
class NLG(object):
  
    sprache = ""
    genbase = object   #frage_verstanden -> Do you understand $?
    dict_konzept_phrase = object #main -> the main method 
    
    
    def __init__(self,sprache):
      self.sprache = sprache
      self.genbase = Genbase()
      self.dict_konzept_phrase = Dict_konzept_phrase()
      return
    
    def generate_args(self, phrase, arg):
      if(self.sprache == "en"):
        if(phrase in  self.genbase.dict.keys()):
          phrase = random.choice( self.genbase.dict[phrase])
                   
          
          if arg in self.dict_konzept_phrase.dict.keys():
            ph = self.dict_konzept_phrase.dict[arg]
            phrase = phrase.replace("$", ph,1)
            return phrase
          else: phrase = phrase.replace("$", arg,1)
          if(": <b>$</b>" in phrase): phrase = phrase.replace(": <b>$</b>",".")
        
        else: 
          print("phrase: \""+phrase+"\" nicht in nlg vorhanden!")
          exit(-1)
    
      phrase = phrase.replace("\n",'\\n')
      return phrase
    
    def generate(self, phrase):
      ausgabe = ""
      if(self.sprache == "en"):
        if(phrase in  self.genbase.dict.keys()):
          
          ausgabe = random.choice( self.genbase.dict[phrase])
        
        else: 
          print("phrase: \""+phrase+"\" nicht in nlg vorhanden!")
          exit(-1)
    
      ausgabe = ausgabe.replace("\n",'\\n')    
      return ausgabe
    
    
