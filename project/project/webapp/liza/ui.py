import sys, time
import warnings
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
import sys, time, select
import queue
import threading

class TimeoutExpired(Exception):
    pass


class UI:	
    
  
  
  def __init__(self,nr):
    self.sendqueue =  queue.Queue()
    self.recvqueue =  queue.Queue()    
    self.nr = nr  
    self.lasttimeout = 0
    self.timed = False
    self.running = True
    self.input = False
    print("--ui initialised--")

  def drain(self,q):
#    while True:
#      try:
#        yield q.get_nowait()
#      except queue.Empty:  # on python 2 use Queue.Empty
#        break
#    print("drained")
     print("bla")
#  def myturn(self):
#    while(not self.recvqueue.empty()):
#      input = self.recvqueue.get()
#      print(input)
      
  def connect(self):
    print("connected")
    #self.sendqueue = sendqueue
    #self.recvqueue = recvqueue

    
  def info(self, phrase):
    self.sendqueue.put("~"+phrase + "~")
    
    
  def tell(self, phrase):
    #print("sending " + phrase)
    while(self.recvqueue.qsize()>0):
       lost = self.recvqueue.get()
#       print("We may have lost: " + lost)
#    self.conn.send("Liza: \""+phrase + "\"")

    phrase.replace("Mr.", "Mr")
    phrase.replace("Mrs.", "Mrs")
    phrase.replace("etc.", "etc")
    phrase.replace("ca.", "ca")
    remain = phrase
    #print(phrase)
    while (len(remain) >0):
        output = ""
        end = 1
        while((output.count('. ')+output.count('!')) < 2 and end < len(remain)):
          end = end+1
          output = remain[:end]
        #print("Output: "+output)
        if output[0] == ' ':
          output = output[1:]
        if output[len(output)-1] == ' ':
          output = output[:-1]
        self.sendqueue.put("Liza: \""+output+"\"")
        if(len(output)>150):
          time.sleep(3)
        else:
          time.sleep(1)
        remain = remain[end:]
        #print("Remain: +" + remain+"+")
      
    
  def analyze(self,phrase):
    #print("sending analysis")
    self.sendqueue.put("    ["+phrase+"]")

  def prompt(self):
    #print("empty function")
    a = 0
    
  def add(self, input):
 #     print("added to queue: " + input)
      
      self.recvqueue.put(input)
 #     for item in self.drain(self.recvqueue):
 #         print(item)
      #print("---")
      
  def listen_timeout(self, timeout):
    
    end = time.time() + timeout
    #print (str(time.time()) + " " + str(end)) 
    while(self.running):
      if (self.input):
        userinput = self.recvqueue.get()
        self.input=False
        if userinput is not None:
        #  print ("returning " + userinput)
          return userinput
        else:
         # print ("returning \"\"")
          return ""
      else:
        #print (str(time.time()) + " " + str(end))
        if time.time() >= end:
          return ""
          #print ("returning \"\"")
        else:
          time.sleep(0.5)
          continue

      
  def listenLong(self):
#    print("listenlong") 
    answer = self.listen_timeout(60)
    return answer

  def listen(self):
    answer = self.listen_timeout(30)
    return answer