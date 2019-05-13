'''
Created on 09.04.2019

@author: Johannes
'''
import os
from project.lehre.Expertenmodell import Expertenmodell
from project.lehre.javaparsing.parser import allreturns
from project.lehre.javaparsing.parser import parse
import unittest



'''    
def display_lesson(lesson):
  for konzept in ep.lessoninhalte[lesson]:
    print('\n'+konzept.upper()+'\n')
    print(ep.zugriffLehreinheit(lesson, konzept, "symbolisch", 0))
    print('\n'+"ENAKTIV:"+'\n')
    print(ep.zugriffLehreinheit(lesson, konzept, "enaktiv", 0))
    print(ep.antworten_anzeigen(lesson, konzept, "enaktiv", 0))
    print('\n'+"WORKED EXAMPLE:"+'\n')
    print(ep.zugriffLehreinheit(lesson, konzept, "worked_example", 0))
    print('\n'+"CODING:"+'\n')
    print(ep.zugriffLehreinheit(lesson, konzept, "coding", 0))
    print('\n'+"LUECKENTEXT:"+'\n')
    print(ep.zugriffLehreinheit(lesson, konzept, "test_lt", 0))
    print(ep.antworten_anzeigen(lesson, konzept, "test_lt", 0))
    print('\n'+"MULTIPLE-CHOICE:"+'\n')
    print(ep.zugriffLehreinheit(lesson, konzept, "test_mc", 0)) 
    print(ep.antworten_anzeigen(lesson, konzept, "test_mc", 0))
    
def display_allFB():
  for key in ep.fehlerbeschreibungen.keys():
    
def display_allLTMC():
  for lesson in ep.lessons:
    for konzept in ep.lessoninhalte[lesson]:    
      for i in range(len(ep.lessons[lesson].syntaxkonzepte[konzept].test_lt)):
        print(ep.zugriffLehreinheit(lesson, konzept, "test_lt", i))
        print("ANTWORTEN: "+ep.antworten_anzeigen(lesson, konzept, "test_lt", i))
      for i in range(len(ep.lessons[lesson].syntaxkonzepte[konzept].test_mc)):
        print(ep.zugriffLehreinheit(lesson, konzept, "test_mc", i))
        print("ANTWORTEN: "+ep.antworten_anzeigen(lesson, konzept, "test_mc", i)) 
'''

class Test(unittest.TestCase):

  
  verzeichnispfad = os.path.realpath(__file__)[:-23]
  
  ep = Expertenmodell("en")

  #prueft ob fuer alle konzepte mc, lt, coding und bilder vorhanden sind
  def testlehreinheiten_completeness_check(self):
    complete = True
    for lesson in self.ep.lessons:
      for konzept in self.ep.lessoninhalte[lesson]:
        if(len(self.ep.lessons[lesson].syntaxkonzepte[konzept].enaktiv ) == 0): 
          complete = False
          print("No enaktiv for: "+konzept)
    for lesson in self.ep.lessons:
      for konzept in self.ep.lessoninhalte[lesson]:    
        try:
          fh = open(self.verzeichnispfad+'project//webapp//static//'+lesson+"//"+konzept+".svg", 'r')
          fh.close()
        except FileNotFoundError:
          complete = False
          print("No picture for: "+konzept)
    for lesson in self.ep.lessons:
      for konzept in self.ep.lessoninhalte[lesson]:    
        if(len(self.ep.lessons[lesson].syntaxkonzepte[konzept].aufgaben ) == 0): 
          complete = False
          print("No aufgabe for: "+konzept)
        else:
          try:             
            aufgabe = self.ep.lessons[lesson].syntaxkonzepte[konzept].aufgaben[0]
            parse("",aufgabe.parsing_befehl)
          except: 
            complete = False
            print("Bad command: "+konzept)
    for lesson in self.ep. lessons:
      for konzept in self.ep.lessoninhalte[lesson]: 
        if(len(self.ep.lessons[lesson].syntaxkonzepte[konzept].examples ) == 0): 
          print("No example for: "+konzept)
          complete = False   
    for lesson in self.ep.lessons:
      for konzept in self.ep.lessoninhalte[lesson]:   
        if(len(self.ep.lessons[lesson].syntaxkonzepte[konzept].test_lt ) == 0): 
          print("No test_lt for: "+konzept)
          complete = False 
        else: 
          for i in range(len(self.ep.lessons[lesson].syntaxkonzepte[konzept].test_lt)):
            try:
              self.ep.antworten_anzeigen(lesson, konzept, "test_lt", i)
            except:
              complete = False
              print("Bad LT: "+konzept+" "+i)
    for lesson in self.ep.lessons:
      for konzept in self.ep.lessoninhalte[lesson]:    
        if(len(self.ep.lessons[lesson].syntaxkonzepte[konzept].test_mc ) == 0): 
          print("No test_mc for: "+konzept)
          complete = False
        else:
          for i in range(len(self.ep.lessons[lesson].syntaxkonzepte[konzept].test_lt)):
              try:
                self.ep.antworten_anzeigen(lesson, konzept, "test_lt", i)
              except:
                complete = False
                print("Bad MC: "+konzept+" "+i)
    if(complete):
      pass
    else: return complete
  
  def testkongruenz_fehler(self):
    kongruenz = True
    for fehler1 in self.ep.fehlerbeschreibungen.keys():
      if(fehler1 not in self.ep.fehlerreaktionen.keys()): 
        kongruenz = False
        print("Fehler nicht in fehlerreaktion: "+fehler1)  
      if fehler1 not in self.ep.fehlerhinweise.keys(): 
        kongruenz = False
        print("Konzept nicht in fehlerhinweise: "+fehler1)
        
    for fehler2 in self.ep.fehlerreaktionen.keys():
      if(fehler2 not in self.ep.fehlerbeschreibungen.keys()): 
        kongruenz = False
        print("Fehler nicht in fehlerbeschreibungen: "+fehler2)  
      if fehler1 not in self.ep.fehlerhinweise.keys(): 
        kongruenz = False
        print("Konzept nicht in fehlerhinweise: "+fehler1)
    
    for fehler3 in self.ep.fehlerhinweise.keys():
      if(fehler3 not in self.ep.fehlerbeschreibungen.keys()): 
        kongruenz = False
        print("Fehler nicht in fehlerbeschreibungen: "+fehler3)  
      if fehler3 not in self.ep.fehlerreaktionen.keys(): 
        kongruenz = False
        print("Konzept nicht in fehlerreaktionen: "+fehler3)    
        
    for fehler4 in self.ep.fehlerbeschreibungen.keys():
      if(fehler4 not in allreturns): 
        kongruenz = False
        print("Fehler aus fehlerbeschreibungen nicht in parserfehlerlist: "+fehler4)  
      
    
    for fehler5 in allreturns:
      if(fehler5 not in allreturns): 
        kongruenz = False
        print("Fehler aus parserfehlerlist nicht in fehlerbeschreibungen: "+fehler5)
      #if(fehler4 not in self.ep.fehlerbeschreibungen.keys()): 
      #  print("Fehler aus parser nicht in fehlerbeschreibungen: "+fehler4)  
    
    if(kongruenz):
      print("Kongruenz")  
      pass
      #if konzept not in self.ep.fehlerhinweise.keys(): print("Konzept nicht in fehlerhinweise: "+konzept)
    #for konzept in self.ep.fehlerhinweise.keys():
    #  if konzept not in self.ep.fehlerbeschreibungen.keys(): print("Konzept nicht in fehlerbeschreibungen: "+konzept)  
    #  if konzept not in self.ep.fehlerreaktionen.keys(): print("Konzept nicht in fehlerreaktionen: "+konzept)
  
  
  #lehreinheiten_completeness_check()
  #kongruenz_fehler()

  def testName(self):
      pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()