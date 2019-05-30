'''
Created on 22.01.2019

@author: Johannes
'''

import os
import sys
from time import gmtime, strftime

sys.path.append(os.path.abspath('../lehre'))
sys.path.append(os.path.abspath('../webapp'))
import csv




from Nutzer import Nutzer #@Unresolvedimport
from Syntaxkonzept import Syntaxkonzept #@Unresolvedimport
verzeichnispfad = os.path.realpath(os.path.abspath('../webapp'))


class Schuelermodell(object):
    verzeichnispfad = os.path.realpath(__file__)
    '''
    Beschreibt, was der Schueler schon gesehen hat.
    '''
    aktuellerThemenblock =  -1 #aktuelle Lesson (z.B. programm structure)
    aktuellesKonzept = -1 #aktuelles Konzept IN Lesson
    
    lessonliste = [] #z.B. programm structure 
    lessoninhalte = {} #Abbildung: lesson -> [liste lehreinheiten]
    
    bekannteLehrinhalte = []
    bekannteLessons = []
    PreLessonPunkte = {} # [Anzahl der Punkte pro Lesson im Pretest,maximale anzahl punkte]
    PostLessonPunkte = {} # [Anzahl der Punkte pro Lesson im Posttest,maximale anzahl punkte]

    sorted_lessonlist = []    
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
     
    #sortiert liste von lessons nach anzahl der punkte im pretest
    def lessonlist_pretest(self):
      liste = []
      for thema in self.PreLessonPunkte.keys():
        liste.append(thema)
      #bubsort
      unsorted = True
      while(unsorted):
        unsorted = False
        for i in range(len(liste)-1):
          a = self.PreLessonPunkte[liste[i]]
          b = self.PreLessonPunkte[liste[i+1]]
          if((a[0] / a[1]) > (b[0] / b[1])):
            e = liste[i]
            liste[i] = liste[i+1]
            liste[i+1] = e
            unsorted = True
            #print(str(liste))
      self.sorted_lessonlist = []
      self.sorted_lessonlist = liste
        
    def prelessonpunkte_eintragen(self,lesson,punkte,gesamtpunkte):
      self.PreLessonPunkte[lesson] = [punkte,gesamtpunkte]
      
    def postlessonpunkte_eintragen(self,lesson,punkte,gesamtpunkte):
      self.PostLessonPunkte[lesson] = [punkte,gesamtpunkte]
    
    def eintragen_pretest(self,ergebnisse):
      #TODO: in csv datei eintragen
      path = os.path.join(os.path.dirname(verzeichnispfad),'experiment', 'pretest.csv')
      timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

      
      with open(path,'a+') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([timestamp,self.name,ergebnisse])
        
      keylist = list(ergebnisse.keys())

      for i in range(len(ergebnisse.keys())): 
        sum = 0
        for e in ergebnisse[keylist[i]]:
          sum += e
        self.prelessonpunkte_eintragen(keylist[i],int(sum),int(len(ergebnisse[keylist[i]])))
      #print(str(self.PreLessonPunkte))
      self.lessonlist_pretest()
      
    def eintragen_posttest(self,ergebnisse):
      #TODO: in csv datei eintragen
      path = os.path.join(os.path.dirname(verzeichnispfad),'experiment', 'posttest.csv')
      timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

      
      with open(path,'a+') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([timestamp,self.name,ergebnisse])
        
      keylist = list(ergebnisse.keys())

      for i in range(len(ergebnisse.keys())): 
        sum = 0
        for e in ergebnisse[keylist[i]]:
          sum += e
        self.postlessonpunkte_eintragen(keylist[i],int(sum),int(len(ergebnisse[keylist[i]])))
      #print(str(self.PostLessonPunkte))
      
    def __init__(self, lessonliste, lessoninhalte, name):
        #print("neuer Nutzer SM: "+str(name))
        self.name = str(name)
        self.laden()
        existiert = False

        if(existiert==False):
          self.bekannteKonzepte = []
          
        self.lessonliste = lessonliste
        self.lessoninhalte = lessoninhalte    
          
        for thema in self.lessonliste:
          self.PreLessonPunkte[thema] = self.PostLessonPunkte[thema] = 0
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
        self.sorted_lessonlist.remove(lesson)
        self.speichern()
        
    def setName(self, Name):
      self.name = Name
      self.laden()
      
    def neuenNutzerEintragen(self, name): 
      #print("NNE")  
      path = os.path.join(os.path.dirname(self.verzeichnispfad),'nutzerdaten','bekannteLessons.txt')
      file1 = open(path,'w') 
      #with open(self.verzeichnispfad+"lehre\\nutzerdaten\\bekannteLessons.txt", 'a') as file:  
      file1.write('\n'+name+": []")  
      #with open(self.verzeichnispfad+"lehre\\nutzerdaten\\darstellungart_effizenz.txt", 'a') as file:  
      path = os.path.join(os.path.dirname(self.verzeichnispfad), 'nutzerdaten','darstellungart_effizenz.txt')
      file2 = open(path,'w') 
      file2.write('\n'+name+": {}")  

    def speichern(self): 
      for lesson in self.bekannteLessons: 
        if lesson not in self.lessonliste: 
          #print(lesson)
          #print("Could not save state of user: "+self.name)
          return
      
      path = os.path.join(os.path.dirname(self.verzeichnispfad), 'nutzerdaten','bekannteLessons.txt')
      file = open(path,'r')  
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
        
      path = os.path.join(os.path.dirname(self.verzeichnispfad), 'nutzerdaten','darstellungart_effizienz.txt')
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
      path = os.path.join(os.path.dirname(self.verzeichnispfad), 'nutzerdaten','bekannteLessons.txt')
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
   

