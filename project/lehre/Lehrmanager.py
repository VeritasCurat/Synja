'''
Wie Modell


'''
import random
import os
import sys

sys.path.append(os.path.abspath('../lehre'))

from random import SystemRandom
from Schuelermodell import Schuelermodell
from Expertenmodell import Expertenmodell
from numpy import sort

secure_rand_gen = SystemRandom()
verzeichnispfad = os.path.realpath(__file__)

'''
Anmerkung1: Unterschied zum Modell (Syntaxkonzept) ikonische Erklaerung usw. sind keine echten Zustaende, sondern werden mit der Variable art und wenigen Anpassungen im Code simuliert, um denCode nicht noch laenger zu machen.
'''

'''
  def _init_(self, lesson, konzept, enaktiv_schritt):
    self.lesson = lesson
    self.konzept = konzept
    self.enaktiv_schritt = enaktiv_schritt
'''    
class Enaktivausgabe():
  lesson = ""
  konzept = ""
  schritt = 0
  zustand = "anfang"
  
  def __init__(self, lesson, konzeptname, schritt, zustand):
    self.lesson = lesson
    self.konzept = konzeptname  
    self.schritt = schritt   
    self.zustand = zustand  

class Lehrausgabe():
  lesson = ""
  konzeptname = ""
  darstellungsart = ""
  version = ""
  
  def __init__(self, lesson, konzeptname, darstellungsart, version):
    self.lesson = lesson
    self.konzeptname = konzeptname  
    self.darstellungsart = darstellungsart  
    self.version = version 

class Hinweis():
  lesson = ""
  konzeptname = ""
  fehlerart = ""
  
  def __init__(self, lesson, konzeptname, fehlerart):
    self.lesson = lesson
    self.konzeptname = konzeptname  
    self.fehlerart = fehlerart
    
    
class Fehlerantwort():
  lesson = ""
  konzeptname = ""
  beschreibung = ""
  
  def __init__(self, lesson, konzeptname, beschreibung):
    self.lesson = lesson
    self.konzeptname = konzeptname  
    self.beschreibung = beschreibung  
    


class Lehrmanager:
  erkannteIntents = ["hinweis","unschluessig","dank", "kompliment", "frustration", "beleidigung", "naechsterThemenblock", "fehlerfrei", "fehlerhaft", "name", "verabschiedung", "frage_verstanden", "weiss_nicht", "gruss", "ja", "nein", "QTeaching", "QUI", "QDialog"]
  themenauswahl =  ['programm_structure', 'basics', 'operators', 'statements', 'controll_structures', 'methods', 'arrays', 'classes']

  lessonliste = []
  lessoninhalte = {}# Abbildung: lesson -> [liste lehreinheiten]

  namensregister = []
  
  
  lastPhrase = "begruessung"

  anzahlerklaerungen = {} 
  anzahlWE = {}
  anzahl_lt = {}
  anzahl_mc = {}
  anzahl_cod = {}
  
  schuelermodell = 1
  
  zustand = "begruessung"
  neuernutzer = False 
  name = ""
  #art (symbolisch, ikonisch, enaktiv, example) und version in der der Lehrinhalt praesentiert wird
  art = ""
  artregister = ["symbolisch", "ikonisch", "worked_example","enaktiv"]
  art_counter = 0
  
  version = 0
  versionWE = 0  
  lesson = ""
  konzept = ""
  dialogausgaben = []
  lastPhrase = ""
  lastEmotion = ""
  #lehrausgabe = None
  
  zustand_test = ""
  iterationen_test = 0
  durchlaeufe_test = 3
  punkte_test = 0
  max_punkte_test = 3
  min_punkte_bestehen = 2
  
  fehlerart = ""#wenn nutzer fehler gemacht hat, wird hier der fehler von parser beschrieben
  fehlerbeschreibung = ""
  zustand_fk = "anfang"
  fehlerursache_konzept = ""
  FK_lesson = ""
  FK_konzept = ""
  FK_reaktion_lesson = ""
  FK_reaktion_konzept = ""
  FK_erklaerungspfad = []
  
  emotion = "neutral"
  
  eyeposition = "neutral"
  expected_entry = "dialog"
  highlight = False
  
  responseTimer= 0
  
  zustand_nK=""
  verstandeneKonzepteLesson = 0
  testblockaufg = [] #speichert aufgaben damit diese nicht wiederholt werden
  testblockaufgct = 0 
  
  enaktiv_schritt = 0 #zaehler, bei welchem schritt, beispiel ist enaktiv
  enaktiv_schrittdict = {} #konzept -> anzahl der schritte, beispiele einer enaktiv aufgabe
  enaktiv_artdict = {} #konzept -> {schritt_loesung,beispiel}
  
  def reset_responseTimer(self):
    self.highlight = False
    self.responseTimer = 0
  
  def inc_responseTimer(self):
    if(self.responseTimer > 15):
      self.responseTimer =0
      if(self.expected_entry == "dialog"):
        self.eyeposition = "neutral_dialoginput"
        self.dialogausgaben.append("eingabe_dialog")
        self.emotion = "neutral"
        self.dialogausgaben.append(self.lastPhrase)
      if(self.expected_entry == "lehre"):
        self.eyeposition = "neutral_teachinginput"
        self.dialogausgaben.append("eingabe_lehre")
        self.emotion = "neutral"
        self.dialogausgaben.append(self.lastPhrase)
    else: 
      #print("TEST: "+str(self.responseTimer))
      self.responseTimer += 1

  def __init__(self, name, lehrliste, anzahlerklaerungen, anzahlAufg, anzahlWE, anzahl_lt, anzahl_mc, en_schritt_dict, enaktiv_artdict):
    #print("neuer Nutzer LM: "+str(name))
    self.name = str(name)   
    
    self.dialogausgaben.append("begruessung")
    self.emotion = "freude"
    self.laden_namensregister()

    #if(self.name not in self.namensregister):
    #  self.neuernutzer = True
    #  self.namensregister.append(self.name)
      #print("neuer Nutzer DM: "+self.name)
    self.enaktiv_artdict = enaktiv_artdict
    self.anzahlerklaerungen = anzahlerklaerungen
    self.anzahl_cod = anzahlAufg
    self.anzahlWE = anzahlWE
    self.anzahl_lt = anzahl_lt
    self.anzahl_mc = anzahl_mc
    self.enaktiv_schrittdict = en_schritt_dict
 
    for s in lehrliste.keys():
      self.lessonliste.append(s)
    #print("lessons: "+str(self.lessonliste))  
   
    self.lessoninhalte = lehrliste

    self.schuelermodell = Schuelermodell(self.lessonliste, self.lessoninhalte, self.name)  
    self.schuelermodell.speichern()
    return
  
  def laden_namensregister(self):
    path = os.path.join(os.path.dirname(verzeichnispfad),'nutzerdaten','bekannteLessons.txt')
    file = open(path,'r')

    eintraege = file.read().split('\n')
    file.close()
    for line in eintraege: 
      name = line.split(':')[0]
      self.namensregister.append(name)
    #print(self.namensregister)

  def enumaration(self, list):
    phrase =""
    if(len(list) == 0): return ""
    elif(len(list) == 1): return list[0]
    else: 
      for ind in range(len(list)-2):
        phrase += list[ind]+", "
      phrase += list[-2]+" and "+list[-1]
      return phrase

  #def getLehrAusgaben(self):
  #  ausgaben = self.lehrausgabe
  #  #self.lehrausgabe = None
  #  return ausgaben
  
  def getDialogAusgaben(self):
    self.setLastPhrase()
    ausgaben = self.dialogausgaben
    self.dialogausgaben = []
    return ausgaben
  
  #sortiert self.artregister in absteigender reihenfolge (nach anzahl der erklaerungen in dieser dart)
  def anpassen_dart_reihenfolge(self):
    while(True):
      exchange = False
      for i in [1,2]:
        if(self.schuelermodell.darstellungsart_effizienz[self.artregister[i]] < self.schuelermodell.darstellungsart_effizienz[self.artregister[i+1]]):
          cpy = self.artregister[i]
          self.artregister[i] = self.artregister[i+1]
          self.artregister[i+1] = cpy
          exchange = True
      if(exchange == False):break
      
  def setLastPhrase(self):
    if(self.dialogausgaben == []): 
      self.lastPhrase = ""
      return
    self.lastPhrase = self.dialogausgaben.pop()
    self.dialogausgaben.append(self.lastPhrase)
    
  def emotionalereaktionen(self, intent):
    if(intent == "dank"): return ["dank", "freude"]
    elif(intent == "kompliment"): return ["freude","freude"]  
    elif(intent == "nichtwissen"): return ["ermutigung","freude"] 
    elif(intent == "frustration"): return ["ermutigung","freude"] 
    elif(intent == "beleidigung"): return ["aufhoeren_beleidigung",""] 
    else: return[]
  
  def handle_noreaction(self):
    #print(self.expected_entry)
    if(secure_rand_gen.randint(1, 3) == 1): self.dialogausgaben.append("joke")
    if(self.lastPhrase == "keine_eingabe_lehre" or self.lastPhrase == "keine_eingabe_dialog"):
      self.lastPhrase = ""
    self.dialogausgaben = []
    
    if(self.expected_entry == "lehre"):
      self.dialogausgaben.append("keine_eingabe_lehre")
    elif(self.expected_entry == "dialog"): 
      self.dialogausgaben.append("keine_eingabe_dialog")
    if(self.lastPhrase != ""): self.dialogausgaben.append(self.lastPhrase) 
    #print(len(self.dialogausgaben))
    self.emotion = "neutral"
    
  def schritt(self, intent,entity):
    self.reset_responseTimer()
    #print("LM zustand: "+self.zustand+"; lesson: "+self.lesson+"; intent: "+intent)
    self.dialogausgaben = []
    self.emotion = "neutral"
    
    datareaction = self.emotionalereaktionen(intent) 
    if(datareaction != []):
      self.dialogausgaben.append(datareaction[0])
      self.emotion = datareaction[1]
      if(self.lastPhrase != ""):self.dialogausgaben.append(self.lastPhrase)
      return self.dialogausgaben
    if(intent == "tell_joke"): 
      self.dialogausgaben.append("joke")
      if(self.lastPhrase != ""): self.dialogausgaben.append(self.lastPhrase) 
      self.emotion = "freude"
      return
    if(intent == "profanity"):
      self.dialogausgaben.append("aufhoeren_beleidigung")
      self.emotion = "ernst"
      if(self.lastPhrase != ""): self.dialogausgaben.append(self.lastPhrase) 
      return
    
    elif(not(intent in self.erkannteIntents)): 
      #print("NICHT VERSTANDEN: "+intent)
      self.dialogausgaben.append("nicht_verstanden")
      if(self.lastPhrase != ""): self.dialogausgaben.append(self.lastPhrase) 
      self.emotion = "fragend"
      return self.dialogausgaben   
    
    if(str(intent).startswith('Q')):
      self.frage_beantworten(intent)
      if(self.lastPhrase != ""):self.dialogausgaben.append(self.lastPhrase)
      return self.dialogausgaben
  
    if(self.zustand == "begruessung"):
      self.begruessung(intent,entity)
      self.setLastPhrase()
    elif(self.zustand == "frage_Name"): 
      self.frage_Name(intent, entity)
      self.setLastPhrase()
    elif(self.zustand == "freude_wiedersehen"): 
      self.emotion = "freude"
      self.freude_wiedersehen(intent)
      self.setLastPhrase()
    elif(self.zustand == "frage_naechsterThemenblock"): 
      self.schuelermodell.speichern()
      self.frage_naechsterThemenblock(intent, entity)
      self.setLastPhrase()
      
    elif(self.zustand == "naechsterThemenblock"):
      self.initialisieren_naechsterThemenblock()
    elif(self.zustand == "initialisieren_naechstesKonzept"): 
      self.initialisieren_naechstesKonzept(intent)
      self.setLastPhrase()
      return self.konzept
    elif(self.zustand == "anfang_Konzept"): 
      self.anfang_Konzept()
      self.setLastPhrase()
      return self.konzept
    elif(self.zustand == "konzeptbeschreibung"):
      self.konzeptbeschreibung()
      self.setLastPhrase()
      return self.konzept
    elif(self.zustand == "konzeptbeschreibung_enaktiv"):
      self.konzeptbeschreibung_enaktiv(intent)
      self.setLastPhrase()
      return self.konzept
    elif(self.zustand == "frage_Konzeptverstanden"):
      self.frage_Konzeptverstanden(intent)
      self.setLastPhrase()
      return self.konzept
    elif(self.zustand == "wechsel_erklaerung"):
      self.wechsel_erklaerung()
      self.setLastPhrase()
      return self.konzept
    elif(self.zustand == "keine_Erklaerungen"):
      self.keine_Erklaerungen(intent)
      self.setLastPhrase()
      return self.konzept 
    elif(self.zustand == "testphase_konzept"):
      self.testphase_konzept(intent)
      self.setLastPhrase()
      return self.konzept 
    elif(self.zustand == "testphase_block"):
      self.testphase_block(intent)
      self.setLastPhrase()
      return self.konzept   
    elif(self.zustand == "fehlerklassifizierung"):
      self.fehlerklassifizierung(intent)
      self.setLastPhrase()
      return self.konzept
    
      
      
  def speichern(self):
    self.schuelermodell.speichern()
    return  
 
  def frage_beantworten(self, frage):
    if(frage == "QUI"):
      self.dialogausgaben.append("ui")
      self.emotion = "neutral"
    if(frage == "QTeaching"):
      self.dialogausgaben.append("teaching")
      self.emotion = "neutral"
    if(frage == "QDialog"):  
      self.dialogausgaben.append("dialog")
      self.emotion = "neutral"
        
  def begruessung(self, intent, entity):
    if(intent == "name" and entity != ""):
      self.expected_entry = "dialog"
      self.frage_Name(intent, entity)
    elif(intent == "gruss"):  
      if(self.name != ""):  
        if(self.neuernutzer==False):
          self.expected_entry = "dialog"
          self.dialogausgaben.append(["freude_wiedersehen", self.name])
          self.emotion = "freude"
          self.zustand = "freude_wiedersehen"
          self.freude_wiedersehen()
          return
        elif(self.neuernutzer==True): 
          self.expected_entry = "dialog"
          self.dialogausgaben.append("einleitung")
          self.emotion = "neutral"
          self.zustand = "einleitung"
          self.einleitung()
          return  
      else:
        self.expected_entry = "dialog"
        self.dialogausgaben.append("frage_Name")
        self.emotion = "neutral"
        self.zustand = "frage_Name"
        return
    else:
      self.expected_entry = "dialog"
      self.dialogausgaben.append("keine_passende_antwort")
      self.dialogausgaben.append("begruessung")
      self.emotion = "freude"
      self.zustand = "begruessung"
    return
       
  def frage_Name(self, intent, name):
    if(intent != "name" or name == ""): 
      self.expected_entry = "dialog"
      self.dialogausgaben.append("keine_passende_antwort")
      self.emotion = "fragend"
      self.dialogausgaben.append("frage_Name")
      self.zustand = "frage_Name"
      return
    else:
      if(name != ""):
        self.name = name
      if(self.neuernutzer==False):
        self.expected_entry = "dialog"
        self.dialogausgaben.append(["freude_wiedersehen", self.name])
        self.zustand = "freude_wiedersehen"
        self.emotion = "freude"
        self.freude_wiedersehen()
        return
      else: 
        self.expected_entry = "dialog"
        self.dialogausgaben.append("einleitung")
        self.zustand = "einleitung"
        self.emotion = "neutral"
        self.einleitung()
        return  
    
  def freude_wiedersehen(self):
    self.schuelermodell.speichern()
    self.expected_entry = "dialog"
    self.dialogausgaben.append("frage_naechsterThemenblock")
    self.emotion = "neutral"
    #if(len(self.schuelermodell.bekannteLessons)>0):self.dialogausgaben.append(["schueler_wissen",self.enumaration(self.schuelermodell.bekannteLessons).replace('_',' ')])
    self.zustand = "frage_naechsterThemenblock"
    return
  
  def einleitung(self):
    #self.dialogausgaben.append("why_java1")
    #self.dialogausgaben.append("why_java2")
    #self.dialogausgaben.append("why_java3")
    #self.dialogausgaben.append("why_synja")
    #self.dialogausgaben.append("goal")
    self.dialogausgaben.append("teaching")
    self.dialogausgaben.append("ui")
    self.dialogausgaben.append("dialog")
    self.schuelermodell.speichern()
    self.expected_entry = "dialog"
    self.dialogausgaben.append("frage_naechsterThemenblock")
    self.emotion = "neutral"
    #if(len(self.schuelermodell.bekannteLessons)>0):self.dialogausgaben.append(["schueler_wissen",self.enumaration(self.schuelermodell.bekannteLessons).replace('_',' ')])
    self.zustand = "frage_naechsterThemenblock"
    return
  
  def frage_naechsterThemenblock(self, intent, entity):
    entity = entity.replace(" ","_")
    if(entity in self.themenauswahl):
      self.lesson = entity
      self.initialisieren_naechsterThemenblock()
      return
    elif(entity not in self.themenauswahl):
      self.expected_entry = "dialog"
      self.dialogausgaben.append("keine_passende_antwort")
      self.dialogausgaben.append("frage_naechsterThemenblock")
      self.emotion = "neutral"
      #if(len(self.schuelermodell.bekannteLessons)>0):self.dialogausgaben.append(["schueler_wissen",self.enumaration(self.schuelermodell.bekannteLessons).replace('_',' ')])
      return
    elif(intent == "nein"):
      self.expected_entry = "dialog"
      self.dialogausgaben.append("verabschiedung")
      self.emotion = "freude"
      self.zustand = "verabschiedung"
      self.verabschiedung()
    else:
      self.expected_entry = "dialog"
      self.dialogausgaben.append("keine_passende_antwort")
      self.emotion = "fragend"
      self.dialogausgaben.append("frage_naechsterThemenblock")
      #if(len(self.schuelermodell.bekannteLessons)>0):self.dialogausgaben.append(["schueler_wissen",self.enumaration(self.schuelermodell.bekannteLessons).replace('_',' ')])
    return
  
  def verabschiedung(self):
    self.dialogausgaben.append("verabschiedung")
    self.zustand = "ENDE"
           
  
  def initialisieren_naechsterThemenblock(self):
    #TODO
    self.art = "symbolisch"
    self.art_counter = 0
    self.verstandeneKonzepteLesson = 0
    #self.konzeptname = self.schuelermodell.min_nichtwissen()
    
    #linearer Ablauf
      #self.schuelermodell.aktuellerThemenblock = self.schuelermodell.aktuellerThemenblock+1
      #self.lesson = self.lessonliste[self.schuelermodell.aktuellerThemenblock]
    #nutzerwahl
    self.schuelermodell.aktuellesKonzept = -1
    
    if self.lesson == "programm_structure": self.dialogausgaben.append("programm_structure")
    elif self.lesson == "basics": 
      self.dialogausgaben.append("basics")
      self.dialogausgaben.append("bases_einleitung")
    elif self.lesson == "operators": self.dialogausgaben.append("operators")
    elif self.lesson == "statements": self.dialogausgaben.append("statements")
    elif self.lesson == "controll_structures": self.dialogausgaben.append("controll_structures")
    elif self.lesson == "methods": self.dialogausgaben.append("methods")
    elif self.lesson == "arrays": self.dialogausgaben.append("arrays")
    elif self.lesson == "classes": 
      self.dialogausgaben.append("classes")
      self.dialogausgaben.append("oop_einleitung")
    else: 
      print("unbekannte Lesson!")
      exit(-1)
    self.emotion = "neutral"
    self.initialisieren_naechstesKonzept("")
        
  def initialisieren_naechstesKonzept(self,intent):
    self.expected_entry = "dialog"
    #print("init Konzept")
    self.art_counter = 0
    self.art = self.artregister[self.art_counter]
    
    #print("LM: inK: "+str(self.schuelermodell.aktuellesKonzept)+" / "+str(len(self.lessoninhalte[self.lesson])-1))
    if(self.schuelermodell.aktuellesKonzept < len(self.lessoninhalte[self.lesson])-1):
      self.schuelermodell.aktuellesKonzept = self.schuelermodell.aktuellesKonzept + 1
      self.konzept = self.lessoninhalte[self.lesson][self.schuelermodell.aktuellesKonzept]
      #print("LM naechstes Konzept: "+self.konzept)
      self.version = self.versionWE = 0
      self.anfang_Konzept()
    else:
      #print("LM: TESTPHASE\n")
      self.zustand_nK = ""
      '''
      if(self.verstandeneKonzepteLesson < int(0.5*len(self.lessoninhalte[self.lesson]))):
        self.dialogausgaben.append("testphase_themenblock_nicht_genug")
        self.dialogausgaben.append("frage_naechsterThemenblock")
        self.zustand = "frage_naechsterThemenblock"
      else:
      '''
      self.zustand_test = "start"
      self.durchlaeufe_test = self.max_punkte_test = 3
      self.dialogausgaben.append("testphase_themenblock")
      #self.emotion = "neutral"
      self.zustand = "testphase_block"
      self.testblockaufg = []
      self.testblockaufgct = 0 
      self.testphase_block("")
    return 

  def anfang_Konzept(self):
    self.expected_entry = "dialog"
    self.dialogausgaben.append(["lehrinhalt",self.konzept])
    self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, self.art, self.version))
    #self.emotion = "neutral"
    #print("LM: LEHRINHALT: "+self.konzept)
    self.zustand = "konzeptbeschreibung"
    self.art = self.artregister[++self.art_counter]
    return self.konzeptbeschreibung()   
    
  def konzeptbeschreibung(self):
    self.expected_entry = "dialog"
    self.dialogausgaben.append(["frage_verstanden",self.konzept])
    #self.emotion = "neutral"
    self.zustand = "frage_Konzeptverstanden"
    return
    
  def konzeptbeschreibung_enaktiv(self, intent):
    #fuehrt einen Test durch, wertet diesen aus und reagiert auf Ergebnis (neu erklaeren oder naechstes Konzept)
    #print("KONZEPT_EN "+self.konzept+" "+self.zustand_test+" "+intent+" "+str(self.enaktiv_schritt)+" "+self.expected_entry)
    #print("KONZEPT_EN "+self.enaktiv_artdict[self.konzept])
    if(self.zustand_test == "start"):
      self.enaktiv_schritt = -1
      if(self.enaktiv_artdict[self.konzept]=="schritte_loesung"):self.dialogausgaben.append(Enaktivausgabe(self.lesson, self.konzept, self.enaktiv_schritt, "enaktiv_introduction_schritte"))
      elif(self.enaktiv_artdict[self.konzept]=="beispiele"):self.dialogausgaben.append(Enaktivausgabe(self.lesson, self.konzept, self.enaktiv_schritt, "enaktiv_introduction_beispiele"))
      self.dialogausgaben.append(Enaktivausgabe(self.lesson, self.konzept, self.enaktiv_schritt, "anfang"))
      self.enaktiv_schritt += 1
      if(self.enaktiv_artdict[self.konzept]=="schritte_loesung"):self.dialogausgaben.append(Enaktivausgabe(self.lesson, self.konzept, self.enaktiv_schritt, "schritt"))
      elif(self.enaktiv_artdict[self.konzept]=="beispiele"):self.dialogausgaben.append(Enaktivausgabe(self.lesson, self.konzept, self.enaktiv_schritt, "beispiel"))
      self.emotion = "neutral"
      self.art = "enaktiv"
      self.expected_entry = "lehre"  
      self.zustand_test = "loesung"
      return
    elif(self.zustand_test == "loesung"):
      if(intent == "nein" or intent == "weiss_nicht"):
        self.enaktiv_schritt=-1       
        self.expected_entry = "dialog"
        self.dialogausgaben.append("wechsel_erklaerung")
        self.emotion = "neutral"
        self.zustand_test="start"
        self.zustand = "frage_Konzeptverstanden"      
        self.wechsel_erklaerung()
        return
      bewertung = intent
      if(bewertung == "fehlerfrei"):
        if(self.enaktiv_artdict[self.konzept]=="schritte_loesung"):self.dialogausgaben.append(Enaktivausgabe(self.lesson, self.konzept, self.enaktiv_schritt, "erweiterung"))
        elif(self.enaktiv_artdict[self.konzept]=="beispiele"):self.dialogausgaben.append("freude_antwort")
        self.enaktiv_schritt += 1
        if(self.enaktiv_schritt >= self.enaktiv_schrittdict[self.konzept]):
          self.zustand_test = "ende"
          self.konzeptbeschreibung_enaktiv("")

      if(self.zustand_test == "loesung"):
        if(self.enaktiv_artdict[self.konzept]=="schritte_loesung"):self.dialogausgaben.append(Enaktivausgabe(self.lesson, self.konzept, self.enaktiv_schritt, "schritt"))
        elif(self.enaktiv_artdict[self.konzept]=="beispiele"):self.dialogausgaben.append(Enaktivausgabe(self.lesson, self.konzept, self.enaktiv_schritt, "beispiel"))
        self.expected_entry = "lehre"  
        self.zustand_test = "loesung"   
      self.emotion = "neutral"
      self.art = "enaktiv"
      return
    elif(self.zustand_test == "ende"):
      self.enaktiv_schritt=-1
      self.dialogausgaben.append(Enaktivausgabe(self.lesson, self.konzept, self.enaktiv_schritt, "ende"))
      self.expected_entry = "dialog"
      self.dialogausgaben.append(["frage_verstanden",self.konzept])
      self.emotion = "freude"     
      self.zustand_test="start"
      self.zustand = "frage_Konzeptverstanden"      
      return
                   
  def frage_Konzeptverstanden(self, intent):  
    #abfrage ob das Konzept verstanden wurde; wenn ja: test, wenn nein: wechsel der Erklaerung
    if(intent == "ja" or intent=="verstanden"):
      self.emotion = "freude"
      self.expected_entry = "dialog"
      self.dialogausgaben.append("freude_verstanden")
      self.dialogausgaben.append("testphase_konzept")
      self.zustand = "testphase_konzept"
      self.zustand_test = "start"
      self.testphase_konzept("")
    elif(intent == "nein" or intent=="weiss_nicht"):
      self.expected_entry = "dialog"
      self.dialogausgaben.append("wechsel_erklaerung")
      self.zustand = "wechsel_erklaerung"
      self.emotion = "neutral"
      self.wechsel_erklaerung()
      return
    else:
      self.expected_entry = "dialog"
      self.dialogausgaben.append("keine_passende_antwort")
      self.emotion = "fragend"
      self.dialogausgaben.append(["frage_verstanden",self.konzept])
      self.zustand = "frage_Konzeptverstanden"
    return
    
  
  def wechsel_erklaerung(self):
    #print("wechsel: "+str(self.art_counter)+" "+self.art)   
    if(self.art_counter >= 3):    
      self.zustand = "keine_Erklaerungen"
      self.expected_entry = "dialog"
      self.dialogausgaben.append("keine_Erklaerungen_OLD")
      self.emotion = "neutral"
      return
   
    self.art_counter = (self.art_counter + 1)
    self.art = self.artregister[self.art_counter]
       
    if(self.art == "enaktiv"):
      self.zustand = "konzeptbeschreibung_enaktiv"
      self.zustand_test = "start"
      self.konzeptbeschreibung_enaktiv("")
    else:
      if(self.art == "ikonisch"): 
        self.dialogausgaben.append(["ikonisch",self.konzept])
      elif(self.art == "worked_example"): 
        self.dialogausgaben.append(["worked_example", self.konzept])
      self.zustand = "konzeptbeschreibung"
      self.dialogausgaben.append((Lehrausgabe(self.lesson, self.konzept, self.art, self.version)))
      self.emotion = "neutral"
      self.konzeptbeschreibung()
      return
    return
     
  def keine_Erklaerungen(self, intent):
    if(intent == "ja"):
      self.initialisieren_naechstesKonzept("")
    elif(intent == "nein"):
      self.art_counter = 0
      self.art = self.artregister[self.art_counter]
      self.konzept = self.lessoninhalte[self.lesson][self.schuelermodell.aktuellesKonzept]
      self.version = self.versionWE = 0
      self.anfang_Konzept()
    else:
      self.dialogausgaben.append("keine_passende_antwort")
      self.emotion = "fragend"
      self.zustand = "keine_Erklaerungen"
      self.dialogausgaben.append("keine_Erklaerungen")
 
     
  def testphase_konzept(self, intent):
    #fuehrt einen Test durch, wertet diesen aus und reagiert auf Ergebnis (neu erklaeren oder naechstes Konzept)
    if(self.zustand_test == "start"):
      #print("LM TK: "+str(self.anzahl_cod[self.konzept]))
      if(self.anzahl_cod[self.konzept] > 0):
        #print("LM coding")
        self.art = "coding"
        self.expected_entry = "lehre"
        self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, self.art, self.version))
        #self.emotion = "neutral"
      else:
        print("LM kein Coding TEST fuer: "+self.konzept)
        exit(-1)
      self.zustand_test = "loesung"
      return
    if(self.zustand_test == "loesung"):
      bewertung = intent
      if(bewertung == "fehlerfrei"):
        self.zustand_test = "start"
        self.dialogausgaben.append("freude_antwort")
        self.emotion = "freude"
        #self.lehrausgabe = None
        self.verstandeneKonzepteLesson += 1
        self.schuelermodell.darstellungsart_effizienz[self.artregister[self.art_counter]] +=1
        self.anpassen_dart_reihenfolge()
        self.initialisieren_naechstesKonzept("")
      elif(bewertung == "fehlerhaft"):
        self.expected_entry = "dialog"
        self.dialogausgaben.append("entaeuschung_antwort")
        self.emotion = "neutral"
        #self.dialogausgaben.append(Fehlerantwort(self.lesson, self.konzept, self.fehlerbeschreibung))
        self.zustand = "fehlerklassifizierung"
        self.zustand_fk = "anfang"
        self.fehlerklassifizierung("")
      elif(bewertung == "unschluessig"):
        self.expected_entry = "lehre"
        self.dialogausgaben.append("todo_testphasekonzept_loesung")
        self.highlight = True
        self.emotion = "neutral"
        self.zustand = "testphase_konzept"
      elif(bewertung == "hinweis"):
        self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, "symbolisch", self.version))
        self.dialogausgaben.append("testphase_konzept")
        self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, self.art, self.version))
        self.highlight = True
        self.emotion = "neutral"
        self.zustand = "testphase_konzept"
      else: 
        self.dialogausgaben.append("testphase_konzept")
        self.emotion = "neutral"
        self.zustand = "testphase_konzept"
      return
    if(self.zustand_test == "berichtigung"):
      if(intent == "ja" or intent == "verstanden"):      
        #self.lehrausgabe = None
        self.dialogausgaben.append("wechsel_erklaerung")
        self.emotion = "neutral"
        self.wechsel_erklaerung()
      elif(bewertung == "unschluessig"):
        self.expected_entry = "dialog"
        self.highlight = True
        self.dialogausgaben.append("todo_testphasekonzept_berichtigung")
        self.dialogausgaben.append("richtigeAntwort")
        self.emotion = "neutral"
      else:
        self.dialogausgaben.append("richtigeAntwort")
        self.emotion = "neutral"
 
  def gen_tb_aufg_list(self):
    self.testblockaufg = []
    self.testblockaufgct = -1 
    
    #fuehrt drei Tests durch
    #print("TB: "+str(self.iterationen_test)+" von "+str(self.durchlaeufe_test))
    #print("TB: "+self.zustand_test)
    for i in range(3):
      while(True):
        zufallsart = secure_rand_gen.randint(1, 2)  
        zufallskonzept = self.lessoninhalte[self.lesson][secure_rand_gen.randint(0,len(self.lessoninhalte[self.lesson])-1)]
        neu = True
        for aufg in self.testblockaufg:
          if(zufallskonzept == aufg[0] and zufallsart == aufg[1]):
            neu = False
            break
        if(neu == True):break
      
      self.testblockaufg.append([zufallskonzept,zufallsart])
    
   
  def testphase_block(self, intent):
    #generiere drei tests
    if(self.testblockaufg == []): 
      self.gen_tb_aufg_list()
      #print(self.testblockaufgct)
      #print(self.testblockaufg)
    
    if(self.iterationen_test < self.durchlaeufe_test):  
      if(self.zustand_test == "start"):
        #print(self.testblockaufgct)
        self.testblockaufgct += 1
      
        #print(self.testblockaufg[self.testblockaufgct])
        zufallskonzept = self.testblockaufg[self.testblockaufgct][0]  
        zufallsart = self.testblockaufg[self.testblockaufgct][1]  
        
        self.konzept = zufallskonzept
                 
        self.dialogausgaben.append("nextTask")
        if(zufallsart == 1):
          self.art = "test_mc"
          self.expected_entry = "lehre"
          self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, "test_mc", self.version))
        elif(zufallsart == 2):
          self.art = "test_lt"
          self.expected_entry = "lehre"
          self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, "test_lt", self.version))
                  
       
        #TODO
        #self.schuelermodell.bekannteLehrinhalte.append(self.lehrausgabe) 
        self.emotion = "neutral"
        self.zustand_test = "loesung"
        return
      elif(self.zustand_test == "loesung"):
        bewertung = intent
        if(bewertung == "fehlerfrei"):
          self.iterationen_test =  self.iterationen_test+1
          #print("TB: NAE IT"+str(self.iterationen_test)+" von "+str(self.durchlaeufe_test))
          self.emotion = "freude"
          self.dialogausgaben.append("freude_antwort")
          self.punkte_test = self.punkte_test+1
          self.zustand_test = "start"
          self.testphase_block("")
          return
        elif(bewertung == "fehlerhaft"):
          self.iterationen_test =  self.iterationen_test+1
          #print("TB: NAE IT"+str(self.iterationen_test)+" von "+str(self.durchlaeufe_test))
          self.dialogausgaben.append("entaeuschung_antwort")
          self.dialogausgaben.append("richtigeAntwort")
          self.expected_entry = "lehre"
          self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, self.art+"_answer", self.version))
          self.emotion = "neutral"
          self.zustand_test = "start"
          return
        elif(bewertung == "no" or bewertung=="weiss_nicht"):
          self.iterationen_test =  self.iterationen_test+1
          #print("TB: NAE IT"+str(self.iterationen_test)+" von "+str(self.durchlaeufe_test))
          self.dialogausgaben.append("entaeuschung_antwort")
          self.dialogausgaben.append("richtigeAntwort")
          self.expected_entry = "lehre"
          self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, self.art+"_answer", self.version))
          self.emotion = "neutral"
          self.zustand_test = "start"
          return
        elif(bewertung == "unschluessig"):
          self.expected_entry = "lehre"
          self.highlight = True
          self.dialogausgaben.append("todo_testphasekonzept_loesung")
          self.emotion = "neutral"
          self.zustand = "testphase_konzept"
        elif(bewertung == "hinweis"):
          self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, "symbolisch", self.version))
          self.dialogausgaben.append("testphase_konzept")
          self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, self.art, self.version))
          self.highlight = True
          self.emotion = "neutral"
          self.zustand = "testphase_konzept"
        else: 
          self.dialogausgaben.append("testphase_themenblock")
          self.zustand = "testphase_block"
          self.dialogausgaben.append("nextTask")
          self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, "test_mc", self.version))
          self.emotion = "neutral"
          return
    elif(self.iterationen_test >= self.durchlaeufe_test):
      self.testblockaufg = []
      self.expected_entry = "dialog"
      self.dialogausgaben.append("auswertungTest")
      self.emotion = "neutral"
      self.zustand_test = ""
      self.zustand = "auswertungTest"
      self.auswertungTest()
      #self.lehrausgabe = None
      return
    
    
  def fehlerklassifizierung(self, intent):
    #pa fragt nach konzept; verwendet der schueler bestimmte schluesselworter in erklaerung, kennt er das Konzept => fluechtigkeitsfehler => test
    #sonst: Missverstaednis oder NIchtwissen (schwierig zu erkennen) => wechsel_erklaerung
    #print("LM FK: zustand: "+self.zustand_fk+", intent: "+intent+", fehlerart: "+str(self.fehlerart)+", lesson:"+str(self.FK_reaktion_lesson)+", konzept:"+str(self.FK_reaktion_konzept))
    if(self.zustand_fk == "anfang"):
      if(self.fehlerbeschreibung!="" and self.FK_lesson!="" and self.FK_konzept!="" and self.FK_reaktion_lesson!="" and self.FK_reaktion_konzept!=""):
        self.expected_entry = "lehre"
        self.dialogausgaben.append(Fehlerantwort(self.lesson, self.konzept, self.fehlerbeschreibung))
      
      self.dialogausgaben.append(["aufforderung_schreiben_codeschnipsel", self.FK_reaktion_konzept.replace(self.FK_reaktion_lesson,"").replace('_','')])
      self.art = "coding"
      #self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, self.art, self.version))
      self.dialogausgaben.append("kompetenzfrage_mithinweis")
      self.zustand_fk = "kompetenzfrage"
      
      self.FK_lesson = self.FK_reaktion_lesson
      self.FK_konzept = self.FK_reaktion_konzept
        
    elif(self.zustand_fk == "kompetenzfrage"):
      #print("FK: KF: "+intent)
      if(intent == "weiss_nicht" or intent == "nein" or intent == "hinweis"):
        self.zustand_fk = "frage_hinweis_verstanden"
        self.expected_entry = "dialog"
        self.dialogausgaben.append(Hinweis(self.FK_lesson, self.FK_konzept, self.fehlerart))
        self.dialogausgaben.append("frage_hinweis_verstanden")
        self.emotion = "neutral"
        #self.dialogausgaben.append(Fehlerantwort(self.lesson, self.konzept, "no_idea"))
      elif(intent == "fehlerhaft"):
        #print("LM: FK: BERICHTIGUNG")
        if(self.fehlerbeschreibung!="" and self.FK_lesson!="" and self.FK_konzept!="" and self.FK_reaktion_lesson!="" and self.FK_reaktion_konzept!=""):
          self.expected_entry = "lehre"
          self.dialogausgaben.append(Fehlerantwort(self.FK_lesson, self.FK_konzept, self.fehlerbeschreibung))
      
          self.dialogausgaben.append(["aufforderung_schreiben_codeschnipsel", self.FK_reaktion_konzept.replace(self.FK_reaktion_lesson,"").replace('_','')])
          self.art = "coding"
          #self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, self.art, self.version))
          self.dialogausgaben.append("kompetenzfrage_mithinweis")
          self.zustand_fk = "kompetenzfrage"
          
          self.FK_lesson = self.FK_reaktion_lesson
          self.FK_konzept = self.FK_reaktion_konzept
          
        else:
          print("FEHLER: LM: FK: kompetenzfrage")
        #self.dialogausgaben.append(["berichtigung", "BERICHTIGUNG: "+self.konzept])
      elif(intent == "fehlerfrei"):
        self.expected_entry = "dialog"
        self.dialogausgaben.append("berichtigung_verstanden")
        
        self.FK_konzept = self.FK_lesson = self.FK_reaktion_lesson = self.FK_reaktion_konzept = self.zustand_fk = ""
        self.expected_entry = "dialog"
        self.dialogausgaben.append(["frage_verstanden",self.konzept])
        self.zustand = "frage_Konzeptverstanden"
      elif(intent == "unschluessig"):
        self.art = "coding"
        self.expected_entry = "lehre"
        self.dialogausgaben.append("todo_fehlerklassifikation_kompetenzfrage")
        self.dialogausgaben.append(["aufforderung_schreiben_codeschnipsel", self.FK_konzept.replace(self.FK_lesson,"").replace('_','')])
        self.zustand_fk = "kompetenzfrage"
        self.dialogausgaben.append("kompetenzfrage_mithinweis")
        self.emotion = "neutral"
        return
      else: 
        self.art = "coding"
        self.expected_entry = "lehre"
        self.dialogausgaben.append(["aufforderung_schreiben_codeschnipsel", self.FK_konzept.replace(self.FK_lesson,"").replace('_','')])
        self.zustand_fk = "kompetenzfrage"
        self.dialogausgaben.append("kompetenzfrage_mithinweis")
        self.emotion = "neutral"
        return
    elif(self.zustand_fk == "frage_hinweis_verstanden"):
      if(intent=="ja"):
        self.art = "coding"
        self.expected_entry = "lehre"
        self.dialogausgaben.append(["aufforderung_schreiben_codeschnipsel", self.FK_konzept.replace(self.FK_lesson,"").replace('_','')])
        self.zustand_fk = "kompetenzfrage"
        self.dialogausgaben.append("kompetenzfrage")
        self.emotion = "neutral"
      elif(intent=="nein" or intent=="weiss_nicht"):
        self.zustand_fk = "erklaerung_erfolglos"
        self.FK_konzept = self.FK_lesson = self.FK_reaktion_lesson = self.FK_reaktion_konzept = self.zustand_fk = ""
        self.zustand_fk="anfang"
        self.fehlerart=""
        self.dialogausgaben.append("wechsel_erklaerung")
        self.wechsel_erklaerung()     
      elif(intent == "fehlerhaft"):
        if(self.fehlerbeschreibung!="" and self.FK_lesson!="" and self.FK_konzept!="" and self.FK_reaktion_lesson!="" and self.FK_reaktion_konzept!=""):
          self.expected_entry = "lehre"
          self.dialogausgaben.append(Fehlerantwort(self.FK_lesson, self.FK_konzept, self.fehlerbeschreibung))
      
          self.dialogausgaben.append(["aufforderung_schreiben_codeschnipsel", self.FK_reaktion_konzept.replace(self.FK_reaktion_lesson,"").replace('_','')])
          self.art = "coding"
          #self.dialogausgaben.append(Lehrausgabe(self.lesson, self.konzept, self.art, self.version))
          self.dialogausgaben.append("kompetenzfrage_mithinweis")
          self.zustand_fk = "kompetenzfrage"
          
          self.FK_lesson = self.FK_reaktion_lesson
          self.FK_konzept = self.FK_reaktion_konzept
        else: print("Fehler LM: FK: frage_hinweis_verstanden")
      elif(intent == "fehlerfrei"):
        self.expected_entry = "dialog"
        self.dialogausgaben.append("berichtigung_verstanden")
        
        self.FK_konzept = self.FK_lesson = self.FK_reaktion_lesson = self.FK_reaktion_konzept = self.zustand_fk = ""
        self.expected_entry = "dialog"
        self.dialogausgaben.append(["frage_verstanden",self.konzept])
        self.zustand = "frage_Konzeptverstanden"
    return ""
            
  def auswertungTest(self):
    #print("LM AUSWERTUNG")
    #wertet Test aus und reagiert auf Ergebnis (neu erklaeren oder naechster Themenblock)
    if(self.punkte_test >= self.min_punkte_bestehen):
      #print("Test1")
      self.dialogausgaben.append("Testergebnis_erfolgreich")
      self.dialogausgaben.append("frage_naechsterThemenblock")
      self.emotion = "freude"
      #if(len(self.schuelermodell.bekannteLessons)>0):self.dialogausgaben.append(["schueler_wissen",self.enumaration(self.schuelermodell.bekannteLessons).replace('_',' ')])
      
      self.zustand = "frage_naechsterThemenblock"
      self.schuelermodell.lessonAlsGelerntEintragen(self.lesson)
      self.schuelermodell.speichern()
      #self.lehrausgabe = None
      self.punkte_test = self.iterationen_test = 0
      return
    else:
      self.dialogausgaben.append("Testergebnis_erfolglos")
      self.emotion = "neutral"
      self.dialogausgaben.append("wechsel_erklaerung")
      self.zustand = "initialisieren_naechstesKonzept"
      self.schuelermodell.aktuellesKonzept = -1
      self.punkte_test = self.iterationen_test = 0
      self.schritt("","")
      return
    