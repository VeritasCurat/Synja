#from project.dialog.NER import NER
'''
Created on 14.01.2019

@author: Johannes Grobelski

@summary: Allgemeine Funktionsweise 
- nlu bildet nutzereingabe(string) auf intents mithilfe der Trainingsdaten ab parse(...)
  davor wird der string auf rechtschreibung untersucht
- nlu kann beleidigungen/ausdruecke erkennen
import importlib
package='sklearn'
importlib.import_module(package)
'''
import os
import sys

sys.path.append(os.path.abspath('..'))
from simpleNLU_DE import simpleNLU_DE #@Unresolvedimport

from rasa_nlu.training_data import load_data
from rasa_nlu.components import ComponentBuilder
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Interpreter

#import tensorflow

#from project.dialog.NER import NER


#from numpy.f2py.tests.test_array_from_pyobj import intent
#from pylint.interfaces import Confidence

import re

verzeichnispfad = os.path.realpath(__file__)

trainingdataEN = os.path.join(os.path.dirname(verzeichnispfad),'nlu','de','training_de.json')
configfileEN = os.path.join(os.path.dirname(verzeichnispfad),'nlu','de','config_spacy_de.yml')


def levenshtein(s, t):
  #source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance
  #From Wikipedia article; Iterative with two matrix rows.
  if s == t: return 0
  elif len(s) == 0: return len(t)
  elif len(t) == 0: return len(s)
  v0 = [None] * (len(t) + 1)
  v1 = [None] * (len(t) + 1)
  for i in range(len(v0)):
      v0[i] = i
  for i in range(len(s)):
      v1[0] = i + 1
      for j in range(len(t)):
          cost = 0 if s[i] == t[j] else 1
          v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
      for j in range(len(v0)):
          v0[j] = v1[j]      
  return v1[len(t)]
      
class Woerterbuch():
  woerter = []
  beleidigungen = []
  
  
  
  def __init__(self):
    path = os.path.join(os.path.dirname(verzeichnispfad),'nlu','de','woerter.txt')
    if (sys.version_info > (3, 0)): file = open(path,'r',encoding="iso-8859-1")
    else: file = open(path,'r')
    while(True):
      line = file.readline().lower().replace('\n','')
      if(line == ""): break
      self.woerter.append(line)
    
    path2 = os.path.join(os.path.dirname(verzeichnispfad),'nlu','de','beleidigungen.txt')
    if (sys.version_info > (3, 0)): file2 = open(path2,'r',encoding="iso-8859-1")
    else: file2 = open(path2,'r')  
    while(True):
      line2 = file2.readline().lower().replace('\n','')
      if(line2 == ""): break
      self.beleidigungen.append(line2)  
  
  
  def profanity_check(self, word):
    #for p in self.profanities:
      #if(self.levenshtein(word, p) <= 1): return True
    if(word in self.beleidigungen): return True
    else: return False    
  
  
  def spellcheck(self, word):
    if(word in self.woerter): return True
    else: return False

class NLU_DE(object):
  builder = ComponentBuilder(use_cache=True) 
  training_data = load_data(trainingdataEN)
  trainer = Trainer(config.load(configfileEN), builder)
  trainer.train(training_data)
  interpreter = Interpreter.load(trainer.persist('model/default'))
   
  intent = ""
  confidence = 0
  
  dictionary = Woerterbuch()
  sNLU = simpleNLU_DE()
  
  
  def __init__(self):
    return    
  
    
  def parse_thema(self, eingabe):
    String = ""
    parsetext = eingabe.split(' ')
    for word in parsetext: 
      String = word     
      if(levenshtein(String, "Kontrollstrukturen") <= 2):return "controll structures"
      elif(levenshtein(String, "Programmstruktur") <= 2):return "programm structure"
      elif(levenshtein(String, "Grundlagen") <= 2):return "basics"
      elif(levenshtein(String, "Arrays") <= 2):return "arrays"
      elif(levenshtein(String, "Operatoren") <= 2):return "operators"
      elif(levenshtein(String, "Anweisungen") <= 2):return "statements"
      elif(levenshtein(String, "Methoden") <= 2):return "methods"
      elif(levenshtein(String, "Klassen") <= 2):return "classes"

    return ""
      
  def parse(self,Eingabe): 
    #print("trying to parse: \"" + Eingabe + "\"")
    eingabe = Eingabe.lower()
    eingabe = eingabe.replace(",", "")
    eingabe = eingabe.replace(".", "")
    eingabe = eingabe.replace(";", "")
    eingabe = eingabe.replace("!", "")
    eingabe = eingabe.replace("?", "")
    
    if(self.sNLU.toleranzpruefung(Eingabe) != ""): 
      print("nlu: eingabe: \""+eingabe+"\", intent: \"" + self.sNLU.toleranzpruefung(Eingabe) + "\", with confidence 100%")
      return self.sNLU.toleranzpruefung(Eingabe)


    while "  " in eingabe:
      eingabe = eingabe.replace("  "," ")
    if eingabe.startswith(" "):
      eingabe = eingabe[1:]  

    for word in eingabe.split(' '):
      if(self.dictionary.profanity_check(word) == True):
        return "profanity"  
    
    for word in eingabe.split(' '):
      if(self.dictionary.spellcheck(word) == False):
        return ""  
      
    try:
      intent =""    
      parse = self.interpreter.parse((eingabe))
      intent = parse['intent']['name']
      confidence = str(parse['intent']['confidence'])
      print("nlu: eingabe: \""+eingabe+"\", intent: \"" + intent + "\", with confidence " + str(float(confidence)))
      if(intent == "name"): 
        1+1
        #print(str(self.parseName(eingabe)))
      if float(confidence) < 0.40:
        intent = ""
      else: 
        return intent
    except Exception as e:
      print ('Generic exception: {}'.format(e))
      return intent
    return intent
    #except:
    #  print("Fehler: keine Exeception!")
    #  return ""
    
    
    
  def parseName(self, String):
    patterns = {r"my name is ([a-z])+": "my name is ", r"im called ([a-z])+": "im called "}  
    for pattern in patterns:
      if(re.search(pattern, String)):
        String = String.replace(String, re.search(pattern, String).group(0))
        String = String.replace(re.search(patterns[pattern], String).group(0), "")
        return String 
    return ""#self.ner.name_extraction(String)  
  
 
 
 
nlu = NLU_DE()
print(nlu.parse("hinweis"))