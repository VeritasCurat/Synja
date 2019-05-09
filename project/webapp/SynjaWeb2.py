'''
Created on 21.01.2019
@author: Johannes Grobelski
@version: 1.0

@summary: Allgemeine Funktionsweise:
- Die Datenstroeme in Synja bestehen hauptsaechlich aus Lehreingaben(Teaching Input(UI)) und Lehrausgaben(Synja) und Dialogeingaben(Dialog Input(UI)) und Dialogausgaben(Synja); diese werden in queues gespeichert
  Dialogausgaben und Lehrausgaben koennen einfache Strings aber auch die zum Datenaustausch im Lehrmanager definierten Objekte (Enaktivausgabe, Lehrausgabe, Hinweis, Fehlerantwort); diese muessen hier vom Expertenmodell zu Strings umgewandelt werden
SynjaWeb 
'''



from project.lehre.Lehrmanager import Lehrmanager, Fehlerantwort, Hinweis, Lehrausgabe
from project.lehre.Expertenmodell import Expertenmodell
 
from project.dialog.Dialogmanager import Dialogmanager
from project.dialog.NLG import NLG
from project.dialog.NLU import NLU
from project.lehre.Lehrmanager import Enaktivausgabe

import threading
import warnings
import time
import queue
from builtins import isinstance
from project.webapp.verlauf import Verlauf


LESEGESCHWINDIGKEIT = 1 #wartezeit nach schreiben von Nachricht
SCHREIBGESCHWINDIGKEIT = 0.05 #sekunde pro zeichen gut: 0.05

writeV = 10000 #wieviele zeichen pro sekunde

lastanswer = 0
class Synja(threading.Thread): 
  
  
  id=0 #used to identify which messages  
  nr=0
  nlg=0
  expertenmodell=Expertenmodell("en")
  dialogmanager=0
  lehrmanager=0
  name=""
  totalCount = 0  
  outputDialog = []
  outputLehre = None
  
  sendqueueDialog = None
  sendqueueDialogZeichen = None
  recvqueueDialog =  None
  sendqueueLehre =  None
  recvqueueLehre =  None  
  coding = False
   
  lastmessages = [] #display the last 10 messages 
  text = ""
  sleeptime = 0
  
  lastmessagetime = int(round(time.time()))
  highlight_input_element = "" #wenn der nutzer laenger nicht geantwortet hat, soll dieses element farblich (rot) hervorgehoben werden
  no_resp_time = 20
  
  verlauf = None
  
  #hauptmethode: hier wird auf die queues gelisten und dann darauf reagiert (lehrmanager)
  def run(self):
    warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

    begruessung = self.nlg.generate("begruessung")
    self.addDialogSynja(begruessung) 
    self.text+=begruessung+'\n'      
  
    while(True):
      listen = self.listen()    
           
      if(isinstance(listen,list) and len(listen)==2):      
        eingabeDialog = listen[0]
        eingabeLehre = listen[1]
      else: continue      
            
      if(eingabeDialog != None and eingabeDialog != ""):
        self.dialogeingabe(eingabeDialog)
      else: self.outputDialog = [] 
      
      if(eingabeLehre != None and eingabeLehre != ""):
        self.lehreingabe(eingabeLehre)
      else: self.outputLehre = None
       
      time.sleep(0.1)  

    
  def dialogeingabe(self, inputUser):
        
    self.schritt(inputUser, "")      
        
    self.tellwithpauses(self.outputDialog)
    
    '''
    if(self.outputLehre != None):
        #print(str(self.outputLehre.darstellungsart))
        self.convertLehreSynjaText(self.outputLehre)
    
    self.outputLehre = None
    self.outputDialog = []  
    '''
    #self.save()
    
  def lehreingabe(self, antworttext):
    if(self.lehrmanager.zustand=="testphase_konzept" or self.lehrmanager.zustand=="testphase_block" or self.lehrmanager.zustand=="konzeptbeschreibung_enaktiv" or self.lehrmanager.zustand=="fehlerklassifizierung"): 
      #Auswertung nameeingabe
      if(self.lehrmanager.FK_lesson != "" and self.lehrmanager.FK_konzept != ""):
        lesson = self.lehrmanager.FK_lesson
        konzeptname = self.lehrmanager.FK_konzept
      else:
        lesson = self.lehrmanager.lesson
        konzeptname = self.lehrmanager.konzept  
      art = self.lehrmanager.art
      version = self.lehrmanager.version
      if(art =="enaktiv"): bewertung = self.em.bewerten_enaktiv(lesson, konzeptname, self.lehrmanager.enaktiv_schritt, antworttext)
      else: 
        bewertung = self.em.bewerten(lesson, konzeptname, art, version, antworttext)
        #self.verlauf.eintragen(id, lesson, konzeptname, art, version, antworttext, bewertung)
      print("bewertung: "+str(bewertung))
      
      if(art == "underline_task"):
        if(bewertung != "fehlerfrei"):
          self.lehrmanager.fehlerbeschreibung = bewertung
          bewertung = "fehlerhaft"
      elif(art == "coding"):
        if(bewertung != "fehlerfrei"):
          print(str(bewertung))
          if(isinstance(bewertung,list) and len(bewertung)==3 and isinstance(bewertung[0],list) and len(bewertung[0])==4 and isinstance(bewertung[1],str)):
            print(str(bewertung))
            self.lehrmanager.FK_lesson = bewertung[0][0]
            self.lehrmanager.FK_konzept = bewertung[0][1]
            self.lehrmanager.FK_reaktion_lesson = bewertung[0][2]
            self.lehrmanager.FK_reaktion_konzept = bewertung[0][3]
            self.lehrmanager.fehlerbeschreibung = bewertung[1]
            self.lehrmanager.fehlerart = bewertung[2]
          bewertung = "fehlerhaft"
         
      self.schritt("",bewertung)
     
      self.tellwithpauses(self.outputDialog)
      
      '''      
      if self.outputLehre!= None: 
        self.convertLehreSynjaText(self.outputLehre)  
      '''  
        
      self.outputDialog = []
      self.outputLehre = None
  
      #self.save()
      
  def tellwithpauses(self, ausgabe):
    if(ausgabe == None or isinstance(ausgabe, list) and len(ausgabe) == 0): return
    elif(len(ausgabe) == 1):self.addDialogSynja(ausgabe[0])
    else:
      for s in ausgabe: 
        #secondswait = len(s) / LESEGESCHWINDIGKEIT
        self.addDialogSynja(s)
        #time.sleep(secondswait)
       
  

  def convertLehreSynjaText(self, lehrausgabe):
    #konzeptname, darstellungsart, version, nameid
    ausgabe = self.em.zugriffLehreinheit(lehrausgabe.lesson, lehrausgabe.konzeptname, lehrausgabe.darstellungsart, lehrausgabe.version)
  
    ausgabetext = ausgabe
    ausgabetext = ausgabetext.replace('\\n', '\n')
    #print("AUSGABETEXT: "+ausgabetext)
     
    self.coding = True
    return str(ausgabetext)
    '''  
    if(lehrausgabe.darstellungsart=="coding"):
      self.tellwithpauses([str(ausgabetext)])
      self.addLehreSynja("")
    else:     
      self.coding = False
      self.addLehreSynja(str(ausgabetext))
    '''
 
  #parsed dialogeingabe mit nlu, bzw. bewertet lehreingabe mit expertenmodell
  #gibt intents an lehrmanager weiter
  #uebersetzt intents mit nlg, lehrausgabeobjekte mit expertenmodell
  def schritt(self, inputDialog, inputLehre):
    if(inputDialog != ""):
      eingabe_intent = self.nlu.parse(inputDialog)
      entity = self.nlu.parseName(inputDialog)     
      if(eingabe_intent!="name"): 
        entity = self.nlu.parse_thema(inputDialog)
        if(entity != ""): eingabe_intent="naechsterThemenblock"
        
      #print("SL input: "+inputDialog+" intent: "+eingabe_intent+" entity: "+entity)        
      self.lehrmanager.schritt(eingabe_intent,entity)    

      if("bye" in self.lehrmanager.dialogausgaben):
        print("VERABSCHIEDUNG")
        exit(1)

      for s in self.lehrmanager.dialogausgaben: 
        phrase = ""
        if isinstance(s, Lehrausgabe):
          if(s.darstellungsart == "coding" or s.darstellungsart == "test_lt" or s.darstellungsart == "test_mc"): 
            #print("SW: TASK: "+str(phrase))
            phrase = [self.convertLehreSynjaText(s),"Task"]
          else: phrase = [self.convertLehreSynjaText(s),"Lehre"]

        elif isinstance(s, Hinweis):
          #print("SW: HINWEIS 1"+s.fehlerart)
          phrase = self.expertenmodell.zugriffHinweis(s.lesson, s.konzeptname, s.fehlerart)
        elif isinstance(s, Enaktivausgabe):
          #print("SW: ENAKT ZUST: "+s.zustand)
          if(s.zustand == "enaktiv_introduction_schritte"): phrase = self.nlg.generate_args("enaktiv_introduction_schritte",s.konzept)
          elif(s.zustand == "enaktiv_introduction_beispiele"): phrase = self.nlg.generate_args("enaktiv_introduction_beispiele",s.konzept)
          elif(s.zustand == "anfang"): phrase = self.nlg.generate_args("enaktiv_anfang",self.expertenmodell.zugriffEnaktiv(s.lesson, s.konzept, s.schritt))
          elif(s.zustand == "schritt"): phrase = self.nlg.generate_args("enaktiv_schritt",self.expertenmodell.zugriffEnaktiv(s.lesson, s.konzept, s.schritt))
          elif(s.zustand == "beispiel"): phrase = self.nlg.generate_args("enaktiv_beispiel",self.expertenmodell.zugriffEnaktiv(s.lesson, s.konzept, s.schritt))
          elif(s.zustand == "erweiterung"): phrase = self.nlg.generate_args("enaktiv_erweiterung",self.expertenmodell.zugriffEnaktiv_erweiterung(s.lesson, s.konzept, s.schritt))
          elif(s.zustand == "ende"): phrase = self.nlg.generate_args("enaktiv_ende",s.konzept)
 
        elif isinstance(s, Fehlerantwort):
          phrase = s.beschreibung
        elif isinstance(s, list) and len(s)==2:
          phrase = self.nlg.generate_args(s[0], s[1])
        else:
          phrase = self.nlg.generate(s)
        self.outputDialog.append(phrase)  
          
      #self.outputLehre = self.lehrmanager.getLehrAusgaben()   
      
    if(inputLehre != None and inputLehre != ""):
      self.lehrmanager.schritt(inputLehre,"")
      for s in self.lehrmanager.dialogausgaben: 
        phrase = ""
        print(s)
        if isinstance(s, Lehrausgabe):
          phrase = [self.convertLehreSynjaText(s),"Lehre"]
        elif isinstance(s, Hinweis):
          #print("SW: HINWEIS 2"+s.fehlerart)
          phrase = self.expertenmodell.zugriffHinweis(s.lesson, s.konzeptname, s.fehlerart)
        elif isinstance(s, Enaktivausgabe):
          #print("SW: ENAKT ZUST: "+s.zustand)
          if(s.zustand == "enaktiv_introduction_schritte"): phrase = self.nlg.generate_args("enaktiv_introduction_schritte",s.konzept)
          elif(s.zustand == "enaktiv_introduction_beispiele"): phrase = self.nlg.generate_args("enaktiv_introduction_beispiele",s.konzept)
          elif(s.zustand == "anfang"): phrase = self.nlg.generate_args("enaktiv_anfang",self.expertenmodell.zugriffEnaktiv(s.lesson, s.konzept, s.schritt))
          elif(s.zustand == "schritt"): phrase = self.nlg.generate_args("enaktiv_schritt",self.expertenmodell.zugriffEnaktiv(s.lesson, s.konzept, s.schritt))
          elif(s.zustand == "beispiel"): phrase = self.nlg.generate_args("enaktiv_beispiel",self.expertenmodell.zugriffEnaktiv(s.lesson, s.konzept, s.schritt))
          elif(s.zustand == "erweiterung"): phrase = self.nlg.generate_args("enaktiv_erweiterung",self.expertenmodell.zugriffEnaktiv_erweiterung(s.lesson, s.konzept, s.schritt))
          elif(s.zustand == "ende"): phrase = self.nlg.generate_args("enaktiv_ende",s.konzept)
  
        elif isinstance(s, Fehlerantwort):
          phrase = s.beschreibung
          #print("SW schritt: "+phrase)
        elif isinstance(s, list) and len(s)==2:
          phrase = self.nlg.generate_args(s[0], s[1])
        else:
          phrase = self.nlg.generate(s)
        self.outputDialog.append(phrase)     

      #self.outputLehre = self.lehrmanager.getLehrAusgaben()   
      
               
  def __init__(self,id,nr,name):  
    self.name = name
    self.id = id
    self.nr = nr
    self.nlg = NLG("en")
    self.nlu = NLU("en")
    self.em = Expertenmodell("en")
    self.dialogmanager= Dialogmanager(name)
    self.lehrmanager=Lehrmanager(name, self.em.lessoninhalte, self.em.anzahl_erklaerungen, self.em.anzahlAufg, self.em.anzahlWE, self.em.anzahl_lt, self.em.anzahl_mc,self.em.en_schritt_dict,self.em.enaktiv_artdict)
    self.verlauf = Verlauf(self.em)
    if(self.name == "NO_ACCOUNT"): self.lehrmanager.neuernutzer = True
     
    #Teil der fuer app und ui gebraucht wird
    super(Synja, self).__init__()
    Synja.totalCount += 1
    self.running = True
    
    self.sendqueueDialog =  queue.Queue()
    self.sendqueueDialogZeichen =  queue.Queue()
    self.recvqueueDialog =  queue.Queue()
    self.sendqueueLehre =  queue.Queue()
    self.recvqueueLehre =  queue.Queue() 
    
    
  #sichert den Stand
  #def save(self):
    #if(self.name != "NO_ACCOUNT"): self.lehrmanager.schuelermodell.speichern()
      
  #fuegt nutzereingaben die vom Dialog input kommen in queue ein      
  def addDialogNutzer(self, input):
    self.no_resp_time = 20
    self.highlight_input_element = ""
    self.lastmessagetime = int(round(time.time()))
    
    if(self.lehrmanager.expected_entry == "lehre"):
      if(self.nlu.parse(input) == ""):
        self.lehrmanager.handle_noreaction()
        self.highlight_input_element = self.lehrmanager.expected_entry
        self.reaction_without_input()
        return
    
    #print("SW: aDN: "+input+"["+self.name+"]")
    self.recvqueueDialog.put(input)
    self.text+="You: "+input+'\n'

  #fuegt nutzereingaben die vom Teaching input kommen in queue ein
  def addLehreNutzer(self, input):
    self.lastmessagetime = int(round(time.time()))
    self.no_resp_time = 20
    
    self.lastmessagetime = int(round(time.time()))
    if(self.lehrmanager.expected_entry == "dialog"):
      self.lehrmanager.handle_noreaction()
      self.highlight_input_element = self.lehrmanager.expected_entry
      self.reaction_without_input()
      return
      
    self.recvqueueLehre.put(input)

  #fuegt alle dialogausgaben in ausgabequeue ein (hinweisdialoge und Fehlerantworten, beide als dialogausgaben werden vorher konvertiert)
  def addDialogSynja(self, dialogausgabe):
    self.lastmessagetime = int(round(time.time()))
    self.no_resp_time = 20

    ausgabe = dialogausgabe
    if isinstance(dialogausgabe, Hinweis):
      #print("SW: HINWEIS 3"+dialogausgabe.fehlerart)
      ausgabe = self.expertenmodell.zugriffHinweis(dialogausgabe.lesson, dialogausgabe.konzeptname, dialogausgabe.fehlerart)
    if(isinstance(dialogausgabe, Fehlerantwort)):
      ausgabe = dialogausgabe.beschreibung     
    
    if(isinstance(ausgabe, list)):self.sendqueueDialog.put(ausgabe)
    else: self.sendqueueDialog.put(ausgabe)
    
    
  #fuegt lehrausgaben von synja in eingabequeue ein, die konvertierungen geschehen in schritt()
  def addLehreSynja(self, phrase):
    #fluhed die lehrausgabe 
    #for i in range(20):
    #  self.sendqueueLehre.put("\n")
    self.lastmessagetime = int(round(time.time()))
    self.no_resp_time = 20
    self.highlight_input_element = ""
    phrase = phrase.replace('\\n','\n')
    self.sendqueueDialog.put([phrase,"Lehre"])
    #print("SW LEHRE: "+phrase)
     
  #hoert auf die beiden eingabequeues, wenn ausgabequeue leer sind
  def listen(self):
    if(self.sendqueueDialog.empty() == False): return None
    a = None
    b = None
    if(self.recvqueueDialog.empty() == False): 
      a = self.recvqueueDialog.get()
      #print("Dialog: "+str(a))
    if(self.recvqueueLehre.empty() == False): 
      b = self.recvqueueLehre.get()
      #print("Lehre: "+str(b))
    return [a,b] 
  
  #getter fuer sendqueueDialog
  def getDialogSynja(self):
    time.sleep(self.sleeptime)
    ausgabe = self.sendqueueDialog.get()
    self.sleeptime = len(str(ausgabe)) / writeV
    return ausgabe
   
  #hilfsfunktion fuer responsiveness
  def reaction_without_input(self):
    for s in self.lehrmanager.dialogausgaben: 
      phrase = ""
      if isinstance(s, Lehrausgabe):
        if(s.darstellungsart == "coding" or s.darstellungsart == "test_lt" or s.darstellungsart == "test_mc"): 
         # print("SW: TASK: "+str(phrase))
          phrase = [self.convertLehreSynjaText(s),"Task"]
        else: phrase = [self.convertLehreSynjaText(s),"Lehre"]

      elif isinstance(s, Hinweis):
        #print("SW: HINWEIS 1"+s.fehlerart)
        phrase = self.expertenmodell.zugriffHinweis(s.lesson, s.konzeptname, s.fehlerart)
      elif isinstance(s, Enaktivausgabe):
        #print("SW: ENAKT ZUST: "+s.zustand)
        if(s.zustand == "enaktiv_introduction_schritte"): phrase = self.nlg.generate_args("enaktiv_introduction_schritte",s.konzept)
        elif(s.zustand == "enaktiv_introduction_beispiele"): phrase = self.nlg.generate_args("enaktiv_introduction_beispiele",s.konzept)
        elif(s.zustand == "anfang"): phrase = self.nlg.generate_args("enaktiv_anfang",self.expertenmodell.zugriffEnaktiv(s.lesson, s.konzept, s.schritt))
        elif(s.zustand == "schritt"): phrase = self.nlg.generate_args("enaktiv_schritt",self.expertenmodell.zugriffEnaktiv(s.lesson, s.konzept, s.schritt))
        elif(s.zustand == "beispiel"): phrase = self.nlg.generate_args("enaktiv_beispiel",self.expertenmodell.zugriffEnaktiv(s.lesson, s.konzept, s.schritt))
        elif(s.zustand == "erweiterung"): phrase = self.nlg.generate_args("enaktiv_erweiterung",self.expertenmodell.zugriffEnaktiv_erweiterung(s.lesson, s.konzept, s.schritt))
        elif(s.zustand == "ende"): phrase = self.nlg.generate_args("enaktiv_ende",s.konzept)
      elif isinstance(s, Fehlerantwort):
        phrase = s.beschreibung
      elif isinstance(s, list) and len(s)==2:
        phrase = self.nlg.generate_args(s[0], s[1])
      else:
        phrase = self.nlg.generate(s)
      print(phrase)
      self.addDialogSynja(phrase)   
   
  #ermoeglicht reaktion auf ausbleiben von nutzerreaktion 
  def responsiveness(self):
    current = int(round(time.time()))
    if(current-self.lastmessagetime >= self.no_resp_time):
      self.lehrmanager.handle_noreaction()
      self.highlight_input_element = self.lehrmanager.expected_entry
      self.reaction_without_input()
      self.lastmessagetime = current
      self.no_resp_time *= 1.5      
           
  #bereitet einen hinweis vor, welches eingabefeld der nutzer verwenden soll         
  def nutzer_auf_inputfeld_hinweisen(self):
    current = int(round(time.time()))
    if(current-self.lastmessagetime >= self.no_resp_time):
      self.lehrmanager.handle_noreaction()
      self.highlight_input_element = self.lehrmanager.expected_entry
      self.reaction_without_input()
      self.lastmessagetime = current
      self.no_resp_time = 10000000 #kein weiterer Hinweis          