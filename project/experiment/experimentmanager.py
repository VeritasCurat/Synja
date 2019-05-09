import os
import re

class Task:
  helptext = ""
  aufgabe = ""
  solutions = []
  
  def __init__(self, helptext, aufgabe, solutions):
    self.helptext = helptext
    self.aufgabe = aufgabe
    self.solutions = solutions
  
  def check_answer(self, answer):
    for solution in self.solutions:
      if self.equal(answer,solution) == True:
        return True
    return False
    
  def equal(self,answer,solution):
    return answer == solution
    
class Experimentmanager:
  verzeichnispfad = os.path.realpath(__file__)[:-20]

  score_test = 0;

  tasks = []
  
  lehrausgabe = ""
  dialogausgabe = ""
  
  zustand = ""
  tasknr = 0

  anz_korrekt = 0
  
  
  
  def __init__(self, art):
    
    self.tasks = []
    if(art == "pre"): self.load_test("pre")
    elif(art == "post"): self.load_test("post")
    self.zustand = "anfang"
    
  def load_test(self, art):
    if(art=="pre"):file = open(self.verzeichnispfad+"pretest.txt", encoding ='ISO-8859-1')
    elif(art=="post"):file = open(self.verzeichnispfad+"posttest.txt", encoding ='ISO-8859-1')
    while(True):
      line = file.readline()
      if(line==""):break
      if(line.startswith('#')):continue
      #neuer Eintrag
      if(line.startswith('\"')):            
        pattern = r":::"
        data = re.split(pattern, line)
        if(data[0] != None):
          helptext = data[0][1:-1]
        if(data[1] != None):
          aufgabe = data[1][1:-1].replace('\\n','\n')
        if(data[2] != None):
          solutions = data[2][2:-2].replace('"','')
          if("::" in solutions):
            solutions = re.split(r"::", solutions)   
          else: solutions = [solutions]
          
        if(helptext != None and aufgabe != None and solutions != None):
          #print(solutions)
          neu = Task(helptext, aufgabe, solutions)
          #print("example: ("+str(tb_name)+"): konzept")
          if(art == "pre"):self.tasks.append(neu)       
          elif(art == "post"):self.tasks.append(neu)      
          
  def ergebnisse_eintragen(self):
    self.score_test = self.anz_korrekt
    
    self.anz_korrekt = 0
    self.zustand = "anfang"

            
  def schritt(self, lehrinput):
    #auswertung
    if(self.tasknr >= len(self.tasks)):
      self.ergebnisse_eintragen()
      return
    if(self.zustand == "anfang"):
      self.zustand = "loesung"
      return self.tasks[self.tasknr].helptext+'\n'+self.tasks[self.tasknr].aufgabe
    elif(self.zustand == "loesung"):
      ergebnis = self.tasks[self.tasknr].check_answer(lehrinput)
      print("EM:"+lehrinput+". LOESUNG ist "+str(ergebnis))
      self.tasknr += 1
      print("EM: AUFGABE: "+str(self.tasknr)+" / "+str(len(self.tasks)))
      self.zustand = "anfang"
      if(ergebnis == True): self.anz_korrekt += 1
      return ergebnis
    else:
      print("falscher Zustand")
      exit(-1)
    
    
'''    
em = Experimentmanager("pre")  
print(em.schritt(""))  
print(em.schritt("public"))  
print(em.schritt(""))
print(em.schritt("int"))  
'''