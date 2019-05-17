'''
Created on 17.05.2019

@author: Johannes
Problem: RASA NLU kann teilweise sogar nicht trainingsdaten zu intents parsen (>40%)
         Beispiel: 'intent': {'name': 'gruss', 'confidence': 0.344466498747804}, 'entities': [], 'text': 'hi'}
Bildet die trainingsdaten auf intents ab.
'''
import os
import io
import json
verzeichnispfad = os.path.realpath(__file__)

class simpleNLU(object):
    intentreg = {}
    
    def toleranz(self, text):
      text = text.lower()
      text = text.replace(",", "")
      text = text.replace(".", "")
      text = text.replace(";", "")
      text = text.replace("!", "")
      text = text.replace("?", "")
      text = text.replace(" ", "")
      return text
      
    def toleranzpruefung(self,text):
      text = self.toleranz(text)
      if(text in self.intentreg.keys()):
        return self.intentreg[text]
      else: return ""
    
    def laden(self):
      path = os.path.join(os.path.dirname(verzeichnispfad), 'nlu', 'training.json')
      with open(path) as f:
        data = json.load(f)['rasa_nlu_data']['common_examples']
        for l in data:
          self.intentreg[self.toleranz(l['text'])] = l['intent']
         


    def __init__(self):
      self.laden()
