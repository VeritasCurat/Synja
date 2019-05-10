'''
Created on 22.01.2019

@author: Johannes
'''

class MultipleChoice(object):
    '''
    classdocs
    '''
    frage = ""
    antworten = ""
    loesungen = []
    name = ""

    def __init__(self, name, Frage, Antworten, Loesungen):
      self.name = name
      self.frage = Frage
      self.antworten = Antworten
      self.loesungen = Loesungen

        
    def beantworten(self, Loesungen):
      if(Loesungen == self.loesungen):
        return "richtig"
      else: 
        return "falsch"