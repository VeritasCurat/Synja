import threading
from project.webapp.liza.ui import UI
import time
from project.webapp.liza.domain import Domain
from project.webapp.liza.phrasebase import Phrasebase
from project.webapp.liza.evaluation import Evaluation
import sys
from project.webapp.liza.parsing import Parsing
import warnings
from random import randint

class L(threading.Thread):
  totalCount = 0  
  
  
  #Initialize all the components#
  def __init__(self,id,nr):  
    self.domain = Domain()
    self.phrasebase = Phrasebase()
    self.parsing = Parsing()
    self.evaluation = Evaluation(self.domain.getTopics(), self.domain.getPraise(), self.domain.getCriticism())
    super(L, self).__init__()
    self.ui = UI(nr)
    self.id = id
    L.totalCount += 1
    self.displayCount()
    self.running = True

  def getUI(self):
    return self.ui
    
  #main method, organize the whole structure of the dialogue#
  def run(self):
  
    #setup
    self.parsing.setui(self.ui)
    warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)
    
    #introductory greeting of the user, general explanations and so on
    self.intro()
    
    #getting stories to ask
    total_number = 6
    stories = self.organizeStories(total_number)
    
    #main loop for asking all stories
    for story in stories:
      self.askStory(story)
    
    #get the evaluation and tell it to the user  
    eval = self.evaluation.evaluate()
    for e in eval:
      self.ui.tell(e)
    
    #say goodbye
    self.goodbye()
   
   
  #just for keeping track of how many lizas there are
  def displayCount(self):
          print("I am the %d. Liza started here since the last restart of the program." % L.totalCount)


  #display a final goodbye message, and then a "system message" stating the liza has disconnected.
  def goodbye(self):
    self.ui.tell("Goodbye!")
    self.ui.info("Liza has disconnected.")
    sys.exit()

  #For asking if the user wants to take a break
  def askbreak(self):
    self.ui.tell("Do you want to continue with this?")
    answer = self.ui.listen()
    if (answer == ""):
      self.ui.tell("Do you want to continue? If you don't reply, I have to assume that you are gone...")
      answer = self.ui.listen()
      if (answer == ""):
        self.ui.tell("Well, okay... I guess we can't continue then.")
        self.goodbye()
    meaning = self.parsing.parse(answer)
    if meaning == "yes":
      self.ui.tell("Okay, great! So let's return to the questions.")
      return True
    self.ui.tell("Oh. I am sorry.")
    self.goodbye()

  #for asking a question and continuing until we finally got an answer
  def askForever(self,question):
    answer = ""
    time = 0
    self.ui.tell(question)
    self.ui.prompt()
    while True:
      time = time + 1
      answer = self.ui.listen()
      if answer == "" and time < 4:
        self.ui.tell(self.phrasebase.getReply("waiting"))
        self.ui.prompt()
      if answer == "" and time >= 4 and time < 7:
        self.ui.tell(self.phrasebase.getReply("worried_waiting"))
        self.ui.prompt()
      if time >= 7 and time < 10:
        continue
      if time >= 10:
        self.ui.tell("It seems that you are a bit distracted right now. Or maybe dead. ... ...I hope you are not dead. But because it's been a while since your last answer...")
        self.ui.prompt()
        self.askbreak()
        time = 0
        self.ui.tell("So my question was: " + question)
        
      if answer != "":
        return answer
      
      
      
  def askStory(self,story):
    #if story type is already explained, go on
    #otherwise, explain
    if not self.domain.getExplained(story.group):
      self.ui.tell(self.phrasebase.getReply("new_topic"))
      self.ui.tell(self.domain.groups[story.group])
      answer = self.askForever(self.phrasebase.getReply("want_topic_explanation"))
      meaning = self.parsing.parse(answer)     
      if meaning == "yes":
        self.ui.tell(self.domain.getExplanation(story.group))
        self.domain.setExplained(story.group)
        self.ui.tell("Now let's get to the question!") 
      if meaning == "no": 
        self.ui.tell("Ok, then let's get right to the question.") 
      else:
        self.ui.tell("Oh, I really like to explain things.")
        self.ui.tell(self.domain.getExplanation(story.group))
        self.domain.setExplained(story.group)
        self.ui.tell("Now let's get to the question!") 
        
    if (len(story.intro) > 0):
      answer = self.askForever(story.intro)
      meaning = self.parsing.parse(answer)
      if "yes" in meaning:
        self.ui.tell(story.introyes)
      elif "no" in meaning:
        self.ui.tell(story.introno) 
      else:
        self.ui.tell(self.phrasebase.getReply("meaninglesses"))
        
    self.ui.tell(story.text)
    self.ui.tell(story.question)
    answer = self.ui.listenLong()
    
    
    if answer == "" or answer == None:
      print("seems like they don't know the answer...")
      self.ui.tell(self.phrasebase.getReply("offer_hint"))
      self.ui.prompt()
      answer = self.ui.listen() 
      meaning = self.parsing.parse(answer)   
      #print(answer)
      #print(meaning)
      if meaning == "yes":
        self.ui.tell(story.hint)
        self.ui.prompt()
      if meaning == "no":
        self.ui.tell("ok!")
      
      meaning = self.parsing.parse(answer)    
      if not meaning == "correct" or meaning == "incorrect":
        answer = self.askForever(self.phrasebase.getReply("introbla") + story.question)
        #print(answer)

    meaning = self.parsing.parseQuiz(answer, story)    
    #print(meaning)
    
    if meaning == "whatquestion":
      self.ui.tell("The question was: " + story.question)
    
  #  if meaning == "hint":
  #    self.ui.tell(story.hint)
  #    answer = askForever(self.phrasebase.getReply("introbla") + story.question)
    
    
    if meaning == "explain":
      self.ui.tell(self.phrasebase.getReply("offer_explanation"))
      self.ui.prompt()
      answer = self.ui.listen() 
      meaning = self.parsing.parse(answer)   
      if meaning == "yes":
        self.ui.tell(story.explain)
        #explained the answer
        #student model: didn't know the answer
        return
        
      
      if meaning == "no":
        self.ui.tell("ok!")
      answer = self.askForever(self.phrasebase.getReply("introbla") + story.question)
      meaning = self.parsing.parse(answer)    
      
      
    if meaning == "correct":
      if(randint(0,1) > 0):
        self.askCalibration(True)
      self.ui.tell(story.answercorrect) #you could also use self.phrasebase.getReply("correct")
      self.evaluation.answer(story, True)

      #student model: knew the answer

    elif meaning == "incorrect":
      if(randint(0,1) > 0):
        self.askCalibration(False)      

      self.evaluation.answer(story, False)
      self.ui.tell(story.answerincorrect) #you could also use self.phrasebase.getReply("incorrect")
      self.ui.tell(self.phrasebase.getReply("offer_explanation"))
      self.ui.prompt()
      answer = self.ui.listen() 
      meaning = self.parsing.parse(answer)   
      if meaning == "yes":
        self.ui.tell(story.explain)

      return
        
        


  def askCalibration(self,correctness):
    self.ui.tell(self.phrasebase.getReply("howsure"))
    answer = self.ui.listen()
    percent = self.parsing.parsePercent(answer)
    self.evaluation.calibrate(correctness, percent)

  def organizeStories(self,total):
    storylist = []
    topic = 0
    for i in range (0,total):
      topic = topic % len(self.domain.getTopics())
      story = self.domain.getStory(topic)
      storylist.append(story)
      topic = topic+1
    return storylist



  def intro(self):
    #the bot introduces itself
    answer = self.askForever(self.phrasebase.getReply("greetings"))
    meaning = self.parsing.parse(answer)
    #print(meaning)
    if "greet" in meaning or "yes" in meaning:
      self.ui.tell("Nice to meet you!")
    answer = self.askForever("You are a human, aren't you?")
    meaning = self.parsing.parse(answer)
    if meaning == "yes":
      self.ui.tell("Great! This means you can help me.")
    if meaning == "no":
      answer = self.askForever("Are you sure? What is the sum of two and three?")
      meaning = self.parsing.parse(answer)
      if meaning == "five":
        self.ui.tell("See, you solved the captcha. You are sufficiently human for my purposes.")
      else:
        self.ui.tell("Very funny. You are definitely human.")

    self.ui.tell("My programmers want me to teach you how to be rational, make good decisions and judge situations correctly.")
    answer = self.askForever("Do you want to be more rational?")
    
    meaning = self.parsing.parse(answer)
    
    if meaning == "yes":
      self.ui.tell("Yeah, that's the spirit!")
      
    if meaning == "no":
      answer =self.askForever("Why would you think that? Rationality is just the ability to make good decisions. Do you want to be able to make good decisions?")
      meaning = self.parsing.parse(answer)
      if meaning == "no":
        self.askbreak()

    self.ui.tell("I will just try to ask you some questions, and try to explain to you what you could do better. If I do a bad job at explaning, just ask me, ok? I never taught humans before.")
    self.ui.tell("So, let's see... the first thing I want you to know is that you don't have to be extremely intelligent to be rational. There are very intelligent people who do things that are not at all reasonable. The key to rational decisions is to know when not to follow your gut feelings, but to stop and actually think about the problem.");
    answer =self.askForever("To get used to the whole situation - how about I ask you a test question? Just to make sure I am doing this teaching thing right. ")
    meaning = self.parsing.parse(answer)
    if meaning == "yes":
      self.ui.tell("Okay, thank you!")
    if meaning == "no":
      self.ui.tell("I would nevertheless like to ask the test question.")
      
    answer =self.askForever("This is my first question: Do people need to follow their gut feelings to make rational decisions?")
    meaning = self.parsing.parse(answer)
    if meaning == "no":
      self.ui.tell("Amazing! I mean, it was easy, I know, but you did it. Very reasonable of you to say this! Now we can start with the actual teaching.")
      
    if meaning == "yes":
      self.ui.tell("Uhm... no. This is a bit awkward. Following you gut feelings means not to think about something, but just go with what feels right. A lot of psychologists have shown that people tend to make a lot of mistakes when they make decisions that way.")
      answer = self.askForever("Do you still want to continue?")
      meaning = self.parsing.parse(answer)
      if meaning == "yes":
        self.ui.tell("Okay! Let's start with the actual teaching!")
      else :
        self.askbreak()
    
    
   
