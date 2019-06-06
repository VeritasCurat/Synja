import unittest
from selenium import webdriver
import time
import random
import string

from threading import Thread

def randomString(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

tb = ["Programmstruktur", "Grundlagen", "Arrays", "Operatoren", "Anweisungen", "Kontrollstrukturen", "Methoden", "Klassen"]

class SynjaCheckmanTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('C:\\Users\\Johannes\\Desktop\\Websitetester\\chromedriver.exe')
        #self.driver.get('http://141.20.25.57/synja')
        self.driver.get('http://127.0.0.1/synja_de')
        '''
        self.driver.implicitly_wait(1)
        log_name = self.driver.find_element_by_id("login_username")
        log_pass = self.driver.find_element_by_id("login_password")
        log_name.send_keys("Checkman")
        log_pass.send_keys("checkman")
        self.driver.find_elements_by_id("login")[1].click()
        self.driver.implicitly_wait(3)
        self.driver.find_element_by_id("aufgaben_loesen").click()
        '''

    def test_check_long_emit_text(self):
        emit_dialog = self.driver.find_element_by_id("emit_dialog")
        self.driver.implicitly_wait(1)
        for i in range(100):
            emit_dialog.send_keys(randomString(i))
            emit_dialog.submit()
            self.driver.implicitly_wait(1)

    def test_check_long_dialog_with_always_random_answer_in_Programmstruktur(self):
        emit_dialog = self.driver.find_element_by_id("emit_dialog")
        self.driver.implicitly_wait(1)
        emit_dialog.send_keys("Hi")
        emit_dialog.submit()
        time.sleep(1)
        while"Klassen"not in self.driver.page_source:
            self.driver.implicitly_wait(1)
        emit_dialog.send_keys(random.choice(tb))
        emit_dialog.submit()
        while "Klassen" not in self.driver.page_source:
            self.driver.implicitly_wait(1)
        emit_dialog.send_keys(random.choice(tb))
        emit_dialog.submit()
        time.sleep(1)
        for i in range(10000):
            emit_dialog.send_keys(randomString(i))
            emit_dialog.submit()
            time.sleep(1)

    def test_check_long_dialog_with_always_nein_in_Programmstruktur(self):
        emit_dialog = self.driver.find_element_by_id("emit_dialog")
        self.driver.implicitly_wait(1)
        emit_dialog.send_keys("Hi")
        emit_dialog.submit()
        time.sleep(1)
        while "Programmstruktur" not in self.driver.page_source:
            self.driver.implicitly_wait(1)
        emit_dialog.send_keys(random.choice(tb))
        emit_dialog.submit()
        time.sleep(1)
        for i in range(10000):
            if(i%5==0):emit_dialog.send_keys("ja")
            else:emit_dialog.send_keys("nein")
            emit_dialog.submit()
            time.sleep(1)

    def tearDown(self):
        #self.driver.find_element_by_id("logout").click()
        self.driver.close()
        
def MyThread():
    unittest.main()

if __name__ == "__main__":
  for i in range(1):
    thread = Thread(target = MyThread)
    thread.start()
    #thread.join()
    #print("thread finished...exiting")
