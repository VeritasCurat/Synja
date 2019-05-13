import sys, time,  random

#The story is a basic element of teaching - it's a question or quiz, wrapped up in some kind of context.
#make sure to have many stories per topic (at least 5, better 10-20).

class multiple_choice(Concept):
#todo
  name = ""
  def __init__(self,Name):
   self.name = Name

class programm_snippet(Concept):
#todo
  name = ""
  program = ""
  
  
  def __init__(self,Name):
   self.name = Name

class Concept(object):
  question = ""
  
  def __init__(self, group, text, question, altquestion, correct, incorrect, intro, yes, no, answercorrect, answerincorrect, explain, hint):
   self.group = group #the topic the story belongs to
   self.text = text #explaining text, what is this all about
   self.question = question #the actual question the user has to answer
   self.altquestion = altquestion #an alternativ phrasing
   self.correct = correct #array of correct keywords
   self.incorrect = incorrect #array of incorrect keywords
   self.intro = intro #optional introduction to set the scene before the basic text of the story
   self.introyes = yes #reaction for one answer to the intro
   self.introno = no #reaction for the other possible answer to the intro
   self.answercorrect = answercorrect #answer if the story was solved correctly
   self.answerincorrect = answerincorrect #answer if the story was solved incorrectly
   self.explain = explain #explanation of the correct solution
   self.hint = hint #hint for helping the user
  
  
class Domain:
 def __init__(self):
 
  #let's initiate with ALL the stories
  
  self.topics = ["variables", "types", "expressions", "assignment", "easy in/out", "control structures", "functions", "parameter transfer", "arrays"]
  self.variables = []
  self.types = []
  self.expressions = []
  self.assignment = []
  self.variables = []
  self.easyIO = []
  self.control_structures = []
  self.functions = []
  self.parameter_transfer = []
  self.arrays = []
  
  self.stories = []
  self.stories.append(self.variables)
  self.stories.append(self.types)
  self.stories.append(self.expressions)
  self.stories.append(self.assignment)
  self.stories.append(self.easyIO)
  self.stories.append(self.control_structures)
  self.stories.append(self.functions)
  self.stories.append(self.parameter_transfer)
  self.stories.append(self.arrays)

  self.explained = []
  self.explained = []
  types = 0   #literale
  variables = 1
  expressions = 2
  assignment = 3
  easyIO = 4
  control_structures = 5
  assignment = 6
  functions = 7
  parameter_transfer = 8
  arrays = 9
 
  
  self.explanations = ["","","","","","","","","",""]
  self.explanations[variables] = "Variables are for containers for literals of a certain type. "
  self.explanations[types] = "Types are attributes to data that tell how to interpret them. Types are associated with a set of literals. Literals are identifiers that have a fixed value associated with them (e.g. ""1"" for the type int or ""true"" for type boolean)." #Quelle: https://en.wikipedia.org/wiki/Data_type 
  self.explanations[expressions] = "An expression is a combination of literals, variables, operators or functions to produce a value."
  self.explanations[assignment] = "An assignment gives a variable a value."
  self.explanations[easyIO] = ""
  self.explanations[control_structures] = "Control structures control which statements of a program are run and how often they are run."
  self.explanations[functions] = "Functions are a tool for reuse of code. A "
  self.explanations[parameter_transfer] = ""
  self.explanations[arrays] = "Arrays are Types "
  
  self.groups = ["","","","","","","","","",""]
  self.groups[variables] = ""
  self.groups[types] = ""
  self.groups[expressions] = ""
  self.groups[assignment] = ""
  self.groups[easyIO] = ""
  self.groups[control_structures] = ""
  self.groups[functions] = ""
  self.groups[parameter_transfer] = ""
  self.groups[arrays] = ""
  
  self.praise = ["","","","","","","","","",""]
  self.praise[variables] = "your_understanding_of_variables = ""very good"""
  self.praise[types] = "It seems you know types. Very good!"
  self.praise[expressions] = "You have understood what expressions are and how to use them."
  self.praise[assignment] = "Youre answers has been a sign that youre good at assignments!"
  self.praise[easyIO] = "Easy Input. Easy Output. Easy for you!"
  self.praise[control_structures] = "IF(topic==""control structures"")you_rock=true;"
  self.praise[functions] = "You know how to use functions."
  self.praise[parameter_transfer] = ""
  self.praise[arrays] = "";
  
  
  
  self.criticism = ["","","","","","","","","",""]
  self.criticism[variables] = ""
  self.criticism[types] = "Types bother you. Sad ..."
  self.criticism[expressions] = "I'm sorry, you havn't expressed a good knowledge about expressions"
  self.criticism[assignment] = ""
  self.criticism[easyIO] = "Easy Input / Output isn't too easy for you!"
  self.criticism[control_structures] = "You're not in control of control structures!"
  self.criticism[functions] = "You're not too good with functions. Let's change that!"
  self.criticism[parameter_transfer] = ""
  self.criticism[arrays] = "";
  
  
  #stories erstellen
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  for i in range(len(self.topics)):
   self.explained.append(0)
  
  print("--domain initialised--")
  
  
 def getTopics(self):
  return self.topics
 
 def getPraise(self):
  return self.praise
  
 def getCriticism(self):
  return self.criticism
 
 def getExplained(self, nr):
  return self.explained[nr]
 
 def setExplained(self, nr):
  self.explained[nr] = 1
 
 
 def getExplanation(self, nr):
  return self.explanations[nr]
 
 
 def getStory(self, number):
  #returns story of the type / topic specified in the number
   if(len(self.stories[number])) == 0:
    raise ValueError("There are not enough stories")
   
   s = random.choice(self.stories[number])
   self.stories[number].remove(s)
   return s
 

  