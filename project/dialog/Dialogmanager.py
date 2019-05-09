
import os
'''
Der Dialogmanager deckt den Dialog um die Lehre (aber nicht den in der Lehre) ab!
'''

class Dialogmanager(object):
  erkannteIntents = ["name", "verabschiedung", "frage_verstanden", "nicht_verstanden", "weiss_nicht", "gruss", "ja", "nein", "QTeaching", "QDialog", "QTopics"]

  
  zustand = "begruessung"
  gespraechsausgaben = ["begruessung"]
  #gespraechsverlauf = 0
  themenauswahl =  ['programm structure', 'basics', 'operators', 'controll structures', 'methods', 'arrays', 'classes']
  namensregister = []
  
  Name = ""
  neuernutzer = False 
  
  lastPhrase = "begruessung"
  
  def __init__(self, name):

    self.name = name
    self.gespraechsausgaben.append("begruessung")
    #self.laden_namensregister()

    if(self.name not in self.namensregister):
      self.neuernutzer = True
      self.namensregister.append(self.name)
      #print("neuer Nutzer DM: "+self.name)
    return
  
  def setLastPhrase(self):
    if(self.gespraechsausgaben == []): 
      self.lastPhrase = ""
      return
    self.lastPhrase = self.gespraechsausgaben.pop()
    self.gespraechsausgaben.append(self.lastPhrase)
    
  
  def laden_namensregister(self):
    path = os.path.realpath(__file__)[:-23]
    source = "lehre\\nutzerdaten\\bekannteLessons.txt"
    file = open(path+source,'r').read()
    eintraege = file.split('\n')
    for line in eintraege: 
      name = line.split(':')[0]
      self.namensregister.append(name)
    #print(self.namensregister)
        
  def getAusgaben(self):
    self.setLastPhrase()
    ausgaben = self.gespraechsausgaben
    self.gespraechsausgaben = []
    
    return ausgaben
    
  
  def schritt(self, intent, entity):
    if(self.zustand == "lehre"):return
    
    
    #print("DM intent:"+intent+", lp: "+self.lastPhrase)
    self.gespraechsausgaben = []
    #self.gespraechsverlauf.eintragen(self.nutzerid, intent, datetime.now())
    if(not(intent in self.erkannteIntents or entity in self.themenauswahl)): 
      self.gespraechsausgaben.append("nicht_verstanden")
      if(self.lastPhrase != ""):self.gespraechsausgaben.append(self.lastPhrase)
      return self.gespraechsausgaben   
    
    if(str(intent).startswith('Q')):
      self.frage_beantworten(intent)
      if(self.lastPhrase != ""):self.gespraechsausgaben.append(self.lastPhrase)
      return self.gespraechsausgaben   
      
    if(self.zustand == "begruessung"):
        self.begruessung(intent,entity)
    elif(self.zustand == "frage_Name"): 
        self.frage_Name(intent, entity)
    elif(self.zustand == "freude_wiedersehen"): 
        self.freude_wiedersehen(intent)
    elif(self.zustand == "frage_naechsterThemenblock"): 
        self.frage_naechsterThemenblock(intent, entity)
    elif(self.zustand == "frage_verstanden"): 
        self.frage_verstanden(intent)
    #for a in self.gespraechsausgaben: 
    #  self.gespraechsverlauf.eintragen("pa", a, datetime.now())   

    return self.gespraechsausgaben   
  
  def frage_beantworten(self, frage):
    if(frage == "QUI"):
      self.gespraechsausgaben.append("ui")
    if(frage == "QTeaching"):
      self.gespraechsausgaben.append("teaching")
    if(frage == "QDialog"):  
      self.gespraechsausgaben.append("dialog")
  
  
  def begruessung(self, intent, entity):
    if(intent == "name" and entity != ""):
      self.frage_Name(intent, entity)
    elif(intent == "gruss"):  
      if(self.name != ""):  
        if(self.neuernutzer):
          self.gespraechsausgaben.append(["freude_wiedersehen", self.name])
          self.zustand = "freude_wiedersehen"
          self.freude_wiedersehen()
          return
        else: 
          self.gespraechsausgaben.append("einleitung")
          self.zustand = "einleitung"
          self.einleitung()
          return  
      else:
        self.gespraechsausgaben.append("frage_Name")
        self.zustand = "frage_Name"
        return
    else:
      self.gespraechsausgaben.append("keine_passende_antwort")
      self.gespraechsausgaben.append("begruessung")
      self.zustand = "begruessung"
    return
       
  def frage_Name(self, intent, name):
    if(intent != "name" or name == ""): 
      self.gespraechsausgaben.append("keine_passende_antwort")
      self.gespraechsausgaben.append("frage_Name")
      self.zustand = "frage_Name"
      return
    else:
      if(name != ""):
        self.name = name
      if(name in self.namensregister):
        self.gespraechsausgaben.append(["freude_wiedersehen", self.name])
        self.zustand = "freude_wiedersehen"
        self.freude_wiedersehen()
        return
      else: 
        self.gespraechsausgaben.append("einleitung")
        self.zustand = "einleitung"
        self.einleitung()
        return  
    
  def freude_wiedersehen(self):
    self.gespraechsausgaben.append("frage_naechsterThemenblock")
    self.zustand = "frage_naechsterThemenblock"
    return
  
  def einleitung(self):
    self.gespraechsausgaben.append("goal")
    self.gespraechsausgaben.append("teaching")
    self.gespraechsausgaben.append("topics")
    self.gespraechsausgaben.append("ui")
    self.gespraechsausgaben.append("dialog")
    self.gespraechsausgaben.append("frage_naechsterThemenblock")
    self.zustand = "frage_naechsterThemenblock"
    return
  
  def frage_naechsterThemenblock(self, intent, entity):
    if(entity in self.themenauswahl):
      self.zustand = "lehre"
      return
    elif(entity not in self.themenauswahl):
      self.gespraechsausgaben.append("keine_passende_antwort")
      self.gespraechsausgaben.append("frage_naechsterThemenblock")
      return
    elif(intent == "nein"):
      self.gespraechsausgaben.append("verabschiedung")
      self.zustand = "verabschiedung"
      self.verabschiedung("")
    else:
      self.gespraechsausgaben.append("keine_passende_antwort")
      self.zustand = "frage_naechsterThemenblock"
    return
  
  def verabschiedung(self, intent):
    self.gespraechsausgaben.append("verabschiedung")
    self.zustand = "Ende"
