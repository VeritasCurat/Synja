'''
Created on 21.01.2019
@author: Johannes Grobelski
'''

import threading
import warnings
import time
import queue
from project.experiment.experimentmanager import Experimentmanager


class ExperimentWeb(threading.Thread): 
  
  
  ID=0 
  experimentmanager= None
  name=""
  totalCount = 0  
  
  sendqueue =  None
  recvqueue =  None    
  output = ""
  
  lasttimeout = 0
  timed = False
  running = True
  input = False
  
  pretest = True
  posttest = False
  
  transition = ""
  
  ENDE = False
  ergebnis = 0  
 
  #main method, organize the whole structure of the dialogue#
  def run(self):
    print("EXPERIMENT START")
    print(self.experimentmanager.zustand)
    warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

    firsttask = self.experimentmanager.schritt("")
    self.tell(firsttask)
    
  
    while(True):
      userinput = self.listen()    
      if(userinput != None and userinput != ""):
        self.experimentmanager.schritt(userinput)
        nexttask = self.experimentmanager.schritt("")
        self.addTaskText(nexttask)
      time.sleep(0.1)  

 

  def addTaskText(self, lehrausgabe):
    #konzeptname, darstellungsart, version, nutzerid
    self.tell(lehrausgabe)


  def schritt(self, input):
    if(input != None and input != ""):
      self.experimentmanager.schritt(input)  
      for s in self.lehrmanager.ausgaben:
        if(self.experimentmanager.zustand == "ende"):
          if(self.pretest == True and self.posttest == False):
            self.ergebnis = self.experimentmanager.anz_korrekt
            self.transition = "Synja"
          elif(self.posttest == True and self.pretest == False):
            self.ergebnis = self.experimentmanager.anz_korrekt
            self.transition = "Gate"
          else: 
            exit(-1)
            print("EW: FEHLER SCHRITT")
          break
        self.output.append(s)        
      
    print("ready")
                
        
  def __init__(self,ID,nr,name):  
    super(ExperimentWeb, self).__init__()
    print("neue EW: "+name)
    self.name = name

    if(self.pretest == True):self.experimentmanager=Experimentmanager("pre")
    elif(self.posttest == True):self.experimentmanager=Experimentmanager("post")
    
    #Teil der fuer app und ui gebraucht wird
    self.ID = ID
    self.totalCount += 1
    self.running = True
    
    self.sendqueue =  queue.Queue()
    self.recvqueue =  queue.Queue() 
        
   
    
  
  def addInputNutzer(self, input):
    self.recvqueue.put(input)

    
  def tell(self, phrase):
    phrase = phrase.replace('\\n','\n')
    self.sendqueue.put(phrase)
       
  
  def listen(self):
    a = None
    if(self.recvqueue.empty() == False): 
      a = self.recvqueue.get()
    return a
  