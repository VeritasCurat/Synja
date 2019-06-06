'''
Created on 22.01.2019
@author: Johannes

@summary: 
- liest darstellungsarten, testaufgaben, und fehlerbeschreibungen, -hinweise (parser) mit parse_... ein. 
  erlaubt umwandlung und formatierung von darstellungsarten, testaufgaben, und fehlerbeschreibungen, -hinweise in Strings mit zugriff_...
  Aufgabenloesungen werden bewerten_... bewertet (Aufgabe an Syntaxkonzept weitergereicht)
'''
import os
import sys
import io
sys.path.append(os.path.abspath('../lehre'))

from Syntaxkonzept import Syntaxkonzept  #@Unresolvedimport
from Lueckentext import Lueckentext #@Unresolvedimport
from MultipleChoice import MultipleChoice #@Unresolvedimport
from Aufgabe import Aufgabe #@Unresolvedimport
from Enaktiv import Enaktiv #@Unresolvedimport
from javaparsing.javaparser import parse #@Unresolvedimport
from javaparsing.javaparser import allreturns  #@Unresolvedimport
from Example import Example #@Unresolvedimport

import re

verzeichnispfad = os.path.realpath(__file__)

class Themenblock(object):
  #Ein Themenblock ist eine Sammlung zusammengehoeriger Syntaxkonzepte
  syntaxkonzepte = {}
  blockname = ""
  
  def __init__(self, name):
    self.blockname = str(name)
    self.syntaxkonzepte = {}
  
    
  def erklaerung_hinzufuegen(self, konzept, erklaerung):
    if(konzept not in self.syntaxkonzepte.keys()):
      self.syntaxkonzepte[str(konzept)] = Syntaxkonzept(str(konzept))
    self.syntaxkonzepte[str(konzept)].darstellung_symbolisch.append(erklaerung)
    
  def example_hinzufuegen(self, konzept, example):
    #print("name: "+str(example.name))
    #print("konzept: "+example.problemstellung)
    #print("erklaerung: "+example.loesung)
    if(konzept not in self.syntaxkonzepte.keys()):
      self.syntaxkonzepte[str(konzept)] = Syntaxkonzept(str(konzept))
    self.syntaxkonzepte[str(konzept)].examples.append(example) 
    #print(self.syntaxkonzepte[str(konzept)].examples[0].name+":"+self.syntaxkonzepte[str(konzept)].examples[0].problemstellung)

      
  def mc_hinzufuegen(self, konzept, mc):
    if(konzept not in self.syntaxkonzepte.keys()):
      print("nicht vorhanden mc: "+konzept)
      exit(-1)
    self.syntaxkonzepte[konzept].test_mc.append(mc)
    
  def lt_hinzufuegen(self, konzept, lt):
    if(konzept not in self.syntaxkonzepte.keys()):
      print("nicht vorhanden lt: "+konzept)
      exit(-1)
    self.syntaxkonzepte[konzept].test_lt.append(lt) 
    
  def aufg_hinzufuegen(self, konzept, aufg):
    if(konzept not in self.syntaxkonzepte.keys()):
      print(self.syntaxkonzepte.keys())
      print("nicht vorhanden aufgabe: "+konzept)
      exit(-1)
    #print(aufg.parsing_befehl)
    self.syntaxkonzepte[konzept].aufgaben.append(aufg)  
    
  def enakt_hinzufuegen(self, konzept, neu):
    #print(neu.konzept+" "+str(neu.schritte_beispiele))
    if(konzept not in self.syntaxkonzepte.keys()):
      print("nicht vorhanden enaktv: "+konzept)
      exit(-1)
    self.syntaxkonzepte[konzept].enaktiv.append(neu)
    
  def undtask_hinzufuegen(self, konzept, aufg):  
    if(konzept not in self.syntaxkonzepte.keys()):
      print("nicht vorhanden undtask: "+konzept)
      exit(-1)
    self.syntaxkonzepte[konzept].underline_aufgaben.append(aufg)
    
    
class ExpertenmodellDE(object):
   
    sprache = ""
    lessons = {} #dict: name -> themenblock
    
    #datenstrukturen die fuer lehrmanager bereitgestellt werden, damit dieser unabhaengig vom em arbeiten kann
    lessoninhalte = {} #dict: lessonname -> liste syntaxkonzepte
    anzahl_erklaerungen = {}
    anzahl_mc = {}
    anzahl_lt = {}
    anzahlWE = {}
    anzahlAufg = {}
    anzahlEnaktiv = {}
    anzahlUndTask = {}
    en_schritt_dict = {} #wieviele beispiele, schritte hat eine enaktiv aufgabe?
    enaktiv_artdict = {} #konzept -> {schritt_loesung,beispiel}
    
    pfad_bilder = "quellen"
    
    intros = {} #lesson -> intro

    hinweise = {} 
    fehlerbeschreibungen = {}
    fehlerreaktionen = {}
    fehlerhinweise = {}

    def __init__(self):
        self.parsen_sym()
        self.parsen_mc()
        self.parsen_lt()
        self.parsen_example()
        self.parsen_aufg()
        self.parsen_enaktiv()
               
        self.parsen_fehlerbeschreibung()
        self.parsen_fehlerreaktion()
        self.parsen_fehlerhinweise()
        #dict fuer
        
        
    def parsen_sym(self):  
      path = os.path.join(os.path.dirname(verzeichnispfad), 'quellen','de', 'symbolisch_de.txt')
      file = io.open(path,'r',encoding='utf-8')#, encoding ='ISO-8859-1'
      tb_name = ""
      while(True):
        line = file.readline()
        if(line==""):break
        if(line.startswith('#')):continue
        #neuer Eintrag
        if(line.startswith('\"')):            
          pattern = r":::"
          data = re.split(pattern, line)
          if(data[0] != None):
            matchname = data[0][1:-1]
          if(data[1] != None):
            matchbeschreibung = data[1][1:-2]
          if(matchname != None and matchbeschreibung != None):
            self.lessons[tb_name].erklaerung_hinzufuegen(matchname, matchbeschreibung)
            if(matchname not in self.lessoninhalte[tb_name]):
              self.lessoninhalte[tb_name].append(matchname)
              self.anzahl_erklaerungen[matchname] = 0       
              self.anzahl_lt[matchname] = 0                
              self.anzahl_mc[matchname] = 0                
              self.anzahlWE[matchname] = 0  
              self.anzahlAufg[matchname] = 0  
              self.anzahlEnaktiv[matchname] = 0  
              self.anzahlUndTask[matchname] = 0  
            self.anzahl_erklaerungen[matchname] += 1     
        else: 
          split = re.split(":", line)
          tb_name = split[1][1:-1]   
          tb_name = tb_name.replace('\r', '')   
          if(tb_name not in [self.lessons.keys()]):
            self.lessons[tb_name] = Themenblock(str(tb_name))  
            self.lessoninhalte[tb_name] = []       
      file.close()                     
      return   
    
    
    def parsen_example(self): 
      path = os.path.join(os.path.dirname(verzeichnispfad), 'quellen','de', 'example_de.txt')
      file = io.open(path,'r',encoding='utf-8')
      tb_name = ""
      while(True):
        line = file.readline()
        if(line==""):break
        if(line.startswith('#')):continue
        #neuer Eintrag
        if(line.startswith('\"')):            
          pattern = r":::"
          data = re.split(pattern, line)
          if(data[0] != None):
            konzept = data[0][1:-1]
          if(data[1] != None):
            problembeschreibung = data[1][1:-2]
          if(data[2] != None):
            loesung = data[2][1:-2]  
          if(konzept != None and problembeschreibung != None and loesung != None):
            neu = Example(konzept, problembeschreibung, loesung)
            #print("example: ("+str(tb_name)+"): konzept")
            self.lessons[tb_name].example_hinzufuegen(konzept, neu)
            self.anzahlWE[konzept] += 1       
        else: 
          split = re.split(":", line)
          tb_name = split[1][1:-1]
          tb_name = tb_name.replace('\r', '')  
          if(tb_name not in self.lessons.keys()):
            print("unbekannter Themenblock ex: "+tb_name+"!")
            print(str(self.lessons.keys()))
            file.close()                     
            exit(-1) 
      file.close()                     
      return 
   
        
    def parsen_lt(self): 
      
      path = os.path.join(os.path.dirname(verzeichnispfad), 'quellen','de','lt_de.txt')
      file = io.open(path,'r',encoding='utf-8')

      tb_name = ""
      while(True):
        line = file.readline()
        if(line==""):break
        if(line.startswith('#')):continue
        if(line.startswith('\"')):            
          pattern = r":::"
          data = re.split(pattern, line)
          if(data[0]!=None):name = data[0][1:-1]
          if(data[1]!=None):aufgabe = data[1][1:-1]
          pattern2 = r"::"
          if(data[2]!=None): lueckentxt = data[2][1:-1]
          while(data[3].startswith(' ')): data[3] = data[3][1:]
          if(data[3]!=None and len(data[3]) > 0):
            loesungen__ = data[3][1:-2]
            loesungen_ = re.split(pattern2, loesungen__)
            for i in range(len(loesungen_)): 
              if(loesungen_[i].startswith('"')): loesungen_[i] = loesungen_[i][1:]
              if(loesungen_[i].endswith('"')): loesungen_[i] = loesungen_[i][:-1]
            #print(loesungen_)
          loesungen = []
          for l in loesungen_: 
            if(l.startswith(" ")): l = l[1:]
            if(l.endswith(" ")): l = l[:-1]
            while(l.count("\"")>2): l = l[1:-1].replace("\"","")
            loesungen.append(l)
          neu = Lueckentext(name, aufgabe, lueckentxt, loesungen)
          #print(name+": "+str(loesungen))
          self.lessons[tb_name].lt_hinzufuegen(name, neu)
          self.anzahl_lt[name] += 1       
        else: 
          split = re.split(":", line)
          tb_name = split[1][1:-1]
          tb_name = tb_name.replace('\r', '')  
          if(tb_name not in self.lessons.keys()):
            print("unbekannter Themenblock lt: "+tb_name+"!")
            print(str(self.lessons.keys()))
            file.close()                     
            exit(-1)            
            #print(list+": "+str(l))
      file.close()                     
      return 
    
    def parsen_mc(self): 
      path = os.path.join(os.path.dirname(verzeichnispfad), 'quellen','de', 'mc_de.txt')
      file = io.open(path,'r',encoding='utf-8')     
      tb_name = ""
      while(True):
        line = file.readline()
        if(line==""):break
        if(line.startswith('#')):continue
        if(line.startswith('\"')): 
          pattern = r":::"
          data = re.split(pattern, line)            
          if(data[0]!=None):name = data[0][1:-1]
          if(data[1]!=None):aufgabenstellung = data[1][1:-1]
          pattern2 = r"::"
          if(data[2]!=None and len(data[2]) > 0):
            aufgabe = re.split(pattern2, data[2][2:-1])
            for a in aufgabe: a = a[1:-1]
          if(data[3]!=None and len(data[3]) > 0):
            while(not data[3].endswith('}')): data[3] = data[3][:-1]
            while(not data[3].startswith('{')): data[3] = data[3][1:]
            loesungen = data[3][1:-1].split(";")
          neu = MultipleChoice(name, aufgabenstellung, aufgabe, loesungen)
          self.anzahl_mc[name]+=1
          self.lessons[tb_name].mc_hinzufuegen(name, neu)
        else: 
          split = re.split(":", line)
          tb_name = split[1][1:-1]
          tb_name = tb_name.replace('\r', '')  
          if(tb_name not in self.lessons.keys()):
            print("unbekannter Themenblock mc: "+tb_name+"!")
            print(str(self.lessons.keys()))
            file.close()                     
            exit(-1)
      file.close()                     
      return 
    
    def parsen_aufg(self): 
      path = os.path.join(os.path.dirname(verzeichnispfad), 'quellen','de', 'aufgaben_de.txt')
      file = io.open(path,'r',encoding='utf-8')   
      tb_name = ""
      while(True):
        line = file.readline()
        if(line==""):break
        if(line.startswith('#')):continue
        elif(line.startswith('\"')): 
          pattern = r":::"
          data = re.split(pattern, line)  
          if(data[0]!=None):konzeptname = data[0][1:-1]
          if(data[1]!=None):aufgstellung = data[1][1:-1]
          patternbefehl1 = r"\$parse .+"
          patternbefehl2 = r"\$multiparse .+"
          patternloesung = r".+"
          loesungsbefehl =""
          loesung = ""
          data[2] = data[2].replace('"','').replace('\n','')
          if(data[2]!=None and re.match(patternbefehl1, data[2]) or re.match(patternbefehl2, data[2])):
            loesungsbefehl = data[2]
          if(data[2]!=None and re.match(patternloesung, data[2])):loesung = data[2][1:-1]
          if("$parse " in loesungsbefehl):
            loesungsbefehl = loesungsbefehl.replace('$parse ','')
            loesungsbefehl = loesungsbefehl.replace(' ','')
          if("$multiparse " in loesungsbefehl):
            loesungsbefehl = loesungsbefehl.replace('$multiparse ','')
          if(len(data) == 4):
            #print(data)
            print("FEHLER PARSE AUFGB")
            file.close()                     
            exit(-1)

          if(len(data) == 3):  
            neu = Aufgabe(aufgstellung, loesungsbefehl, loesung)
            #print(konzeptname)
          self.anzahlAufg[konzeptname]+=1

          self.lessons[tb_name].aufg_hinzufuegen(konzeptname, neu)
        else: 
          split = re.split(":", line)
          tb_name = split[1][1:-1]
          tb_name = tb_name.replace('\r', '')  
          if(tb_name not in self.lessons.keys()):
            print("unbekannter Themenblock aufg: "+tb_name+"!")
            print(str(self.lessons.keys()))
            file.close()                     
            exit(-1)
      file.close()                     
      return 
    
    def parsen_enaktiv(self): 
      path = os.path.join(os.path.dirname(verzeichnispfad), 'quellen','de', 'enaktiv_de.txt')
      file = io.open(path,'r',encoding='utf-8')         
      tb_name = ""
      while(True):
        line = file.readline()
        if(line=="" or line=='\n'):break
        if(line.startswith('#')):continue
        elif(line.startswith('\"')): 
          pattern = r":::"
          data = re.split(pattern, line)  
          typ=""
          if(len(data)==3):
            typ="beispiele"
            if(data[0]!=None):konzeptname = data[0][1:-1]
            if(data[1]!=None):aufgstellung = data[1][1:-1]
            if(data[2]!=None):schritte_beispiele= data[2][1:-2]
            if("::" in schritte_beispiele): schritte_beispiele = schritte_beispiele.split("::")
            else: schritte_beispiele = [schritte_beispiele]
            #for i in range(len(schritte_beispiele)): schritte_beispiele[i] = schritte_beispiele[i][:-1].replace('"','')
          elif(len(data)==4): 
            typ="schritte_loesung" 
            if(data[0]!=None):konzeptname = data[0][1:-1]
            if(data[1]!=None):aufgstellung = data[1][1:-1]
            if(data[2]!=None):loesung = data[2][1:-1]
            if(data[3]!=None):schritte_beispiele= data[3][1:-2]
            if("::" in schritte_beispiele): schritte_beispiele = schritte_beispiele.split("::")
            else: schritte_beispiele = [schritte_beispiele]
          for i in range(len(schritte_beispiele)): 
            while(schritte_beispiele[i].startswith('"')): schritte_beispiele[i] = schritte_beispiele[i][1:] 
            while(schritte_beispiele[i].endswith('"')): schritte_beispiele[i] = schritte_beispiele[i][:-1] 
          
          neu = Enaktiv(konzeptname, aufgstellung, loesung, schritte_beispiele, typ)
          self.en_schritt_dict[konzeptname] = len(schritte_beispiele)
          self.enaktiv_artdict[konzeptname] = typ
          self.anzahlEnaktiv[konzeptname]+=1

          self.lessons[tb_name].enakt_hinzufuegen(konzeptname, neu)
        else: 
          split = re.split(":", line)
          tb_name = split[1][1:-1]
          tb_name = tb_name.replace('\r', '')  
          if(tb_name not in self.lessons.keys()):
            print("unbekannter Themenblock enak: "+tb_name+"!")
            print(str(self.lessons.keys()))
            file.close()                     
            exit(-1)
      file.close()                     
      return 
    
    def parsen_fehlerbeschreibung(self):
      path = os.path.join(os.path.dirname(verzeichnispfad), 'quellen','de', 'fehlerklassifizierung','fehlerbeschreibungen_de.txt')
      file = io.open(path,'r',encoding='utf-8')         
      tb_name = ""
      while(True):
        line = file.readline()
        if(line==""):break
        if(line.startswith('#')):continue
        elif(line.startswith('\"')): 
          pattern = r":::"
          data = re.split(pattern, line)  
          if(data[0]!=None):konzeptname = data[0][1:-1]
          if(data[1]!=None):fehlerart = data[1][1:-1]
          if(data[2]!=None):beschreibung = data[2][1:-2]
          #print(loesungsbefehl+" "+loesung)
          self.fehlerbeschreibungen[fehlerart] = beschreibung
        else:
          split = re.split(":", line)
          tb_name = split[1][1:-1]
          tb_name = tb_name.replace('\r', '')  
          if(tb_name not in self.lessons.keys()):
            print("unbekannter Themenblock fehlerbeschr: "+tb_name+"!")
            print(str(self.lessons.keys()))
            file.close()                     
            exit(-1)
      file.close()                     
      return
    
    def parsen_fehlerhinweise(self):
      path = os.path.join(os.path.dirname(verzeichnispfad), 'quellen','de', 'fehlerklassifizierung','fehlerhinweise_de.txt')
      file = io.open(path,'r',encoding='utf-8')          
      tb_name = ""
      while(True):
        line = file.readline()
        if(line==""):break
        if(line.startswith('#')):continue
        elif(line.startswith('\"')): 
          pattern = r":::"
          data = re.split(pattern, line)  
          if(data[0]!=None):konzeptname = data[0][1:-1]
          if(data[1]!=None):fehlerart = data[1][1:-1]
          if(data[2]!=None):hinweis = data[2][1:-2]
          #print(loesungsbefehl+" "+loesung)
          self.fehlerhinweise[fehlerart] = hinweis
        else:
          split = re.split(":", line)
          tb_name = split[1][1:-1]
          tb_name = tb_name.replace('\r', '')  
          if(tb_name not in self.lessons.keys()):
            print("unbekannter Themenblock fehlerhinweise: "+tb_name+"!")
            print(str(self.lessons.keys()))
            file.close()                     
            exit(-1)
      file.close()                     
      return

    def parsen_fehlerreaktion(self):
      path = os.path.join(os.path.dirname(verzeichnispfad), 'quellen','de', 'fehlerklassifizierung','fehlerreaktionen_de.txt')
      file = io.open(path,'r',encoding='utf-8')          
      tb_name = ""
      while(True):
        line = file.readline()
        if(line.startswith('#')):continue
        elif(line==""):break
        elif(line.startswith('\"')):
          pattern = r":::"
          data = re.split(pattern, line)
          if(data[0]!=None):konzeptname = data[0][1:-1]
          if(data[1]!=None):fehlerart = data[1][1:-1]
          if(data[2]!=None):reaktion = data[2][1:-2]
          #print(loesungsbefehl+" "+loesung)
          self.fehlerreaktionen[fehlerart] = [tb_name,konzeptname,reaktion]
        else:
          split = re.split(":", line)
          tb_name = split[1][1:-1]
          tb_name = tb_name.replace('\r', '')  
          if(tb_name not in self.lessons.keys()):
            print("unbekannter Themenblock fehlerreaktion: "+tb_name+"!")
            print(str(self.lessons.keys()))
            file.close()                     
            exit(-1)
      file.close()                     
      return
      #einlesen example_eng.json
        
    def zugriffLehreinheit(self, lesson, konzept, art, version):    
      #print(str("EM: "+lesson+": "+konzept+": "+art+": "+str(version)))
      #if(str(version) != None): print("Version: "+str(version))
      ausgabe = None
      ausgabetext = ""
      if(art=="symbolisch"):
        if(self.lessons[lesson].syntaxkonzepte[konzept].darstellung_symbolisch == None or  self.lessons[lesson].syntaxkonzepte[konzept].darstellung_symbolisch[version] == None): return "Error: EM: No such file."
        ausgabe = self.lessons[lesson].syntaxkonzepte[konzept].darstellung_symbolisch[version]
        ausgabetext = str(ausgabe)
      elif(art=="ikonisch"):
        if(self.lessons[lesson].syntaxkonzepte[konzept].darstellung_symbolisch == None or  self.lessons[lesson].syntaxkonzepte[konzept].darstellung_symbolisch[version] == None): return "Error: This type of representation does not exist!"
        ausgabe = self.lessons[lesson].syntaxkonzepte[konzept].darstellung_symbolisch[version]
        ausgabetext = lesson+"/"+konzept+".svg"
      elif(art == "enaktiv"):
        if(self.lessons[lesson].syntaxkonzepte[konzept].enaktiv == None or  self.lessons[lesson].syntaxkonzepte[konzept].enaktiv[version] == None): return "Error: EM: No such file."
        ausgabe = self.lessons[lesson].syntaxkonzepte[konzept].enaktiv[version]
        ausgabetext = str(ausgabe.aufgabe)+'\n'+str(ausgabe.aufgabenstellung)
      elif(art=="coding"):
        if(self.lessons[lesson].syntaxkonzepte[konzept].aufgaben == None or  self.lessons[lesson].syntaxkonzepte[konzept].aufgaben[version] == None): return "Error: This type of representation does not exist!."
        ausgabe = self.lessons[lesson].syntaxkonzepte[konzept].aufgaben[version]
        ausgabetext += ausgabe.aufgabenstellung
      elif(art=="test_mc"):
        if(self.lessons[lesson].syntaxkonzepte[konzept].test_mc == None or  self.lessons[lesson].syntaxkonzepte[konzept].test_mc[version] == None): return "No multiple Choice quiz of representation does not exist!"
        ausgabe = self.lessons[lesson].syntaxkonzepte[konzept].test_mc[version]
        ausgabetext = "Please choose the right answer(s) by typing in the number(s) of the answer(s) into user input:\n" + ausgabe.frage + "\n"
        i=1
        for s in ausgabe.antworten: 
          if(i==1):ausgabetext += str(i)+". "+s[:-1] + "\n"
          if(i>1):ausgabetext += str(i)+". "+s[1:-1] + "\n"
          i = i+1
      elif(art=="test_lt"):
        ausgabe = self.lessons[lesson].syntaxkonzepte[konzept].test_lt[version]         
        ausgabetext = ""   
        if(ausgabe.aufgabenstellung != ""):ausgabetext += ausgabe.aufgabenstellung + "\n"
        ausgabetext += "Please fill the gap by typing the answer in Teaching Input:\n"
        ausgabetext += ausgabe.aufgabe
      elif(art=="underline_task"):
        ausgabe = self.lessons[lesson].syntaxkonzepte[konzept].underline_aufgaben[version]         
        ausgabetext = ausgabe.aufgabenstellung
      elif(art=="worked_example"):
        #print("version: "+str(version))
        ausgabe = self.lessons[lesson].syntaxkonzepte[konzept].examples[version]
        ausgabetext = str(ausgabe.problemstellung+"\n "+ausgabe.loesung)
      elif(art == "test_mc_answer"):
        ausgabetext = self.antworten_anzeigen(lesson, konzept, "test_mc", version)
      elif(art == "enaktiv_answer"):
        ausgabetext = self.antworten_anzeigen(lesson, konzept, "enaktiv", version)
      elif(art == "test_lt_answer"):
        ausgabetext = self.antworten_anzeigen(lesson, konzept, "test_lt", version)
      elif(art == "coding_answer"):
        ausgabetext = self.antworten_anzeigen(lesson, konzept, "coding", version)
      elif(art == "underline_task_answer"):
        ausgabetext = self.antworten_anzeigen(lesson, konzept, "underline_task", version)
      else: 
        print("EM: zugriffLehreinheit: unbekannte Format: "+str(art))
        print(art)
        exit(-1)
        
      #fixes
      ausgabetext = ausgabetext.replace('\\n', '\n')
      #print("AUSGABETEXT: "+ausgabetext)
      return ausgabetext
    
    def zugriffEnaktiv_erweiterung(self, lesson, konzept, schritt): 
      erweiterung = ""
      for i in range(schritt+1):
        erweiterung += self.lessons[lesson].syntaxkonzepte[konzept].enaktiv[0].schritte_beispiele[i]+' '
      return erweiterung
    
    def zugriffEnaktiv(self, lesson, konzept, schritt): 
      #print(str(schritt)+" "+str(len(self.lessons[lesson].syntaxkonzepte[konzept].enaktiv[0].schritte_beispiele)))
      if(schritt == -1):
        return self.lessons[lesson].syntaxkonzepte[konzept].enaktiv[0].aufgabenstellung
      elif(schritt < len(self.lessons[lesson].syntaxkonzepte[konzept].enaktiv[0].schritte_beispiele)):
        return self.lessons[lesson].syntaxkonzepte[konzept].enaktiv[0].schritte_beispiele[schritt]
      elif(schritt >= len(self.lessons[lesson].syntaxkonzepte[konzept].enaktiv[0].schritte_beispiele)):       
        return self.lessons[lesson].syntaxkonzepte[konzept].enaktiv[0].loesung
    
    def zugriffHinweis(self, lesson, konzept, fehlerart):    
      #print(str("EM Hinweis:"+lesson+": "+konzept))

      if(fehlerart in self.fehlerhinweise.keys()):
        ausgabetext = self.fehlerhinweise[fehlerart]
      else: 
        #print("EM: zugriffHinweis: unbekannte Format!")
        exit(-1)
        
      #fixes
      ausgabetext = ausgabetext.replace('\\n', '\n')
      #print("AUSGABETEXT: "+ausgabetext)
      return ausgabetext
    
    def zugriffFKantwort(self, lesson, konzept, fehlerbeschreibung):    
      #print(str("EM: "+lesson+": "+konzept+": "+str(fehlerbeschreibung)))
      if(fehlerbeschreibung in self.fehlerbeschreibungen.keys()):
        ausgabetext = self.fehlerbeschreibungen[fehlerbeschreibung]
      else: 
        print("EM: zugriffFKantwort: unbekannte Format!")
        exit(-1)
        
      #fixes
      #ausgabetext = ausgabetext.replace('\\n', '\n')
      #print("AUSGABETEXT: "+ausgabetext)
      return ausgabetext


    def antworten_anzeigen(self, lesson, konzept, art, version): 
      return self.lessons[lesson].syntaxkonzepte[konzept].richtige_anworten(art, version)
      
    def bewerten_enaktiv(self,lesson,konzept,schritt,antworttext):
      bew = self.lessons[lesson].syntaxkonzepte[konzept].bewertung_enaktiv(schritt,antworttext)
      if(bew == True): return "fehlerfrei"
      else: return "fehlerhaft"
      
    def bewerten(self, lesson, konzept, art, version, antworttext): 
      bewertung = self.lessons[lesson].syntaxkonzepte[konzept].bewertung(art, version, antworttext)
      #print("EM: BEW"+str(bewertung))
      if(art == "coding"):
        if(bewertung[0] == True):
          return "fehlerfrei"
        else: 
          reaktion_konzept = self.fehlerreaktionen[bewertung[0]][2]
          reaktion_lesson = "" 
          for l in self.lessons:
            if(reaktion_lesson != ""): break
            for k in self.lessoninhalte[l]:
              if(reaktion_konzept == k): 
                reaktion_lesson = l
                break
          
          fehlerreaktion = [lesson,konzept,reaktion_lesson,reaktion_konzept]
          fehlerbeschr = self.fehlerbeschreibungen[bewertung[0]].replace("$",bewertung[1]).replace('\\n','\n')
          fehlerart = bewertung[0]
          return [fehlerreaktion,fehlerbeschr,fehlerart]
      else:
        if(bewertung == True):
          return "fehlerfrei"
        return "fehlerhaft"
      
    def generate_fehlerbeschreibung(self,fehlerana):
      fehlerbeschreibung = self.fehlerbeschreibungen[fehlerana[0]]
      if("$" in fehlerbeschreibung):
          fehlerbeschreibung = fehlerbeschreibung.replace("$",fehlerana[1])
      return fehlerbeschreibung.replace('\\n','\n')
    





'''
ep = ExpertenmodellDE()
print(ep.bewerten("arrays", "array_reassignment", "coding", 0, "int array[] = new int[3]; array[0] = \"test\";"))
#print(ep.bewerten("basics", "variable_definition", "coding", 0, "int 1a;"))
print("TEST")
print(ep.zugriffHinweis("basics", "comments", "wrong_structure"))
print(str(ep.lessoninhalte.keys()))
print(ep.zugriffEnaktiv("basics", "literals", 0))
print(ep.bewerten_enaktiv("basics", "literals", 0, "test"))
print(ep.zugriffEnaktiv("programm_structure", "programm_structure_main", 0))
print(ep.zugriffEnaktiv("programm_structure", "programm_structure_main", 2))
print(ep.zugriffEnaktiv("programm_structure", "programm_structure_main", 3))
print(ep.zugriffEnaktiv("programm_structure", "programm_structure_main", 4))
print(ep.zugriffEnaktiv("programm_structure", "programm_structure_main", 5))
print(ep.zugriffEnaktiv("programm_structure", "programm_structure_main", 6))
print(ep.zugriffEnaktiv("programm_structure", "programm_structure_main", 7))
print(ep.zugriffEnaktiv("programm_structure", "programm_structure_main", 8))
print(ep.zugriffEnaktiv("programm_structure", "programm_structure_main", 9))
print(ep.zugriffEnaktiv("programm_structure", "programm_structure_main", 10))
'''

#print(ep.bewerten("methods", "method_access", "coding", 0, "void test(){} test();"))
#print(ep.bewerten("operators", "bitwise_operators", "coding", 0, "int a; a<<2"))
#print(ep.zugriffLehreinheit("controll_structures", "for", "test_mc", 0))
#print(ep.antworten_anzeigen("controll_structures", "for", "test_mc", 0))
#print(ep.bewerten("controll_structures", "for", "test_mc", 0, "2,3"))
'''

print(ep.zugriffLehreinheit("controll_structures", "if", "worked_example", 0))
print(str(ep.lessoninhalte["methods"]))

print(ep.bewerten("methods", "method_access", "coding", 0, "void test(){} test();"))

print(ep.bewerten("operators", "bitwise_operators", "coding", 0, "int a; a<<2"))
print(ep.zugriffLehreinheit("controll_structures", "for", "test_mc", 0))
print(ep.antworten_anzeigen("controll_structures", "for", "test_mc", 0))
print(ep.bewerten("controll_structures", "for", "test_mc", 0, "2,3"))
print(ep.zugriffLehreinheit("controll_structures", "if", "worked_example", 0))


'''

