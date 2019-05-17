'''
Created on 06.05.2019

@author: Johannes
'''
import os
import sys
sys.path.append(os.path.abspath('../lehre'))


from Expertenmodell import Expertenmodell
import os
import csv
from time import gmtime, strftime
verzeichnispfad = os.path.realpath(__file__)

class Verlauf(object):
    '''
    classdocs
    '''
    ep = None
    path = os.path.realpath(__file__)[:-10]



    def __init__(self, expertenmodell):
      self.ep = expertenmodell
      
    def eintragen(self, id, lesson, konzeptname, art, version, antworttext, bewertung):
      aufgabenstellung = self.ep.zugriffLehreinheit(lesson, konzeptname, art, version)
      aufgabenstellung = aufgabenstellung.replace('\\n', '\n')
      
      timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
      
      path = os.path.join(os.path.dirname(verzeichnispfad), 'other', 'verlauf.csv')
      
      with open(path,'a+') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([id,timestamp,aufgabenstellung,antworttext,bewertung])
        #file.write(str()+'\n')


ep = Expertenmodell("en")
verlauf = Verlauf(ep)
verlauf.eintragen(0, "basics", "comments", "test_mc", 0, "1", "fehlerfrei")        