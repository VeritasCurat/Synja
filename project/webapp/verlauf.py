'''
Created on 06.05.2019

@author: Johannes
'''
import os
import sys
#import psutil
sys.path.append(os.path.abspath('../lehre'))
sys.path.append(os.path.abspath('.'))
from ExpertenmodellEN import ExpertenmodellEN  #@Unresolvedimport
from ExpertenmodellDE import ExpertenmodellDE  #@Unresolvedimport

import os
import csv
import time
from time import gmtime, strftime
verzeichnispfad = os.path.realpath(__file__)

def eintragen_load(synjanr):
  '''
  cpu = psutil.cpu_percent()
  mem = psutil.virtual_memory()
  nrsynja = str(synjanr)+" Synjas"
  timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
  path = os.path.join(os.path.dirname(verzeichnispfad), 'other', 'systemload.csv')
  #print(str(cpu)+" "+str(mem))
  with open(path,'a+') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow([timestamp,cpu,mem,nrsynja])
  '''
  
class Verlauf(object):
    '''
    classdocs
    '''
    ep = None
    path = os.path.realpath(__file__)[:-10]



    def __init__(self, expertenmodellEN, expertenmodellDE):
      self.ep_en = expertenmodellEN
      self.ep_de = expertenmodellDE
     
      
    def eintragen(self, sprache, id, lesson, konzeptname, art, version, antworttext, bewertung):
      if(sprache == "en"):aufgabenstellung = self.ep_en.zugriffLehreinheit(lesson, konzeptname, art, version)
      elif(sprache == "de"):aufgabenstellung = self.ep_de.zugriffLehreinheit(lesson, konzeptname, art, version)
      aufgabenstellung = aufgabenstellung.replace('\\n', '\n')
     
      timestamp = self.gettime(0)
      
      path = os.path.join(os.path.dirname(verzeichnispfad), 'other', 'verlauf.csv')
      
      with open(path,'a+') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([str(id),timestamp,aufgabenstellung,antworttext,bewertung])
        #file.write(str()+'\n')

    def gettime(self,hours):
      #timept = gmtime() + 7200
      #strftime("%Y-%m-%d %H:%M:%S", timept)
      timept = time.time() + hours*3600
      timestamp = time.ctime(timept)
      return timestamp
      
'''

ep_de = ExpertenmodellEN()
ep_en = ExpertenmodellEN()
verlauf = Verlauf(ep_en,ep_de)
verlauf.eintragen("en",0, "basics", "comments", "test_mc", 0, "1", "fehlerfrei")        
print(verlauf.gettime(0))
'''