'''
Created on 22.01.2019

@author: Johannes
'''

class Lueckentext(object):
    '''
    classdocs
    '''

    name = ""
    aufgabenstellung = ""
    aufgabe = ""
    loesungen = []
    
    def loesung_anzeigen(self):
      return self.aufgabe.replace("___", self.loesungen[0])
    
    def __init__(self, name, aufgabenstellung, aufgabe, loesungen):
      self.name = name
      self.aufgabenstellung = aufgabenstellung
      self.aufgabe = aufgabe
      self.loesungen = loesungen
    
    @staticmethod
    def toleranztest_ws(nutzerantwort, loesung, anzahlWS):
    #rekursive Funktion die prueft ob durch einfuegen von whitespaces, die nutzerantwort und die loesung uebereinstimmen  
      #basisschritt
      if(Lueckentext.vergleich(nutzerantwort, loesung)): return True
      if(anzahlWS == 0): return False
      
      #rekursionsschritt
      list = []
      for i in range(len(loesung)):
        if(loesung[i] == ","):
          loesungEINF = loesung[0:i+1]+" "+loesung[i+1:]
          if(Lueckentext.vergleich(nutzerantwort, loesungEINF)): return True
          else: list.append(loesungEINF)
        if(loesung[i] == " "):
          loesungEINF = loesung[0:i+1]+" "+loesung[i+1:]
          if(Lueckentext.vergleich(nutzerantwort, loesungEINF)): return True
          else: list.append(loesungEINF)  
      
      for el in list:
        if(Lueckentext.toleranztest_ws(nutzerantwort, el, anzahlWS-1)):return True
        
        
      return False
  
  
    @staticmethod
    def toleranztest(nutzerantwort, loesung):
    #gibt dem nutzer die moeglichkeit leerzeichen, gross-/kleinschreibung zu missachten
      nutzerantwort = nutzerantwort.lower()
      loesung = loesung.lower()
      nutzerantwort = nutzerantwort.replace("\t","  ")
      loesung = loesung.replace("\t","  ")
      if(Lueckentext.toleranztest_ws(loesung, nutzerantwort, 5)): return True  
      
    @staticmethod
    def vergleichINT(antwort):
      for zeichen in antwort:
        a = False
        for i in range(10):
          if(zeichen == str(i)): 
            a = True
            break
        if(a==False): return False  
      return True  
      
    @staticmethod  
    def vergleich(antwort, loesung):
    #kann klassen aufloesen  
      #print("VGL: "+antwort+" "+loesung)
      if("%integer%" in loesung): return Lueckentext.vergleichINT(antwort)
      
      if(antwort == loesung):return True
      
      else: return False  

    @staticmethod
    def beantworten(antwort, loesung):
      print("Loesungen B: "+str(loesung)+" "+antwort)
      if(Lueckentext.toleranztest(antwort, loesung)):return True
      else: return False
      
      
