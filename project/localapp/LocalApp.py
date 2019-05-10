'''
Created on 31.01.2019

@author: Johannes
'''

# qt5_ex.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFrame, QTextEdit, QScrollBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, QRect
from PyQt5 import *

from project.localapp.SynjaLocal import Synja
from twisted.conch.insults.window import HorizontalScrollbar
from PyQt5.Qt import QTextBrowser


class LocalApp(QWidget):
  synja = Synja()
  dialog = "Synja: "+synja.ersteAusgabe()+"\n"
  app=0
  dialogeingabefeld = object
  dialogfeld = object
  lehrfeld = object
  imagelabel = object
  name = ""
  
  def __init__(self, title="Synja"):
    super().__init__() # inherit init of QWidget
    self.title = title
    self.left = 100
    self.top = 100
    self.width = 1200
    self.height = 800
    self.widget()  
    self.name = "User"
    

    
  def lehrebene_darstellung(self):
    #Lehrebene:  Frame und Label
    self.lehrebene = QFrame(self)
    self.lehrebene.setGeometry(QRect(0, 0, 800, 800))
    
    self.label1 = QLabel(self.lehrebene, text="teaching")
    # margin: left, top; width, height
    self.label1.setGeometry(QRect(20, 0, 100, 50))
    self.label1.setWordWrap(True) # allow word-wrap
    
    #add textfield to display contents of teaching
    self.lehrfeld = QTextBrowser(self.lehrebene)
    self.lehrfeld.setFontPointSize(12)
    self.lehrfeld.setText(self.synja.outputLehre)
    self.lehrfeld.setGeometry(QRect(20, 50, 750, 500))
    
    #add textfield for answering
    self.antwortfeld = QTextEdit(self.lehrebene)
    self.antwortfeld.setFontPointSize(12)
    self.antwortfeld.setText("")
    self.antwortfeld.setGeometry(QRect(20, 570, 750, 150))
    
    #add button: submit solution
    self.loesungsbutton = QPushButton(self.lehrebene, text="submit solution")
    self.loesungsbutton.setGeometry(QRect(20, 730, 200, 50))
    self.loesungsbutton.clicked.connect(self.lehreingabe)
    
  def dialogebene_darstellung(self):
    #Dialogebene:  Frame, Label, Textfeld, Eingabefeld, Buttons
    self.dialogebene = QFrame(self)
    self.dialogebene.setGeometry(QRect(800, 0, 400, 800))
    
    self.labelde = QLabel(self.dialogebene, text="dialog")
    # margin: left, top; width, height
    self.labelde.setGeometry(QRect(20, 0, 100, 50))
    self.labelde.setWordWrap(True) # allow word-wrap
    
    #add textfield to display messages
    self.dialogfeld = QTextBrowser(self.dialogebene)
    self.dialogfeld.setFontPointSize(12)
    self.dialogfeld.setText(self.dialog)
    self.dialogfeld.setGeometry(QRect(0, 50, 400, 450))
    
    #add textfield for input
    self.dialogeingabefeld = QTextEdit(self.dialogebene)
    self.dialogeingabefeld.setFontPointSize(12)
    self.dialogeingabefeld.setGeometry(QRect(0, 520, 400, 200))

    #add button: submit message
    self.submitbutton = QPushButton(self.dialogebene, text="submit message")
    self.submitbutton.setGeometry(QRect(0, 730, 200, 50))
    self.submitbutton.clicked.connect(self.dialogeingabe)
    

  def widget(self):
    # window setup
    self.setWindowTitle(self.title)
    # self.setGeometry(self.left, self.top, self.width, self.height)
    ## use above line or below
    self.resize(self.width, self.height)
    self.move(self.left, self.top)
    self.lehrebene_darstellung()
    self.dialogebene_darstellung()
    self.show()
    
  @pyqtSlot()
  def dialogeingabe(self):
    self.dialogeingabefeld.setFontPointSize(12)
    #if(str(self.dialogeingabefeld.text()=="")):return
    inputUser = str(self.dialogeingabefeld.toPlainText())    
        
    self.synja.schritt(inputUser, "")
    if(self.synja.name != self.name and self.synja.name != ""): 
      self.name = self.synja.name
    
    self.dialog +=  self.name+": "+inputUser+"\n"
    self.dialogfeld.setText(self.dialog)
    self.dialogeingabefeld.setText("")
    
    
    for s in self.synja.outputDialog: self.addDialogSynja(s)
    if(self.synja.outputLehre != None):
        print("LA: "+str(self.synja.outputLehre))
        print("LA: "+str(self.synja.outputLehre.lesson))
        print("LA: "+str(self.synja.outputLehre.konzeptname))
        print("LA: "+str(self.synja.outputLehre.darstellungsart))
        print("LA: "+str(self.synja.outputLehre.version))

        self.addLehreSynjaText(self.synja.outputLehre)
    
    self.synja.outputLehre = None
    self.synja.outputDialog = []
    
    
  def lehreingabe(self):
    if(self.synja.lehrmanager.zustand=="testphase_konzept" or self.synja.lehrmanager.zustand=="testphase_block"): 
      #Auswertung nutzereingabe
      antworttext = str(self.antwortfeld.toPlainText())
      print(antworttext)
      lesson = self.synja.lehrmanager.lesson
      konzeptname = self.synja.lehrmanager.konzept
      art = self.synja.lehrmanager.art
      version = self.synja.lehrmanager.version
      bewertung = self.synja.expertenmodell.bewerten(lesson, konzeptname, art, version, antworttext)
      print("LA bewertung: "+bewertung)
      
      self.synja.schritt("",bewertung)
     
      for s in self.synja.outputDialog: 
        print("ausgabe: "+s)
        self.addDialogSynja(s)
            
      self.antwortfeld.setText("")
      if self.synja.outputLehre!= None: 
        self.addLehreSynjaText(self.synja.outputLehre)  
        
        
      self.synja.outputDialog = []
      self.synja.outputLehre = None

    
  def addDialogSynja(self, text):
    self.latestUserInput = text
    self.dialog +=  "Synja: "+text+"\n"
    self.dialogfeld.setText(self.dialog) 
    
    if(self.dialogfeld.verticalScrollBar() != None):
      self.dialogfeld.verticalScrollBar().setValue(200000000);
    
  
  def addLehreSynjaText(self, lehrausgabe):
    #konzeptname, darstellungsart, version, nutzerid
    ausgabe = self.synja.expertenmodell.zugriffLehreinheit(lehrausgabe.lesson, lehrausgabe.konzeptname, lehrausgabe.darstellungsart, lehrausgabe.version)
    self.lehrfeld.setText(str(ausgabe))   
     
     
     
  def test_lehrdaten(self):
    self.synja.displayAll()
    ausgabe = ""
    for l in self.synja.outputLehreTest:
      ausgabe += "\n\n"+l
      self.lehrfeld.setText(str(ausgabe))
    
app = QApplication(sys.argv) 
widget = LocalApp()
sys.exit(app.exec_()) 