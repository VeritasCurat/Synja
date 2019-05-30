
import os
#TODO
#import bcrypt

class Usergate():
  
  verzeichnispfad = os.path.realpath(__file__)[:-21]
  
  usrdata = {}
  usrProgress = {}
  
  
  def __init__(self):
    #print("lade usergate")
    #bekannteLessons = open(self.verzeichnispfad+"webapp\\usergate\\bekannteLessons.txt", encoding ='ISO-8859-1')
    path = os.path.join(os.path.abspath(self.verzeichnispfad), 'usergate','logindata.txt')
    logindata = open(path)
    line = ""
    while(True):
      line = logindata.readline()
      if(line == "" or line == '\n'): break
      data = line.split(':')
      if '\n' in data[1]:
        self.usrdata[data[0]] = data[1][:-1]
      else: self.usrdata[data[0]] = data[1]
    return
  

  def saveUsrLogin(self):
    path = os.path.join(os.path.abspath(self.verzeichnispfad),'usergate','logindata.txt')
    logindata = open(path, 'w')    
    for user in self.usrdata.keys():
      print(user)
      logindata.write(str(user+":"+str(self.usrdata[user]))+'\n')
        
  def saveUserProgress(self):
    path = os.path.join(os.path.abspath(self.verzeichnispfad),'usergate','usrprogress.csv')
    progressdata = open(path, 'w')
    for user in self.usrProgress.keys():
      print(user)
      progressdata.write(str(user+": "+str(self.usrProgress[user]))+'\n')
    
  def checkLogin(self, name, password):
    if(name in self.usrdata.keys()):
      if(self.usrdata[name] == password):
      #if bcrypt.hash_pw(password, self.usrdata[name]) == self.usrdata[name]:
        return True 
    return False
      
    
  def createUser(self, name, password):
    #pw = 'u'+password
    #salt = bcrypt.gensalt()
    #password_hashed = bcrypt.hashpw(pw,salt)
    
    for givenname in self.usrdata.keys():
      if(givenname == name):
        return False
    self.usrdata[name] = password#password_hashed
    self.usrProgress[name] = []
    self.saveUserProgress()
    self.saveUsrLogin()
    return True
  
  def checkProgress(self, name):
    if(name in self.usrProgress.keys()):
      return self.usrProgress[name]
    else: return None
    
  def enterProgress(self, name, lesson):
    if(name not in self.usrProgress.keys()):return False
    for Lesson in self.usrProgress[name]:
      if(lesson in Lesson):return
    self.usrProgress[name].append(str(lesson))
    self.saveUserProgress()
   

