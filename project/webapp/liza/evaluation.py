class Evaluation:
  def __init__(self, topiclist, praise, criticism):
    self.topiclist = topiclist
    self.max = len(topiclist)
    print("I exist!" + str(len(topiclist)))
    self.correct = {}
    self.incorrect = {}
    self.calibrationPOS = 0
    self.calibrationPOS_nr = 0
    self.calibrationNEG = 0
    self.calibrationNEG_nr = 0
    self.praise = praise
    self.criticism = criticism
    
  def calibrate(self,correctness,percentage):
  #  print(percentage)
    if correctness:
      self.calibrationPOS = self.calibrationPOS + percentage
      self.calibrationPOS_nr += 1
    else:
      self.calibrationNEG = self.calibrationNEG + (100-percentage)
      self.calibrationNEG_nr += 1
  #  print(self.calibrationPOS)
  #  print(self.calibrationPOS_nr)
  #  print(self.calibrationNEG)
  #  print(self.calibrationNEG_nr)
 
  def answer(self, story, correct):
    #print("So was the story answered correctly?" + str(correct))
    print("type of story: " + str(story.group) + " " +str(correct))
    
    
    if(correct):
      if story.group in self.correct:
        self.correct[story.group] += 1
      else:
        self.correct[story.group] = 1
    else:
      if story.group in self.incorrect:
        self.incorrect[story.group] += 1
      else:
        self.incorrect[story.group] = 1
        
  def evaluate(self):
    #print("evaluation!")
    poscal = 0
    negcal = 0
    if (self.calibrationPOS_nr > 0):
      poscal = self.calibrationPOS * 1.0 / (self.calibrationPOS_nr * 1.0)
    if (self.calibrationNEG_nr > 0):
      negcal = self.calibrationNEG * 1.0 / (self.calibrationNEG_nr * 1.0)
    
    eval = []
    
    print("Calibration for correct things: " + str(poscal))
    print("Calibration for negative things: " + str(negcal))
   
    for x in range(0,self.max):
      if x in self.correct or x in self.incorrect:
        c = 0 #number story x was correct
        i = 0 #number story x was incorrect
        if x in self.correct:
          c = self.correct[x]
        if x in self.incorrect:
          i = self.incorrect[x]
        
        percentage = 100* (c*1.0) / ((c+i)*1.0)
        eval.append("In questions of type \"" + self.topiclist[x]+ "\", you answered " + str(percentage) + "% of the questions correctly.")
        if (percentage > 0.7):
          eval.append(self.praise[x])
        if (percentage < 0.3):
          eval.append(self.criticism[x])
    eval.append("It is not only important to know the right answers, but also to have a clear understanding of one's own capabilities and uncertainties.")
    
    
    if ((poscal > 70 or (self.calibrationPOS_nr == 0))and (negcal > 70 or (self.calibrationNEG_nr == 0))):
      eval.append("Your calibration is very high! That means that you are awesome at judging how likely it is that you are right. Very good!")
    elif ((poscal > 50 or (self.calibrationPOS_nr == 0)) and (negcal > 50 or (self.calibrationNEG_nr == 0))):
      eval.append("Your calibration is high. That means you are good at judging how likely it is that you are right. But you can still improve.")
    
    if((poscal < 50 and self.calibrationPOS_nr > 0) and (negcal < 50 and self.calibrationNEG_nr > 0)):
      eval.append("You seem quite confused. You should obverse your own results some more.")
    else:
      if(poscal < 50 and self.calibrationPOS_nr > 0):
        eval.append("Sometimes you are right about things, but don't seem to trust in your own abilities. Be a little more confident!")
      if(negcal < 50 and self.calibrationNEG_nr > 0):
        eval.append("Sometimes you are very confident, but you are not actuall right. You should questions your abilities more.")
      
    
    return eval