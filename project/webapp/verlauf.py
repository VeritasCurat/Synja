'''
Created on 06.05.2019

@author: Johannes
'''
from project.lehre.Expertenmodell import Expertenmodell
import os
import csv
from time import gmtime, strftime

class Verlauf(object):
    '''
    classdocs
    '''
    ep = None
    path = os.path.realpath(__file__)


    def __init__(self, expertenmodell):
      self.ep = expertenmodell
      
    def eintragen(self, id, lesson, konzeptname, art, version, antworttext, bewertung):
      aufgabenstellung = self.ep.zugriffLehreinheit(lesson, konzeptname, art, version)
      aufgabenstellung = aufgabenstellung.replace('\\n', '\n')
      
      timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
      with open("other/verlauf.csv", 'a+') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([id,timestamp,aufgabenstellung,antworttext,bewertung])
        #file.write(str()+'\n')
      
      
ep = Expertenmodell("en")
verlauf = Verlauf(ep)
verlauf.eintragen("hans", "basics", "literals", "test_mc", 0, "1", "fehlerhaft")
      