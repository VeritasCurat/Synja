'''
Created on 13.03.2019

@author: Johannes
'''
from lehre.javaparsing.parser import *

class Enaktiv(object):
  
    typ = ""
    konzept = ""
    aufgabenstellung = ""
    loesung = ""
    schritte_beispiele = []
    beispiele = []

    def __init__(self, konzeptname, aufgstellung, loesung, schritte_beispiele, typ):
      self.typ = typ
      self.konzept = konzeptname
      self.aufgabenstellung = aufgstellung
      self.loesung = loesung
      
      self.schritte_beispiele = schritte_beispiele
              
    def loesen(self, input):
      for loesung in self.loesungen:
        print(loesung)
        if(input == loesung): return True
        else:
          if("$parse" in loesung): return parse(input, loesung[loesung.index("$parse")+7:])
          else: continue
      return False
        
     