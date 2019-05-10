'''
Created on 13.03.2019

@author: Johannes
'''
from lehre.javaparsing.parser import *

class Underline_Task(object):
    konzept = ""
    aufgabenstellung = ""
    loesungen = []
    geloeste = []
    
    def __init__(self, konzept, aufgabenstellung, loesung):
      self.konzept = konzept
      self.aufgabenstellung = aufgabenstellung
      self.loesungen = loesung
    
    def loesen(self, nutzerantwort):
      nantwort = nutzerantwort.replace('\n','')
      for loesung in self.loesungen:
        lsg = self.loesungen[0].replace('\n','')
        
        schnitt=""
        if(len(lsg) > len(nantwort)):schnitt = lsg.replace(nantwort,"")
        else:schnitt = nantwort.replace(lsg,"")

        schnitt = schnitt.replace('\\n','\n')
        patternlsg = r"[\n\t\r]*"
        
        for a in schnitt:
          if(a!=' ' and a!='\n'):
            print("SCHNITTFAULT: "+a)
            return False
        
        if(nutzerantwort in self.geloeste):
          return "schon_geloest"
        else: 
          self.geloeste.append(nutzerantwort)
          return True
    

class Aufgabe(object):
    aufgabenstellung = ""
    
    parsing_befehl = ""
    loesung = ""
  

    def __init__(self, aufgabenstellung, parsing_befehl, loesung):
      self.aufgabenstellung = aufgabenstellung
      
      if(parsing_befehl != ""):
        self.parsing_befehl = parsing_befehl
      elif(loesung != ""):
        self.loesung = loesung
      else: 
        print("Wrong syntax for parsing: "+parsing_befehl)
        exit(-1)
      self.loesung = loesung
      
    def loesung(self, input):
      if(self.parsing_befehl == "" and input != ""):
        if(input == self.loesung): return True
        else: return False
      elif(self.parsing_befehl != "" and input == ""):
        return parse(input, self.parsing_befehl)
      else:
        print("Wrong syntax for parsing: "+self.parsing_befehl)
        exit(-1)