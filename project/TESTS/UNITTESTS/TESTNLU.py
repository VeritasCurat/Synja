'''
Created on 27.04.2019

@author: Johannes
'''
import unittest
from project.dialog.NLU import NLU


class Test(unittest.TestCase):


  @staticmethod
  def test_nlu():
    nlu = NLU("en")
    i = 0
    if(nlu.parse( "bye") != "verabschiedung"):raise AssertionError("verabschiedung")
    if(nlu.parse( "good bye") != "verabschiedung"):raise AssertionError("verabschiedung")
    if(nlu.parse( "bye synja") != "verabschiedung"):raise AssertionError("verabschiedung")
    if(nlu.parse( "lets end this session") != "verabschiedung"):raise AssertionError("verabschiedung")
    #if(nlu.parse( "lets finish tommorow") != "verabschiedung"):raise AssertionError("verabschiedung")
    if(nlu.parse( "let us continue next week") != "verabschiedung"):raise AssertionError("verabschiedung")
    if(nlu.parse( "i want to exit") != "verabschiedung"):raise AssertionError("verabschiedung")
    if(nlu.parse( "i want to go now") != "verabschiedung"):raise AssertionError("verabschiedung")
    if(nlu.parse( "this is enough lets end this") != "verabschiedung"):raise AssertionError("verabschiedung")
    if(nlu.parse( "enough for today") != "verabschiedung"):raise AssertionError("verabschiedung")
    if(nlu.parse( "lets quit this") != "verabschiedung"):raise AssertionError("verabschiedung")
    
    if(nlu.parse( "i know") != "verstanden"):raise AssertionError("verstanden")
    if(nlu.parse( "i get it") != "verstanden"):raise AssertionError("verstanden")
    if(nlu.parse( "i understand") != "verstanden"):raise AssertionError("verstanden")
    if(nlu.parse( "i get the idea") != "verstanden"):raise AssertionError("verstanden")
    if(nlu.parse( "i understood the concept") != "verstanden"):raise AssertionError("verstanden")
    if(nlu.parse( "sure") != "verstanden"):raise AssertionError("verstanden")
    if(nlu.parse( "this is clear") != "verstanden"):raise AssertionError("verstanden")
    if(nlu.parse( "i got it") != "verstanden"):raise AssertionError("verstanden")

    if(nlu.parse( "my name is john") != "name"):raise AssertionError("name")
    if(nlu.parse( "its bob") != "name"):raise AssertionError("name")
    if(nlu.parse( "im anna") != "name"):raise AssertionError("name")
    if(nlu.parse( "im called marie") != "name"):raise AssertionError("name")
    if(nlu.parse( "hi im michael") != "name"):raise AssertionError("name")
    if(nlu.parse( "yeah its tom") != "name"):raise AssertionError("name")
    if(nlu.parse( "oh hi im gustav") != "name"):raise AssertionError("name")
    if(nlu.parse( "hey there im alex") != "name"):raise AssertionError("name")
    
    if(nlu.parse( "i don't know") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "i dont get it") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "i understood the concept") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "i have a problem to understand this") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "this confuses me") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "that is diffcult to grasp") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "what is this?") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "i dont know what to do") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "what next?") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "i forgot") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "i dont remember") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "i dont know") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "i cant remember") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "what is this?") != "weiss_nicht"):raise AssertionError("weiss_nicht")
    if(nlu.parse( "what does this mean?") != "weiss_nicht"):raise AssertionError("weiss_nicht")
 
    if(nlu.parse( "my name is ") != "begruessung"):raise AssertionError("begruessung")
    if(nlu.parse( "hi there") != "begruessung"):raise AssertionError("begruessung")
    if(nlu.parse( "hello synja") != "begruessung"):raise AssertionError("begruessung")
    if(nlu.parse( "hi synja it is very nice to meet you") != "begruessung"):raise AssertionError("begruessung")
    if(nlu.parse( "nice to meet you") != "begruessung"):raise AssertionError("begruessung")
    if(nlu.parse( "hi") != "begruessung"):raise AssertionError("begruessung")
    if(nlu.parse( "good morning") != "begruessung"):raise AssertionError("begruessung")
    if(nlu.parse( "grussings") != "begruessung"):raise AssertionError("begruessung")
    if(nlu.parse( "hi synja") != "begruessung"):raise AssertionError("begruessung")
    if(nlu.parse( "hey there synja") != "begruessung"):raise AssertionError("begruessung")
    if(nlu.parse( "good day") != "begruessung"):raise AssertionError("begruessung")
    if(nlu.parse( "hey there") != "begruessung"):raise AssertionError("begruessung")
  
    if(nlu.parse( "yes") != "ja"):raise AssertionError("ja")
    if(nlu.parse( "i accept") != "ja"):raise AssertionError("ja")
    if(nlu.parse( "yes i do") != "ja"):raise AssertionError("ja")
    if(nlu.parse( "sure") != "ja"):raise AssertionError("ja")
    if(nlu.parse( "go") != "ja"):raise AssertionError("ja")
    if(nlu.parse( "thats right") != "ja"):raise AssertionError("ja")
    if(nlu.parse( "right") != "ja"):raise AssertionError("ja")
    if(nlu.parse( "i think so") != "ja"):raise AssertionError("ja")
    if(nlu.parse( "definitly") != "ja"):raise AssertionError("ja")
    if(nlu.parse( "oh yes") != "ja"):raise AssertionError("ja")
    if(nlu.parse( "i would think so") != "ja"):raise AssertionError("ja")
    if(nlu.parse( "that works") != "ja"):raise AssertionError("ja")
    
    if(nlu.parse( "no") != "nein"):raise AssertionError("nein")
    if(nlu.parse( "no i didnt") != "nein"):raise AssertionError("nein")
    if(nlu.parse( "false") != "nein"):raise AssertionError("nein")
    if(nlu.parse( "i dont want to") != "nein"):raise AssertionError("nein")
    if(nlu.parse( "decline") != "nein"):raise AssertionError("nein")
    if(nlu.parse( "not now") != "nein"):raise AssertionError("nein")
    if(nlu.parse( "thats wrong") != "nein"):raise AssertionError("nein")
    if(nlu.parse( "wrong") != "nein"):raise AssertionError("nein")
    if(nlu.parse( "that doesnt work") != "nein"):raise AssertionError("nein")
    if(nlu.parse( "that doesnt fit") != "nein"):raise AssertionError("nein")
    if(nlu.parse( "i dont think so") != "nein"):raise AssertionError("nein")   
   
    if(nlu.parse( "what is syntax?") != "QTeaching"):raise AssertionError("teaching")
    if(nlu.parse( "what can you teach me?") != "QTeaching"):raise AssertionError("teaching")
    if(nlu.parse( "how can you help me?") != "QTeaching"):raise AssertionError("teaching")
    if(nlu.parse( "what can i learn?") != "QTeaching"):raise AssertionError("teaching")
    if(nlu.parse( "how can you help me?") != "QTeaching"):raise AssertionError("teaching")
    if(nlu.parse( "how does the teaching work?") != "QTeaching"):raise AssertionError("teaching")
    if(nlu.parse( "how do you teach?") != "QTeaching"):raise AssertionError("teaching")
        
    if(nlu.parse( "how does the ui work?") != "QUI"):raise AssertionError("ui")
    if(nlu.parse( "where should i type?") != "QUI"):raise AssertionError("ui")
    if(nlu.parse( "where should i click?") != "QUI"):raise AssertionError("ui")
    if(nlu.parse( "where is it displayed?") != "QUI"):raise AssertionError("ui")
    if(nlu.parse( "how to answer?") != "QUI"):raise AssertionError("ui")
    if(nlu.parse( "what did you say?") != "QUI"):raise AssertionError("ui")
    if(nlu.parse( "how can you understand me?") != "QUI"):raise AssertionError("ui")
    if(nlu.parse( "how do you hear me?") != "QUI"):raise AssertionError("ui")
    if(nlu.parse( "how is this dialog possible?") != "QUI"):raise AssertionError("ui")
    if(nlu.parse( "can you understand me?") != "QUI"):raise AssertionError("ui")
    
    if(nlu.parse( "how can you understand me?") != "QDialog"):raise AssertionError("gespraech")
    if(nlu.parse( "how can you understand what i wrote?") != "QDialog"):raise AssertionError("gespraech")
    if(nlu.parse( "how can we write?") != "QDialog"):raise AssertionError("gespraech")
    if(nlu.parse( "which topics can i choose from?") != "QDialog"):raise AssertionError("gespraech")
    

    pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()