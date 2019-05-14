from project.webapp.liza.domain import Domain as domain
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.components import ComponentBuilder
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Metadata, Interpreter
from project.lehre.Expertenmodell import verzeichnispfad
import random
from builtins import str


class Parsing:
  verzeichnispfad
  builder = ComponentBuilder(use_cache=True) 
  training_data = load_data(verzeichnispfad+'webapp/liza/rasa/training.json')
  trainer = Trainer(config.load(verzeichnispfad+"webapp/liza/rasa/config_spacy.yml"), builder)
  trainer.train(training_data)
  interpreter = Interpreter.load(trainer.persist('model/default'))
  

#  interpreter = Interpreter.load('model\default\default\model_20180607-104830')
 
  
  def __init__(self):
    self.ui = None
    print ("--parser initialised--")

  def setui(self,ui):
    self.ui = ui

  def train(self):
    print("trained.")
    
  
  def getAnswer(self):
      return random.choice(["yes","no"])
    
  def askAgain(self):
    self.ui.tell("Sorry, I didn't get that. Can you rephrase?")
    self.ui.prompt()
    answer = self.ui.listen()
    parse = self.interpreter.parse(answer)
    print("  rasa nlu   " + parse['intent']['name'] + ", with confidence " + str(parse['intent']['confidence']) + "%\n")
    if parse['intent']['confidence'] < 0.4:
      parse = self.askAgain()
    return parse['intent']['name']
    
  def parsePercent(self,string):
    
    #numbers outside of the range are not parsed correctly. e.g. 105 would be parsed as "1".
    
    #print(string)
    if str(100) in string:
      return 100
    
    for i in range(10,100):
      if str(i) in string:
        return i
        
    for i in range(1,11):
      if str(i) in string:
        return i
  
    if "0" in string:
      return 0
    if "totally sure" in string:
      return 90
      
  
    if "unsure" in string:
      return 30
    if "no idea" in string:
      return 20
    if "i guess" in string:
      return 60
    if "no really" in string:
      return 30
    if "no idea" in string:
      return 40
    if "not very" in string:
      return 10
    if "not high" in string:
      return 25
    if "very sure" in string:
      return 90
    if "quite" in string:
      return 75
    if "highly likely" in string:
      return 85
    if "confident" in string:
      return 95
    if "extremely" in string:
      return 99
    if "absolutely" in string:
      return 99
    if "sure" in string:
      return 80
    if "likely" in string:
      return 80
    if "high probability" in string:
      return 80
    if "low probability" in string:
      return 30
    if "very high probability" in string:
      return 90
    if "tiny probability" in string:
      return 10
    if "high" in string:
      return 80
    if "low" in string:
      return 30
    return 50
      
      
  def parse(self,String): 
    #print("trying to parse: " + String + ".")
    try:
      String = String.replace(".","")
      String = String.replace(",","")
      String = String.replace("!","")
      String = String.lower()
      #print(String + " is being parsed")
      parse = self.interpreter.parse(unicode(String))
      print("  rasa nlu   " + parse['intent']['name'] + ", with confidence " + str(parse['intent']['confidence']))
      if parse['intent']['confidence'] < 0.4:
        parse = self.askAgain()
      #print(parse['intent']['name'])
      return parse['intent']['name']
    except:
      print("no input")
      return ""

    
  def parseQuiz(self,String,Story):
    if String == None:
      return ""
      
    print("trying to parse: " + String + ".")
    
    
    parse = self.interpreter.parse(String)
    if parse['intent']['name'] == "explain" and parse['intent']['confidence'] > 0.4:
      return "explain"
    
    if (Story.correct.isdigit() and len(Story.incorrect)==0):
      #it's a story which expects a percentage or a likelihood as an answer!
      #print("we need to parse the input (" + String + ") as percent!")
      percent = self.parsePercent(String)
      correct = int(Story.correct)
      print("Answer was parsed interpreted as " + str(percent) + " and the correct percentage is " + str(correct))
      if (abs(correct-percent) > 20):
        return "incorrect"
      return "correct"
    
    try:
      String = String.replace(".","")
      String = String.replace("!","")
      String = String.lower()
      String = "~"+String+"~"
      corrects = Story.correct.split(", ")
      incorrects = Story.incorrect.split(", ")
      
  #    print ("\n")
  #    print (String)
  #    print(corrects)
  #    print(incorrects)

      for c in corrects:
        if c.lower() in String:
          #print(c)
          #print("correct! " + c)
          return "correct"
        #else:
        #  print("no " + c)
          
      for i in incorrects:
        if i.lower() in String:
          #print(i)
          #print("incorrect! " + i)
          return "incorrect"
        #else:
        #  print("no " + i)
      
      else:
        self.ui.tell("Sorry, I didn't get that. Can you rephrase?")
        answer = self.ui.listen()
        return self.parseQuiz(answer,Story)
        
    except:
      print("no input")
      return ""
    
