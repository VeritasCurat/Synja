import ui as ui
import domain as domain
import phrasebase as phrasebase
import sys, time
import parsing as parsing
import warnings


# stable (gender, age, name)
# profile (skills)
# context (frustration, attention)
# 

ui = ui.UI()
domain = domain.Domain()
phrasebase = phrasebase.Phrasebase()
parsing = parsing.Parsing()




def goodbye():
  ui.tell("Goodbye!")
  sys.exit()


def askbreak():
  ui.tell("Do you want to continue with this?")
  answer = ui.listen()
  if (answer == ""):
    ui.tell("Do you want to continue? If you don't reply, I have to assume that you are gone...")
    answer = ui.listen()
    if (answer == ""):
      ui.tell("Well, okay... I guess we can't continue then.")
      return False
  
  meaning = parsing.parse(answer)
  if meaning == "yes":
    ui.tell("Okay, great! So let's return to the questions.")
    return True
  ui.tell("Oh. I am sorry.")
  return False

def askForever(question):
  answer = ""
  time = 0
  ui.tell(question)
  ui.prompt()
  while True:
    time = time + 1
    answer = ui.listen()
    if answer == "" and time < 4:
      ui.tell("\n")
      ui.tell(phrasebase.getReply("waiting"))
      ui.prompt()
    if answer == "" and time >= 4 and time < 7:
      ui.tell("\n")
      ui.tell(phrasebase.getReply("worried_waiting"))
      ui.prompt()
    if time >= 7 and time < 10:
      continue
    if time >= 10:
      ui.tell("\n")
      ui.tell("It seems that you are a bit distracted right now. Or maybe dead. ... ...I hope you are not dead. But because it's been a while since your last answer...")
      ui.prompt()
      if askbreak():
          time = 0
          ui.tell("So my question was: " + question)
          ui.prompt()
          continue
      else:
          goodbye()
          break
      
    if answer != "":
      return answer
    
    
    
def askStory(story):
  #if story type is already explained, go on
  #otherwise, explain
  #intro
  
  
  
  if not domain.getExplained(story.group):
    ui.tell(phrasebase.getReply("new_topic"))
    ui.tell(domain.groups[story.group])
    answer = askForever(phrasebase.getReply("want_topic_explanation"))
    meaning = parsing.parse(answer)     
    if meaning == "yes":
      ui.tell(domain.getExplanation(story.group))
      domain.setExplained(story.group)
      ui.tell("Now let's get to the question!") 
    if meaning == "no": 
      ui.tell("Ok, then let's get right to the question.") 
  
  ui.tell(story.text)
  ui.tell(story.question)
  ui.prompt()
  answer = ui.listenLong()
  meaning = parsing.parseQuiz(answer, story)   
#  if answer == "":
#    ui.tell(phrasebase.getReply("offer_hint"))
#    ui.prompt()
#    answer = ui.listen() 
#    meaning = parsing.parse(answer)   
#    if meaning == "yes":
#      ui.tell(story.hint)
#      ui.prompt()
#    if meaning == "no":
#      ui.tell("ok!")
#    answer = askForever(phrasebase.getReply("introbla") + story.question)
#    meaning = parsing.parse(answer)    
  
  
  if meaning == "whatquestion":
    ui.tell("The question was: " + story.question)
  
#  if meaning == "hint":
#    ui.tell(story.hint)
#    answer = askForever(phrasebase.getReply("introbla") + story.question)
  
  
  if meaning == "explain":
    ui.tell(phrasebase.getReply("offer_explanation"))
    ui.prompt()
    answer = ui.listen() 
    meaning = parsing.parse(answer)   
    if meaning == "yes":
      ui.tell(story.explain)
      #explained the answer
      #student model: didn't know the answer
      return
      
    
    if meaning == "no":
      ui.tell("ok!")
    answer = askForever(phrasebase.getReply("introbla") + story.question)
    meaning = parsing.parse(answer)    
    
    
  if meaning == "correct":
    ui.tell(phrasebase.getReply("correct"))
    #student model: knew the answer

  elif meaning == "incorrect":
    ui.tell(phrasebase.getReply("incorrect"))
    ui.tell(phrasebase.getReply("offer_explanation"))
    ui.prompt()
    answer = ui.listen() 
    meaning = parsing.parse(answer)   
    if meaning == "yes":
      ui.tell(story.explain)
      #explained the answer
      #student model: didn't know the answer
      return
      
  
  
  
#  else:
    #do nothing
  
#  if answer == "correct":
#    ui.tell(phrasebase.getReply("correct")
#  else if answer == "incorrect":
#    ui.tell(phrasebase.getReply("incorrect")
#  else 




def organizeStories(total):
  storylist = []
  topic = 0
  for i in range(total):
    topic = topic % len(domain.getTopics())
    story = domain.getStory(topic)
    storylist.append(story)
    topic = topic + 1 
  return storylist



def intro():
  
  answer = askForever(phrasebase.getReply("greetings"))
  meaning = parsing.parse(answer)
  if "greet" in meaning:
    ui.tell("Nice to meet you!")
    
  answer = askForever("You are a human, aren't you?")
  meaning = parsing.parse(answer)
  if meaning == "yes":
    ui.tell("Great! This means you can help me.")
  if meaning == "no":
    answer = askForever("Are you sure? What is the sum of two and three?")
    meaning = parsing.parse(answer)
    if meaning == "five":
      ui.tell("See, you solved the captcha. You are sufficiently human for my purposes.")
    else:
      ui.tell("Very funny. You are definitely human.")

  ui.tell("My programmers want me to teach you how to be rational, make good decisions and judge situations correctly.")
  askForever("Do you want to be more rational?")
  meaning = parsing.parse(answer)
  
  if meaning == "yes":
    ui.tell("Yeah, that's the spirit!")
    
  if meaning == "no":
    answer = askForever("Why would you think that? Rationality is just the ability to make good decisions. Do you want to be able to make good decisions?")
    meaning = parsing.parse(answer)
    if meaning == "no":
      askbreak()

  ui.tell("I will just try to ask you some questions, and try to explain to you what you could do better. If I do a bad job at explaning, just ask me, ok? I never taught humans before.")
  ui.tell("So, let's see... the first thing I want you to know is that you don't have to be extremely intelligent to be rational. There are very intelligent people who do things that are not at all reasonable. The key to rational decisions is to know when not to follow your gut feelings, but to stop and actually think about the problem.");
  answer = askForever("To get used to the whole situation - how about I ask you a test question? Just to make sure I am doing this teaching thing right. ")
  meaning = parsing.parse(answer)
  if meaning == "yes":
    ui.tell("Okay, thank you!")
  if meaning == "no":
    ui.tell("I would nevertheless like to ask the test question.")
    
  answer = askForever("This is my first question: Do people need to follow their gut feelings to make rational decisions?")
  meaning = parsing.parse(answer)
  if meaning == "no":
    ui.tell("Amazing! I mean, it was easy, I know, but you did it. Very reasonable of you to say this! Now we can start with the actual teaching.")
    
  if meaning == "yes":
    ui.tell("Uhm... no. This is a bit awkward. Following you gut feelings means not to think about something, but just go with what feels right. A lot of psychologists have shown that people tend to make a lot of mistakes when they make decisions that way.")
    answer = askForever("Do you still want to continue?")
    meaning = parsing.parse(answer)
    if meaning == "yes":
      ui.tell("Okay! Let's start with the actual teaching!")
    else :
      askbreak()
  


#if __name__ == '__main__':
#  ui.connect()
#  parsing.setui(ui)
#  warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

#  while(True):
#    ui.tell("Say something. I will try to understand and parse it.")
#    answer = ui.listen()
#    parsed = parsing.parse(answer)
#    analysis = str(parsed['intent']['name']) + ", with confidence " + str(parsed['intent']['confidence'])
#    ui.analyze(analysis)
 
 # intro()
 # stories = organizeStories(total_number)
 # for story in stories:
 #   askStory(story)
 
 
 
def startliza:
  parsing.setui(ui)
  warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

  while(True):
    ui.tell("Say something. I will try to understand and parse it.")
    answer = ui.listen()
    parsed = parsing.parse(answer)
    analysis = str(parsed['intent']['name']) + ", with confidence " + str(parsed['intent']['confidence'])
    ui.analyze(analysis)


  
  
  
