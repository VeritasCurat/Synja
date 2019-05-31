'''
Created on 30.05.2019

@author: Johannes
'''
import urllib
import time
import threading
from urllib.request import urlopen

import requests #imports requests module. You need this to perform requests.

class stresstester(threading.Thread):
  id = 0
  
  def __init__(self,id):
    super(stresstester, self).__init__()
    self.id= id
    
  def run(self):
    self.stresstest_connect()
  
  def stresstest_connect(self):
    times=0
    start = time.time()
    while(True):
      sitedata=requests.get("http://141.20.25.57/synja")
     # print(sitedata.content )#prints html content of google.
      times += 1
      end = time.time()
      if(end - start > 1):
        print(str(self.id)+": "+str(times))
        times = 0
        end = start
      #print(times)
  
  def stresstest_open(self):
    times=0
    start = time.time()
    while(True):
      html = urlopen("http://141.20.25.58")
      html2 = urlopen("http://141.20.25.57")
      times += 1
      end = time.time()
      print(end - start)
      print(times)
      
    #<print(html2)


if __name__ == '__main__':
  for i in range(200):
    st = stresstester(i)
    st.start()
  
  #print(html.read())