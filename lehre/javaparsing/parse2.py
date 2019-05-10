import subprocess
import os


verzeichnispfad = os.path.realpath(__file__)[:-9]

def checkCompile(java_file):
  cmd = verzeichnispfad+java_file
  #proc = subprocess.Popen(cmd, shell=True).args,
  try:
    process = subprocess.Popen(["java", cmd], stdout = subprocess.PIPE)
    print(process.communicate())
  except subprocess.CalledProcessError as e:
    print(e.output)
    return False
  return True

def compile_java(java_file):
  cmd = verzeichnispfad+java_file
  #proc = subprocess.Popen(cmd, shell=True).args,
  try:
    process = subprocess.Popen(["javac", cmd], stdout = subprocess.PIPE)
    print(process.communicate())
  except subprocess.CalledProcessError as e:
    print(e.output)
    return False
  return True

checkCompile("Test.class")
  