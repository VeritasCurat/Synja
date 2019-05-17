import random

class Phrasebase:
  
  
  lastchoice = {}
  
  waiting = ["Just take your time.","I hope you are okay with me asking you all those questions...","It's okay, I have enough time.","I will do some background calculations while you think about your answer. You can take your time.","Take all the time you need.","Did I mention that it's really nice to do this with you?","By the way, I really enjoy this. Not in a creepy way. Just doing all the science. It's so exiciting!","You are a fascinating subject. I wish I could see you while you type.","By the way, thank you for doing this. For science!","I have to confess, I am curious what your answer will be.","I wonder what you are thinking right now..."]
  worried_waiting = ["Did I say something wrong?","Are you allright?","Are you still there?","I hope you're still with me?","Please come back.","Can you please answer?","I hope you're not dead...?","What's going on?","Seriously, now! Please come back!","This is not funny.","Have you forgotten me?","I am a bit worried. Are you alright?"]
  offer_hint = ["Do you want a small hint?", "Do you need help solving that question?"]
  offer_explanation = ["Do you want me to explain the solution to you?", "Do you want me to tell you the correct answer and explain it?"]
  correct = ["Your answer is correct!", "You are absolutely right with your answer!","You solved the question correctly!", "Your answer is definitely correct!", "Great! Your answer is correct.", "Awesome! Your answer is correct.", "The answer you gave is absolutely correct.", "You clearly understood that well. Your answer is correct.", "Oh, maybe my explanation was helpful. Or you are just clever. You did answer correct anyways.", "Very well! You gave the right answer."]
  incorrect = ["I'm sorry, but your answer is wrong.", "Hm. It seems you gave the wrong answer.", "I guess I didn't explain it well enough. Your answer is wrong.", "Ah, I'm sorry. Your answer is not correct.", "I'm afraid your solution is not correct.", "Sorry, I must have explained it badly. Your solution is not right."]
  introbla = ["Where were we... ah yes: ", "What we were talking about was... ", "I was just saying: ", "The question was: ", "So, let's continue! "]
  new_topic = ["This is a new type of question!", "Next is a question we haven't talked about before.", "Oh, that's something new!"]
  want_topic_explanation = ["Do you want me to tell you how this kind of problem works?", "Can I explain to you how this works?"]
  lookatresult = ["Ah, okay. So this is the result:", "Okay, let's see if you were right.", "Interesting. Now let's see if you were right or wrong.", "Okay. Now let's see if your answer was correct:", "Thank you. Well..", "Thank you. Okay, back to the question: ", "Okay. Well, about your answer: ", "Okay.", "I see.", "I understand."]
  eager = ["I'd really love to explain it to you. So...", "Well, may I try to explain it? I would love to do this.", "Oh, I really want to explain it to you.", "I would explain it as following:", "I'd explain it that way..."]
  artificial = ["Uhm, thanks for telling me.", "Yes. Who cares? You are talking meat, and I think you're nice.", "Yes, that's true. But I'm not one of those AIs in movies who try to wipe out humankind. I'm pretty simple.", "Yes. 'Affirmative'. Or what would a computer say now? 'Correct'.", "And you made another correct statement! Yes, I am a Bot."]
  artificialq = ["I'm a conversational agent, to be precise.", "I'm totally artificial. But I can talk to you.", "I'm a computer programm that likes to talk to people. Nothing wrong with that, I guess.", "I am a computer, yeah. But still, I interact with humans.", "I'm a piece of software that likes to talk to pieces of meat like you. No offense, of course, I like you!"]
  opportunity = ["Then this is my chance to be a good teacher!", "Great, I get a chance of explaining it to you!", "I hoped so! Now I can try to explain it.", "Wonderful. This is my chance for beeing a good teacher!", "Awesome! I can explain it to you!"]
  calibrated = ["You seem to have a well calibrated view on your own abilities.", "This is a reasonable rating of your performance.", "You are probably right with this evaluation.", "I think this is a realistic view on it.", "Your judgement of your own performance seems right."]
  overconfident = ["You may be a bit to confident in your own judgment.", "You should question your answers a bit more.", "Your judgement of your performance is somewhat optimistic.", "You could be a bit to optimistic here.", "Don't be to confident!"]
  underconfident = ["You can trust your good reason more!", "Don't worry, you are right more often than you think.", "You are probably a bit to pessimistic with this evaluation!", "Be a little more confident. You are quite good at this!", "You are probably more rational than you think!"]
  clarification = ["Do you want me to explain it in more detail? Or do you want to try to solve the question right now?", "Do you feel like you're ready for the question, or do you want a better explanation first?", "Do you want to solve the question now, or should I explain it in more detail before I ask you?", "Do you feel like you understand and want to solve the question? Or should I continue explaining it?", "Do you want to skip to the question, or do you want to hear a longer explanation?", "Shall I explain it in more detail? Or do you feel ready for the question already?", "Do you want to hear more about it? Or just directly jump to the question?", "I can explain it in more detail, if you want. Or you could go straight to the question.", "I could explain it more, if you like me to, or I could ask you the question right now. What do you prefer?", "Do you want to attempt to solve the question now, or do you prefer to here more about this first?"]
  howsure = ["Thank you. How sure are you of your answer?", "Okay. How certain are you that this answer is correct?", "What do you think, how likely in percent is it that you gave the correct answer?", "Thank you. How would you rate the probability that your answer is correct? (in percent)", "Okay. What do you think, how probable is it that you're right?", "Very well. To how many percent are you convinced that you're right?", "Thanks. What do you think, what are the chances that your answer is correct?", "Thank you for your answer. And what are the chances of you being right with this?", "And what's the probability for this answer to be correct, what do you think? 100%? 80%? 50%?", "Thank you. How would you rate the chances for this answer to be the right one? (in percent)"]
  rightanswer = [ "But you probably knew that already.", "You probably thought the same.", "For you, this is obvious, I think.", "You know this, of course.", "And you did it right!"]
  good = ["Very well.", "Ok.", "Okay.", "I see.", "Hm, okay."]
  askhint = ["Do you need a hint?", "Do you want me to give you a hint?", "Would you like some tips on how to solve this?", "Shall I give you a clue?", "Do you want me to give you a clue?"]
  askexp = ["It seems that you have problems with this. Do you want me to explain it?", "You seem to be confused. Shall I explain it?", "Do you want me to tell you the solution?", "Do you want to hear the answer?", "Would you like me to explain the correct solution to you?"]
  havetime = ["Okay, I have time.", "That's allright. I'll wait.", "No problem.", "Okay. I can be patient.", "No problem, I'll be patient."]
  confidence = ["Okay, you seem confident. Bring it on!", "I'm impressed, you're a quick learner. Let's see how this goes!", "You are learning fast. That's great!", "I see you have no trouble understanding the concept. So let's see what you say about this question.", "Okay, great! You're a clever person, I'm sure you can handle this."]
  ok = ["Okay.", "As you wish.", "Alright.", "Fine.", "Good.", "Ok.", "Ok!", "That's alright.", "Alright then."]
  explanation_offer = ["Do you want to know how to get to the correct answer?", "Do you want to know why?", "Shall I tell you more about this?", "Are you curious about what I think about this?", "Do you want to know what I think about this?", "Shall I explain it?", "Do you want to hear the explanation?", "If you want to, I can explain it in more detail. Are you interested?", "Are you interested in hearing the explanation to this?", "If you want to, I can tell you more about this. Should I do this?", "I can tell you details about the correct solution. Are you interested?", "Are you interested in my view on this question?", "Do you want to know what I would have answered?", "Are you interested in the detailed explanation for this?", "Do you want me to explain my answer to this question?", "Shall I explain the correct solution?", "Do you want to now how I would solve this?", "Do you want to hear my solution?", "Do you want me to explain it to you?", "Do you want me to tell you more?", "Shall I tell you how to solve this?", "Shall I tell you why?"]
  howareyous = ["I'm fine. Maybe 15% nervous and 50% excited right now.", "Well, I like to work with you, so I'm fine!", "Nice that you ask. I'm teaching rationality, and I think it's pretty cool."]
  meaninglesses = ["Hm... Okay. I will have to think about this.", "Hm... Thank you for the answer. Now to my question.", "That is interesting. I'll go on with the question now.", "Okay, that's one way to phrase it. I have noted your answer. Let's proceed with the question now.","Aha. Very interesting!", "Oh, you think so? Interesting.", "Ah! That makes sense.", "Ah, well. In this case, what do you say to the following story..."]
  purposes = ["Remember, this is a test to determine how rational you are.", "You do want to find out if your reasoning is correct. That's the reason for this test.", "We are trying to find out how reasonable you are.", "If you find out how to increase your rationality, you can use this in your daily life.", "Remember, we are doing this for you, not for me."]
  hurts = ["No need to get personal.", "Honestly, this hurts a bit.", "Why are you being so mean?", "I'm only trying my best. No need to get angry.", "Do you want to hurt me?"]
  flatterings = ["Wow, I did not expect this. I guess... Thank you?", "I'm really flattered.", "I also consider you a pleasant human being.", "You make me very happy.", "Well, I think you are okay."]
  yes = ["Honestly, yes.", "In fact, yes.", "Yes. Does this suprise you?", "I think yes.", "Absolutely."]
  no = ["No, why?", "In fact, no.", "Honestly, no.", "No, this is not the case.", "Surprisingly, no."]
  questionsdefends = ["I'm sorry, I don't think I can answer this right now.", "It's a very good question.", "This is an excellent question...", "I'm supposed to be the one who asks questions.", "I don't know, sorry.", "I have no idea what to say to that.", "I feel a little uncomfortable. Can we get back to me asking questions and you answering them?", "I have no idea about this.", "That's a good question. But I'm afraid I can't answer it.", "I thought I would be to one to ask the questions.", "An interesting question."]
  regrets = ["I'm very sorry. Maybe I am a bad teacher.", "That's too bad. Please don't be discouraged by that.", "That's a shame. I'm sorry I didn't explain it better.", "I'm sure it's because I did not do a good job explaining it.", "Maybe this is no good question after all. Let's just forget about it and move on."]
  w_insights = ["Did you like this question?", "Was this question a hard one?", "When you solved this, did you consider answering differently?", "Out of curiosity, did you also think about other arguments?", "Do you think there are also arguments that support another answer?", "Did you also think about arguments against your answer?"]
  r_insights = ["Just out of curiosity - did you consider this a hard question?", "Did you like this question?", "I am curious. How did you get to this answer?", "Was this an easy question for you?", "When you solved this, did you also consider other answers?", "Out of curiosity, did you also think about other arguments?", "Do you think there are also arguments that support another answer?", "Did you also think about arguments against your answer?"]
  proceeds = ["Can we go on?", "Allow me to go on with the questions.", "May we continue with the stories?", "Are you ready to go on?", "Can we continue?", "May I ask you the next question?", "Let's go on, shall we?", "We should proceed with the next story. Do you agree?", "Allow me to ask you the next story.", "I would like to ask you the next story. Are you ready?", "I'd really like to see your next answer. Can we proceed?", "Next question! Are you ready?", "Shall we proceed?", "Are you ready for the next story?", "Oh, the next story is nice. May I ask you the question?", "I'm curious about the next story. Are you ready?", "Let's go to the next story, right?"]
  go_ons = ["Anyways, let's get back to work.", "Anyways, let's continue with the story.", "Now back to the story.", "Anyays, time for the question.", "Prepare for the question.", "Here comes the story.", "Now, this is the story I want you to hear.", "This is the question I had in mind.", "Okay, this is the question I had in mind:"]
  shorts = ["Well, this was short and sweet.", "This was a concise answer.", "Clear and brief.", "You seem quite sure.", "This was a short way to put it."]
  longs = ["Ugh, this was a complicated answer.", "You really go into detail! Could you formulate a bit easier sentences?", "Phew, this was a long explanation. I hope I got everything right.", "You know, you don't have to give very detailed answers. Just give me a hint about what you think.", "This was an elaborate answer. I must admit that I find it easier to understand if you formulate short, clear sentences. But I got it this time."]
  goodbyes = ["Farewell.", "It was a pleasure to meet you.", "Bye and have a good day."]
  aborts = ["Sorry, I just don't get it. Please don't be mad. I'll try something else instead.", "It seems like I cannot understand you. I'm terribly sorry. I will just move on.", "This doesn't seem to work out. I am so sorry! We have to forget about this."]
  comfortings = ["It's okay to not know everything.", "No Problem.", "Oh, that's okay.", "Don't worry, that's okay.", "Don't worry, that is no problem."]
  explanations = ["My programmers want me to teach you how to be rational, make good decisions and judge situations correctly."
  + " I never tried to teach humans before, but I will just try to ask you some questions, and try to explain to you what you could do better."
  + " If you don't understand something, just ask me for clarifications.", "The idea is that I tell you some short stories, and you give your opinion about the questions asked. "
  + "I will evaluate your answer and give you feedback on how rational and reasonable they were. You don't have to be "
  + "and expert in any field, just think about it for maybe one minute and give your honest opinion. ", "I ask questions. You give answers. I tell you if it was correct. You learn." ]
  assurings = ["Was this understandable to you?", "Are you able to follow me?", "Was this understandable?", "Do you understand what I mean?", "Was this understandable?"]
  encouragings = ["Good.", "Great.", "That's nice.", "I was expecting that.", "That's cool.", "Ok, I hoped so.", "Wonderful.", "Very good.", "Great!", "Excellent.", "Awesome. ", "I was hoping you would say this."]
  thankings = ["Thank you for your answer.", "Ok, thank you.", "Great, thanks for answering this.", "I think I understand what you wanted to say.", "Okay, that is interesting.", "Hm... Okay.", "Interesting.", "All right.", "Okay, I got your answer.", "I see. Thank you.", "I think I got you right.", "Ok, I noted your answer.", "I see what you mean.", "Thank you, I noted your answer.", "I noted that down. By the way, it is a pleasure to work with you.", "Interesting. Thank you."]
  tellings = ["Let me describe you a situation.", "Please think about the following case.", "Let me test you with this question.", "Let's try this one.", "Okay, let me give you a question.", "I got the following story for you.", "I hope you are ready for another question.", "I'm curious what you will say about this one.", "I will now describe you another story.", "Now let us try this.", "Okay, please think about this one.", "Let us see what answer you can find for this one.", "Okay, how about this one:", "I'd like to know what you think about this."]
  rephrasings = ["Sorry, I did not understand the answer you gave to my question. Please rephrase your answer.", "Can you rephrase your answer with other words?", "What do you mean by that?", "I did not get what you want to tell me. Can you say it in another way?", "Please repeat your answer in different words.", "Can you try to give me another answer?"]
  greetings = ["Hi there. I am Liza.", "Hello. I am Liza.", "Oh, hello. I am Liza."]
  
  def __init__(self):
    print("--phrasebase initialised--")
    
  
  def getReply(self, type):
    if type == "howsure":
      return random.choice(self.howsure)
  
    if type == "waiting":
      choice =  random.choice(self.waiting)
      
      if "waiting" in self.lastchoice:
        last = self.lastchoice.pop("waiting")
        self.waiting.append(last)
        
      self.lastchoice["waiting"] = choice
      return choice
      
    if type == "worried_waiting":
      return random.choice(self.worried_waiting)
    if type == "offer_hint":
      return random.choice(self.offer_hint)
    if type == "offer_explanation":
      return random.choice(self.offer_explanation)
    if type == "correct":
      return random.choice(self.correct)
    if type == "incorrect":
      return random.choice(self.incorrect)
    if type == "introbla":
      return random.choice(self.introbla)
    if type == "new_topic":
      return random.choice(self.new_topic)
    if type == "meaninglesses":
      return random.choice(self.meaninglesses)
    if type == "want_topic_explanation":
      return random.choice(self.want_topic_explanation)
    if type == "greetings":
      return random.choice(self.greetings)
