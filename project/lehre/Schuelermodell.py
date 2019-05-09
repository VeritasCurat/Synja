'''
Created on 22.01.2019

@author: Johannes
'''
from project.webapp.Nutzer import Nutzer
from project.lehre.Syntaxkonzept import Syntaxkonzept
import os
from project.lehre.Expertenmodell import Expertenmodell

class Schuelermodell(object):
    verzeichnispfad = os.path.realpath(__file__)[:-23]
    '''
    Beschreibt, was der Schueler schon gesehen hat.
    '''
    aktuellerThemenblock =  -1 #aktuelle Lesson (z.B. programm structure)
    aktuellesKonzept = -1 #aktuelles Konzept IN Lesson
    
    lessonliste = [] #z.B. programm structure 
    lessoninhalte = {} #Abbildung: lesson -> [liste lehreinheiten]
    
    bekannteLehrinhalte = []
    bekannteLessons = []

    alleMC = {}
    alleLT = {}    
    alleErklaerungen = {}    
    
    darstellungsart_effizienz = {} #Abbildung: art[String] -> anzahl_erfolg[int]
        
    name = ""

    def enumaration(self, list):
      phrase =""
      if(len(list) == 0): return ""
      elif(len(list) == 1): return list[0]
      else: 
        for ind in range(len(list)-2):
          phrase += list[ind]+","
        phrase += list[-2]+","+list[-1]
        return phrase

    def lehrinhalt_angesehen(self, lehrinhalt):
      self.bekannteLehrinhalte.append(lehrinhalt)
      
    def lehrinhalt_bekannt(self, lehrinhalt):
      if(lehrinhalt in self.bekannteLehrinhalte):
        return True
      else: return False

    def __init__(self, lessonliste, lessoninhalte, name):
        #print("neuer Nutzer SM: "+str(name))
        self.name = str(name)
        #self.laden()
        existiert = False

        if(existiert==False):
          self.bekannteKonzepte = []
          
        self.lessonliste = lessonliste
        self.lessoninhalte = lessoninhalte    
          
        for thema in self.lessonliste:
          for syntaxkonzept in self.lessoninhalte[thema]:
          
            '''  
            self.themenliste.append(Syntaxkonzept(syntaxkonzept).name)
            
            self.bekannteMC[Syntaxkonzept(syntaxkonzept).name] = []
            self.bekannteLT[Syntaxkonzept(syntaxkonzept).name] = []
            self.bekannteErklaerungen[Syntaxkonzept(syntaxkonzept).name] = []
            
            self.alleErklaerungen[Syntaxkonzept(syntaxkonzept).name] = [range(0,len(Syntaxkonzept(syntaxkonzept).darstellung_symbolisch))]
            self.alleLT[Syntaxkonzept(syntaxkonzept).name] = [range(0,len(Syntaxkonzept(syntaxkonzept).test_lt))]
            self.alleMC[Syntaxkonzept(syntaxkonzept).name] = [range(0,len(Syntaxkonzept(syntaxkonzept).test_mc))]
            ''' 
        self.darstellungsart_effizienz['symbolisch'] = 0
        self.darstellungsart_effizienz['ikonisch'] = 0
        self.darstellungsart_effizienz['enaktiv'] = 0
        self.darstellungsart_effizienz['worked_example'] = 0    
            
    def naechsteErklaerung(self, konzept):  
      for erklaerung in self.alleErklaerungen:
        if erklaerung in self.bekannteErklaerungen: continue
        else: 
          ++self.aktuellesKonzept
          return konzept
          
    def naechstesKonzeptLinear(self):
      for konzept in self.themenliste:
        if konzept in self.bekannteKonzepte: continue
        else: 
          ++self.aktuellesKonzept
          return konzept
       
    def lessonSchonBekannt(self, lesson):    
      if(lesson in self.bekannteLessons): return True
      else: return False
        
    def lessonAlsGelerntEintragen(self, lesson):
      if(lesson not in self.bekannteLessons):
        self.bekannteLessons.append(lesson)
        #self.speichern()
        
    def setName(self, Name):
      self.name = Name
      #self.laden()
      
    def neuenNutzerEintragen(self, name): 
      print("NNE")  
      with open(self.verzeichnispfad+"lehre\\nutzerdaten\\bekannteLessons.txt", 'a') as file:  
        file.write('\n'+name+": []")  
      with open(self.verzeichnispfad+"lehre\\nutzerdaten\\darstellungart_effizenz.txt", 'a') as file:  
        file.write('\n'+name+": {}")  

    def speichern(self): 
      for lesson in self.bekannteLessons: 
        if lesson not in self.lessonliste: 
          #print(lesson)
          #print("Could not save state of user: "+self.name)
          return
      
      path = os.path.join(os.path.abspath(self.verzeichnispfad), 'lehre','nutzerdaten','bekannteLessons.txt')
      file = open(path)  
      data = ""
      line = ""
      while(True):
        line = file.readline()
        if(line == None or line == ""): break
        if(self.name in line): 
          line = self.name+": ["
          line += self.enumaration(self.bekannteLessons).replace(' ','').replace('\'','')
          line+="]"
        data += str(line) 
      with open(path,'w') as file:
        file.write(data)
        
      path = os.path.join(os.path.abspath(self.verzeichnispfad), 'lehre','nutzerdaten','darstellungart_effizienz.txt')
      file = open(path)  
      data = ""
      line = ""
      while(True):
        line = file.readline()
        if(line == None or line == ""): break
        if(self.name in line): 
          line = self.name+": ["
          line += str(self.darstellungsart_effizienz)
          line += "]"
        data += str(line) 
      with open(path,'w') as file:
        file.write(data)        
      return
    
    def laden(self): 
      #print("lade schuelermodell")
      path = os.path.join(os.path.abspath(self.verzeichnispfad), 'lehre','nutzerdaten','bekannteLessons.txt')
      file = open(path)  
      line = ""
      neuernutzer = True
      #laden bekannte lessons
      while(True):
        line = file.readline()
        if(line == None or line == ""): break
        if(self.name in line):
          liste = line.split(':')[1][2:-1]
          if(',' in liste):self.bekannteLessons = liste.split(',')
          else: self.bekannteLessons = [liste]
          if('' in self.bekannteLessons):self.bekannteLessons.remove('')
          neuernutzer = False
          break
        
      #laden darstellungsart_effizienz
      self.darstellungsart_effizienz['symbolisch'] = 0
      self.darstellungsart_effizienz['ikonisch'] = 0
      self.darstellungsart_effizienz['enaktiv'] = 0
      self.darstellungsart_effizienz['worked_example'] = 0
      


      if(neuernutzer == True):self.neuenNutzerEintragen(self.name)
      file.close()                     
      return
   
