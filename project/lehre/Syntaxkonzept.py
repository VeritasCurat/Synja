'''
Created on 22.01.2019
@author: Johannes

@summary: Allgemeine Funktionsweise:
- Speichert darstellungsarten und testarten als eine Einheit
- Bewertet lehreingaben von Nutzer mit gewisser toleranz
'''
import sys
import os

sys.path.append(os.path.abspath('../webapp'))
sys.path.append(os.path.abspath('../lehre'))

from Nutzer import Nutzer #@Unresolvedimport
from Lueckentext import Lueckentext #@Unresolvedimport
from javaparsing.javaparser import parse #@Unresolvedimport

class Syntaxkonzept(object):
    name = ""
    darstellung_symbolisch = None
    darstellung_ikonisch = None
    enaktiv = None
    examples = None
    test_lt= None
    test_mc = None
    aufgaben = None
    underline_aufgaben = None
    fkdata = {}

    def __init__(self, Name):
      self.name = Name
      self.darstellung_symbolisch = []
      self.examples = []
      self.test_lt = []
      self.test_mc = []
      self.aufgaben = []
      self.enaktiv =[]
      self.underline_aufgaben = []
      return
      
    
      
    def richtige_anworten(self, art, version): 
      prefix = ["There is no solution.", "The solution is: ", "The solutions are: "]
      ret = "\n"
      if(art == "test_mc"):
          loesungen = self.test_mc[version].loesungen
          if(len(loesungen)==0):return prefix[0]
          if(len(loesungen)==1):ret+=prefix[1]+'\n'
          if(len(loesungen)>1):ret+=prefix[2]+'\n'
          i = 0  
          for loesung in loesungen:
            index = self.translate_index(loesung)
            if(index != None): 
              a = ""
              if(i==0): a = self.test_mc[version].antworten[index-1][:-1]+'\n'
              elif(i>0): a = self.test_mc[version].antworten[index-1][1:-1]+'\n'
              if(a.startswith("\"")):
                a = a[1:]
              ret+= loesung+". "+a
              i+=1
          return ret
      elif(art == "test_lt"):
          loesungen = self.test_lt[version].loesungen   
          if(len(loesungen)==0):return prefix[0]
          if(len(loesungen)==1):
            ret+=prefix[1]
          if(len(loesungen)>1):ret+=prefix[2]+'\n'
          if(len(loesungen) > 1):
            i=1
            for loesung in loesungen:
              ret += str(i)+". "+self.test_lt[version].aufgabe.replace("___", loesung)+'\n'
              i+=1
          else: ret += '\n'+self.test_lt[version].aufgabe.replace("___", loesungen[0])
          return ret
      elif(art == "underline_task"):
        loesungen = self.underline_aufgaben[version].loesungen
        print(len(loesungen))
        return ret
      elif(art == "enaktiv"):
        loesungen = self.enaktiv[version].loesungen
        loesung = ""
        for l in loesungen:
          loesung += l+'\n'
        print(len(loesung))
        return loesung
      else: 
        print("Unbekanntes Aufgabenformat!")
        exit(-1)
            
    def bewertung_enaktiv(self,schritt,antwort):
      if(schritt < len(self.enaktiv[0].schritte_beispiele)):
        return (self.enaktiv[0].schritte_beispiele[schritt]).replace(' ','') == antwort.replace(' ','')         
      return False
      
    def bewertung(self, art, version, antworttext):  
      #print("sk bewertung: darstellungsart: "+art+" version: "+str(version)+" antworttext: "+str(antworttext)+" konzept: "+self.name) 
      if(art == "test_mc"):
        #umwandlung von string in array
        loesungencpy = self.test_mc[version].loesungen
        nutzerantwort =[]
        for zeichen in antworttext:
          if(zeichen.isdigit()==True):
            nutzerantwort.append(zeichen)   
        if(len(nutzerantwort) != len(loesungencpy)):return False
        for loesung in nutzerantwort:
          if(loesung in loesungencpy):
            loesungencpy.remove(loesung)
        if(len(loesungencpy)==0):return True
        else: return False
      elif(art == "test_lt"):
        loesungen = self.test_lt[version].loesungen
        for _antwort in loesungen:
          #print("loesung LT: "+str(_antwort))
          if Lueckentext.beantworten(_antwort,antworttext):
            return True
        else: return False
      elif(art == "coding"):
        print(self.aufgaben[0].parsing_befehl)
        value = parse(antworttext, self.aufgaben[0].parsing_befehl)
        return value
      elif(art == "underline_task"):
        return self.underline_aufgaben[version].loesen(antworttext)
      elif(art == "enaktiv"):
        return self.enaktiv[version].loesen(antworttext)
      else: 
        print("Unbekanntes Aufgabenformat!")
        print(art)
        exit(-1)
        
        
    def translate_index(self, str):
      if(str == "0"): return 0  
      elif(str == "1"): return 1  
      elif(str == "2"): return 2  
      elif(str == "3"): return 3  
      elif(str == "4"): return 4  
      elif(str == "5"): return 5  
      elif(str == "6"): return 6  
      elif(str == "7"): return 7  
      elif(str == "8"): return 8  
      elif(str == "9"): return 9  
      elif(str == "10"): return 10  
      elif(str == ""): return None
      else: 
        print("Multiple-Choice Quiz has too many answers!")
        print(str)
        exit(-1)