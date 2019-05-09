'''
Created on 21.01.2019
@author: Johannes Grobelski


'''
from project.webapp.Nutzer import Nutzer
from project.webapp.NutzerID import NutzerID

from project.lehre.Lehrmanager import Lehrmanager, Fehlerantwort, Hinweis
from project.lehre.Expertenmodell import Expertenmodell
 
from project.dialog.Dialogmanager import Dialogmanager
from project.dialog.NLG import NLG
from project.dialog.NLU import NLU

import threading
import warnings
import time
import queue
from idlelib.idle_test.test_configdialog import dialog


LESEGESCHWINDIGKEIT = 1 #wartezeit nach schreiben von Nachricht
SCHREIBGESCHWINDIGKEIT = 0.05 #sekunde pro zeichen gut: 0.05

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
  lasttimeout = 0
  timed = False
  running = True
  input = False
  
  coding = False
   
  lastmessages = [] #display the last 10 messages 
  text = ""
  
  #main method, organize the whole structure of the dialogue#
  def run(self):
    warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

    begruessung = self.nlg.generate("begruessung")
    self.tell_dialog(begruessung) 
    self.text+="Synja: "+begruessung+'\n'      
  
    while(True):
      listen = self.listen()    
            
      eingabeDialog = listen[0]
      eingabeLehre = listen[1]
            
            
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
    
    if(self.outputLehre != None):
        #print(str(self.outputLehre.darstellungsart))
        self.addLehreSynjaText(self.outputLehre)
    
    self.outputLehre = None
    self.outputDialog = []  
    
    #self.save()
    
  def lehreingabe(self, antworttext):
    if(self.lehrmanager.zustand=="testphase_konzept" or self.lehrmanager.zustand=="testphase_block" or self.lehrmanager.zustand=="konzeptbeschreibung_enaktiv" or self.lehrmanager.zustand=="fehlerklassifizierung"): 
      #Auswertung nameeingabe
      lesson = self.lehrmanager.lesson
      konzeptname = self.lehrmanager.konzept
      art = self.lehrmanager.art
      version = self.lehrmanager.version
      bewertung = self.em.bewerten(lesson, konzeptname, art, version, antworttext)
      print("bewertung: "+bewertung)
      
      if(art == "underline_task"):
        if(bewertung != "fehlerfrei"):
          self.lehrmanager.fehlerart = bewertung
          bewertung = "fehlerhaft"
      elif(art == "coding"):
        if(bewertung != "fehlerfrei"):
          self.lehrmanager.fehlerart = bewertung
          bewertung = "fehlerhaft"
      self.schritt("",bewertung)
     
      self.tellwithpauses(self.outputDialog)
            
      if self.outputLehre!= None: 
        self.addLehreSynjaText(self.outputLehre)  
        
        
      self.outputDialog = []
      self.outputLehre = None
  
      #self.save()
      
  def tellwithpauses(self, ausgabe):
    if(ausgabe == None or len(ausgabe) == 0): return
    elif(len(ausgabe) == 1):self.addDialogSynja(ausgabe[0])
    else:
      for s in ausgabe: 
        #secondswait = len(s) / LESEGESCHWINDIGKEIT
        self.addDialogSynja(s)
        #time.sleep(secondswait)
       
  def addDialogSynja(self, dialogausgabe):
    ausgabe = dialogausgabe
    if isinstance(dialogausgabe, Hinweis):
      phrase = self.expertenmodell.zugriffHinweis(dialogausgabe.lesson, dialogausgabe.konzeptname, dialogausgabe.fehlerart)
    if(isinstance(dialogausgabe, Fehlerantwort)):
      ausgabe = self.em.zugriffFKantwort(dialogausgabe.lesson, dialogausgabe.konzeptname, dialogausgabe.fehlerart)
    print("SW: aDS"+str(ausgabe)+"["+self.name+"]")
    self.tell_dialog(ausgabe)


  def addLehreSynjaText(self, lehrausgabe):
    #konzeptname, darstellungsart, version, nameid
    ausgabe = self.em.zugriffLehreinheit(lehrausgabe.lesson, lehrausgabe.konzeptname, lehrausgabe.darstellungsart, lehrausgabe.version)
  
    ausgabetext = ausgabe
    ausgabetext = ausgabetext.replace('\\n', '\n')
    print("AUSGABETEXT: "+ausgabetext)
      
    if(lehrausgabe.darstellungsart=="coding"):
      self.coding = True
      self.tellwithpauses([str(ausgabetext)])
      self.tell_lehre("")
    else:     
      self.coding = False
      self.tell_lehre(str(ausgabetext))

  def schritt(self, inputDialog, inputLehre):
    if(inputDialog != ""):
      eingabe_intent = self.nlu.parse(inputDialog)
      entity = self.nlu.parseName(inputDialog)     
      if(eingabe_intent!="name"): 
        entity = self.nlu.parse_thema(inputDialog)
        if(entity != ""): eingabe_intent="naechsterThemenblock"
        
      print("SL input: "+inputDialog+" intent: "+eingabe_intent+" entity: "+entity)  
      
      self.lehrmanager.schritt(eingabe_intent,entity)  
        

      if("bye" in self.lehrmanager.dialogausgaben):
        print("VERABSCHIEDUNG")
        exit(1)

      for s in self.lehrmanager.dialogausgaben: 
        phrase = ""
        print(s)
        if isinstance(s, Hinweis):
          phrase = self.expertenmodell.zugriffHinweis(s.lesson, s.konzeptname)
        elif isinstance(s, Fehlerantwort):
          phrase = self.expertenmodell.zugriffFKantwort(s.lesson, s.konzeptname, s.fehlerart)
        elif isinstance(s, list):
          phrase = self.nlg.generate_args(s[0], s[1])
        else:
          phrase = self.nlg.generate(s)
        self.outputDialog.append(phrase)  
          
      self.outputLehre = self.lehrmanager.getLehrAusgaben()   
      
    if(inputLehre != None and inputLehre != ""):
      self.lehrmanager.schritt(inputLehre,"")
            
      
            
      for s in self.lehrmanager.dialogausgaben: 
        phrase = ""
        print(s)
        if isinstance(s, Hinweis):
          phrase = self.expertenmodell.zugriffHinweis(s.lesson, s.konzeptname, s.fehlerart)
        if isinstance(s, Fehlerantwort):
            phrase = self.em.zugriffFKantwort(s.lesson, s.konzeptname, s.fehlerart)
            print("SW schritt: "+phrase)
        elif isinstance(s, list):
          phrase = self.nlg.generate_args(s[0], s[1])
        else:
          phrase = self.nlg.generate(s)
        self.outputDialog.append(phrase)     

      self.outputLehre = self.lehrmanager.getLehrAusgaben()   
      
    print("ready")
               
  def __init__(self,id,nr,name):  
    print("neue SW INIT: "+name)
    self.name = name
    self.id = id
    self.nr = nr
    self.nlg = NLG("en")
    self.nlu = NLU("en")
    self.em = Expertenmodell("en")
    self.dialogmanager= Dialogmanager(name)
    self.lehrmanager=Lehrmanager(name, self.em.lessoninhalte, self.em.anzahl_erklaerungen, self.em.anzahlAufg, self.em.anzahlWE, self.em.anzahl_lt, self.em.anzahl_mc, self.em.fehlerreaktionen)
    
    #Teil der fuer app und ui gebraucht wird
    super(Synja, self).__init__()
    Synja.totalCount += 1
    self.running = True
    
    self.sendqueueDialog =  queue.Queue()
    self.sendqueueDialogZeichen =  queue.Queue()
    self.recvqueueDialog =  queue.Queue()
    self.sendqueueLehre =  queue.Queue()
    self.recvqueueLehre =  queue.Queue() 
        
    
  def save(self):
    #sichert den Stand
    self.lehrmanager.schuelermodell.speichern()
    
  '''
  simple queue
  
  '''  
    
  def addDialogNutzer(self, input):
    print("SW: aDN: "+input+"["+self.name+"]")
    self.recvqueueDialog.put(input)
    self.text+="You: "+input+'\n'

      
  def addLehreNutzer(self, input):
    self.recvqueueLehre.put(input)

    
  def tell_lehre(self, phrase):
    #fluhed die lehrausgabe 
    #for i in range(20):
    #  self.sendqueueLehre.put("\n")
    phrase = phrase.replace('\\n','\n')
    self.sendqueueLehre.put(phrase)
       
  def tell_dialog(self, phrase):
    self.sendqueueDialog.put("Synja: "+phrase)
    
  def listen_lehre(self):
    answer = self.listen_timeout_lehre(1)
    return answer  
  
  def listen(self):
    a = None
    b = None
    if(self.recvqueueDialog.empty() == False): 
      a = self.recvqueueDialog.get()
      print("Dialog: "+str(a))
    if(self.recvqueueLehre.empty() == False): 
      b = self.recvqueueLehre.get()
      print("Lehre: "+str(b))
    return [a,b] 
  
  
'''
NICHT GENUTZT
'''
   
#Outputs the dialog output letterwise. 
def writehumanly(self, dialogausgaben):
    if(dialogausgaben == None or len(dialogausgaben) == 0): return
    else:
      for ausgabe in dialogausgaben:  
        self.text += "Synja: "
        self.sendqueueDialogZeichen.put(self.text)
        AUSGABE = ausgabe
        if isinstance(ausgabe, Hinweis):
          AUSGABE = self.expertenmodell.zugriffHinweis(ausgabe.lesson, ausgabe.konzeptname, ausgabe.fehlerart)
        elif(isinstance(ausgabe, Fehlerantwort)):
          AUSGABE = self.em.zugriffFKantwort(ausgabe.lesson, ausgabe.konzeptname, ausgabe.fehlerart)
        print("SW: "+AUSGABE)
        punktpause = False
        for zeichen in AUSGABE:
          self.text += zeichen
          self.sendqueueDialogZeichen.put(self.text)
          if(zeichen=="." or zeichen=="?" or zeichen=="!"):
            punktpause = True
            time.sleep(LESEGESCHWINDIGKEIT)
          else: time.sleep(SCHREIBGESCHWINDIGKEIT)
        self.text += '\n'
        self.sendqueueDialogZeichen.put(self.text)
        if(punktpause == False):time.sleep(LESEGESCHWINDIGKEIT)
  