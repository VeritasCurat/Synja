'''
Created on 21.01.2019

@author: Johannes
'''
import os
import sys
sys.path.append(os.path.abspath('../lehre'))


source = "rasa\phrasesEN.json"
import random
import os
import re

class Dict_konzept_phrase:
  
  dict = {}
  
  def __init__(self):
    verzeichnispfad = os.path.realpath(__file__)
    path = os.path.join(os.path.dirname(verzeichnispfad),'nlg','translation_konzept_phrase_en.txt')
    file = open(path,'r')
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
    verzeichnispfad = os.path.realpath(__file__)
    path = os.path.join(os.path.dirname(verzeichnispfad),'nlg','phrasesEN.txt')
    file = open(path,'r')
    while(True):
        line = file.readline()
        if(line==""):break
        #neuer Eintrag
        if("=" in line):            
          pattern = r"= \""
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
    
    
    
class NLG_EN(object):
  
    sprache = ""
    genbase = object   #frage_verstanden -> Do you understand $?
    dict_konzept_phrase = object #main -> the main method 
    
    
    def __init__(self):
      self.genbase = Genbase()
      self.dict_konzept_phrase = Dict_konzept_phrase()
      return
    
    def uebersetzung_thema(self,e):
      if(e == "programm_structure"):return "program structure"
      if(e == "basics"):return "basics"
      if(e == "arrays"):return "arrays"
      if(e == "operators"):return "operators"
      if(e == "statements"):return "statements"
      if(e == "controll_structures"):return "control structures"
      if(e == "methods"):return "methods"
      if(e == "classes"):return "classes"
    
    def generate_args(self, phrase, arg): 
      p = phrase

      if(phrase in  self.genbase.dict.keys()):
        phrase = random.choice( self.genbase.dict[phrase])
        
        if isinstance(arg,list):
          if(p == "empfehlung_naechsterThemenblock"):
            subsen = ""
            if(len(arg)>2):
              for i in range(len(arg)-2):
                subsen += self.uebersetzung_thema(arg[i])+", "
              subsen+= self.uebersetzung_thema(arg[len(arg)-2])+" and "+self.uebersetzung_thema(arg[len(arg)-1])
            elif(len(arg)==2):
              subsen+= self.uebersetzung_thema(arg[len(arg)-2])+" and "+self.uebersetzung_thema(arg[len(arg)-1])
            elif(len(arg)==1):
              subsen+= self.uebersetzung_thema(arg[len(arg)-1])
            return phrase.replace("$",subsen)         
        
        if arg in self.dict_konzept_phrase.dict.keys():
          ph = self.dict_konzept_phrase.dict[arg]
          phrase = phrase.replace("$", ph,1)
          
        else: phrase = phrase.replace("$", arg,1)
        if(": <b>$</b>" in phrase): phrase = phrase.replace(": <b>$</b>",".")
      
      else: 
        print("phrase: \""+phrase+"\" nicht in nlg vorhanden!")
        exit(-1)

      #fix python2
      phrase = repr(phrase)
      while("\\\"\\r" in phrase): phrase = phrase.replace("\\\"\\r",'')
      while("\"" in phrase): phrase = phrase.replace("\"",'')
      while("\\r" in phrase): phrase = phrase.replace("\\r",'')
      while("\\'" in phrase): phrase = phrase.replace("\\'",'')
      while("\'" in phrase): phrase = phrase.replace("\'",'')     

      return phrase
    
    def generate(self, phrase):
      ausgabe = ""
      if(phrase in  self.genbase.dict.keys()):
        
        ausgabe = random.choice( self.genbase.dict[phrase])
      
      else: 
        print("phrase: \""+phrase+"\" nicht in nlg vorhanden!")
        exit(-1)
    
      ausgabe = ausgabe.replace("\n",'\\n')    
      return ausgabe
