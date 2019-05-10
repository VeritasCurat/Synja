'''
Created on 21.01.2019
@author: Johannes Grobelski

'''


from project.lehre.Lehrmanager import Lehrmanager
from project.lehre.Expertenmodell import Expertenmodell
 
from project.dialog.Dialogmanager import Dialogmanager
from project.dialog.NLG import NLG
from project.dialog.NLU import NLU

import warnings

class Synja():
  nlu = NLU("en")
  nlg = NLG("en")
  expertenmodell=Expertenmodell("en")
  dialogmanager=Dialogmanager("")
  lehrmanager=Lehrmanager("", expertenmodell.lessoninhalte, expertenmodell.anzahl_erklaerungen, expertenmodell.anzahlAufg,  expertenmodell.anzahlWE, expertenmodell.anzahl_lt, expertenmodell.anzahl_mc, expertenmodell.en_schritt_dict)
  name = ""
  ui = 0 #TODO
  totalCount = 0  
  
  inputDialog = ""
  outputDialog = []
  outputLehre = None
  
  outputLehreTest = []
  
  def ersteAusgabe(self):
    return self.nlg.generate(self.dialogmanager.gespraechsausgaben[0])


  def eingabeLehrebene(self): 
    self.dialogmanager.schritt("eingabeLehre", "")
  
  #main method, organize the whole structure of the dialogue#
  def schritt(self, inputDialog, inputLehre):
    if(inputDialog != ""):
      eingabe_intent = self.nlu.parse(inputDialog)
      entity = self.nlu.parseName(inputDialog)     
      if(eingabe_intent!="name"): 
        entity = self.nlu.parse_thema(inputDialog)
        if(entity != ""): eingabe_intent="naechsterThemenblock"
        
      print("SL input: "+inputDialog+" intent: "+eingabe_intent+" entity: "+entity)  
      
      self.lehrmanager.schritt(eingabe_intent,entity)  
        

      if("bye" in self.lehrmanager.dialogausgaben):
        print("VERABSCHIEDUNG")
        exit(1)

      for s in self.lehrmanager.dialogausgaben: 
        phrase = ""
        if isinstance(s, list):
          phrase = self.nlg.generate_args(s[0], s[1])
        else:
          phrase = self.nlg.generate(s)
        self.outputDialog.append(phrase)  
          
      self.outputLehre = self.lehrmanager.getLehrAusgaben()   
      
    if(inputLehre != ""):
      
      self.lehrmanager.schritt(inputLehre,"")
      
      for s in self.lehrmanager.dialogausgaben: 
        phrase = ""
        if isinstance(s, list):
          phrase = self.nlg.generate_args(s[0], s[1])
        else:
          phrase = self.nlg.generate(s)
        self.outputDialog.append(phrase)     

      self.outputLehre = self.lehrmanager.getLehrAusgaben()   
      
    print("ready")
                
        
  def __init__(self):  
    warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

    #self.nlu = NLU()

    #self.lehrmanager = Lehrmanager(id)
 
  def displayAll(self):
    for lesson in self.expertenmodell.lessons.keys():
      for syntaxkonzept in self.expertenmodell.lessons[lesson].syntaxkonzepte.keys():
        #alle examples ausgeben
        i=0
        for version in self.expertenmodell.lessons[lesson].syntaxkonzepte[syntaxkonzept].examples:
          self.outputLehreTest.append(self.expertenmodell.zugriffLehreinheit(lesson, syntaxkonzept, "worked_example", i))
          i+=1
        '''
        #alle mc ausgeben
        i=0
        for version in self.expertenmodell.lessons[lesson].syntaxkonzepte[syntaxkonzept].test_mc:
          self.outputLehreTest.append(self.expertenmodell.zugriffLehreinheit(lesson, syntaxkonzept, "test_mc", i))
          self.outputLehreTest.append(self.expertenmodell.zugriffLehreinheit(lesson, syntaxkonzept, "test_mc_answer", i))
          i+=1
        #alle lt ausgeben  
        i=0
        for version in self.expertenmodell.lessons[lesson].syntaxkonzepte[syntaxkonzept].test_lt:
          self.outputLehreTest.append(self.expertenmodell.zugriffLehreinheit(lesson, syntaxkonzept, "test_lt", i))
          self.outputLehreTest.append(self.expertenmodell.zugriffLehreinheit(lesson, syntaxkonzept, "test_lt_answer", i))
          i+=1  
        '''