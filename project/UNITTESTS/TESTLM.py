'''
Created on 15.04.2019

@author: Johannes
'''
import unittest
from project.lehre.Lehrmanager import Lehrmanager
from project.lehre.Expertenmodell import Expertenmodell
   
 






class Test(unittest.TestCase):

  
  @staticmethod
  def perfekterDurchlauf():
    em = Expertenmodell("en")
    lm=Lehrmanager("john", em.lessoninhalte, em.anzahl_erklaerungen, em.anzahlAufg, em.anzahlWE, em.anzahl_lt, em.anzahl_mc)
    lm.zustand_test = "start"
    lm.lesson = "programm_structure"
    lm.schuelermodell.setName("anna")
    lm.initialisieren_naechsterThemenblock()
    lm.initialisieren_naechstesKonzept("")
    lm.initialisieren_naechstesKonzept("")
    lm.initialisieren_naechstesKonzept("")
    lm.testblockaufg = []
    lm.testphase_block("")
    pass

  @staticmethod
  def testLM_TB(self):
    from ExpertenmodellEN import ExpertenmodellEN #@Unresolvedimport
    from ExpertenmodellDE import ExpertenmodellDE #@Unresolvedimport#TODO: loeschen

    expertenmodell_en = ExpertenmodellEN()  
    lehrmanager=Lehrmanager("bob", expertenmodell_en.lessoninhalte, expertenmodell_en.anzahl_erklaerungen, expertenmodell_en.anzahlAufg, expertenmodell_en.anzahlWE, expertenmodell_en.anzahl_lt, expertenmodell_en.anzahl_mc,expertenmodell_en.en_schritt_dict,expertenmodell_en.enaktiv_artdict)
    lehrmanager.lesson = "programm_structure"
    
    for i in range(1000):
        lehrmanager.gen_next_tb_aufg()  
    
  @staticmethod
  def testgescheiterterBlock():
    em = Expertenmodell("en")
    lm=Lehrmanager("john", em.lessoninhalte, em.anzahl_erklaerungen, em.anzahlAufg, em.anzahlWE, em.anzahl_lt, em.anzahl_mc)
    lm.zustand_test = "start"
    lm.lesson = "programm_structure"
    lm.initialisieren_naechsterThemenblock()
    lm.initialisieren_naechstesKonzept("")
    lm.initialisieren_naechstesKonzept("")
    lm.initialisieren_naechstesKonzept("")
    lm.gen_tb_aufg_list()
    '''
    lm.schritt("fehlerfrei","")
    lm.schritt("fehlerhaft","")
    lm.schritt("fehlerhaft","")
    '''
    pass
    
  @staticmethod
  def nichtVerstandenBlock():
    em = Expertenmodell("en")
    lm=Lehrmanager("john", em.lessoninhalte, em.anzahl_erklaerungen, em.anzahlAufg, em.anzahlWE, em.anzahl_lt, em.anzahl_mc)
    lm.zustand_test = "start"
    lm.lesson = "programm_structure"
    lm.initialisieren_naechsterThemenblock()
    lm.initialisieren_naechstesKonzept("")
    lm.schritt("nein","") 
    pass
    
  def testgen_tb_aufg_list(self):
    em = Expertenmodell("en")
    lm=Lehrmanager("john", em.lessoninhalte, em.anzahl_erklaerungen, em.anzahlAufg, em.anzahlWE, em.anzahl_lt, em.anzahl_mc)
    lm.lesson = "programm_structure"
    lm.gen_tb_aufg_list()
    print("AUFGABEN: "+str(lm.testblockaufg))
    pass


if __name__ == "__main__":
    unittest.main()