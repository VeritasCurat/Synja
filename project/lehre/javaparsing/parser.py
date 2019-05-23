'''
Created on 08.03.2019
@author: Johannes Grobelski

@summary: Allgemeine Funktionsweise:
- jedem Syntaxkonzept werden verschiedene Codingaufgaben zugeordnet (z.B. if -> ifstatement (schreiben)); diese aufgaben werden jeweils in einer Funktion auf Syntax geprueft
- dabei kann allgemein in folgende fehlerklassen eingeteilt werden: allgemeine struktur falsch (per regex), subkonzept falsch (per funktionsaufruf) (z.b. boolean_expression in if statement), zugrifffehler (unbekannte var., falscher typ etc.)
- fehler werden als fehlercode (in form von string) mit 
'''

''' 
#folgende returns sind nicht explizit in parser.py aber in fehlerbeschreibung, fehlerreaktion und fehlerhinweis
replacereturns:
variable_definition: variable -> array
variable_definition: variable_definition -> variable_definition_initialization
variable_definition_initialization: variable -> array
variable_definition_initialization: variable_definition_initialization -> array_reassignment
variable_definition: variable -> multidim_array

#folgende funktionen tauchen als returns in anderen funktionen auf
functionreturns:
multiline_comment(eingabe)[0]
singleline_comment(eingabe)[0]
variable_definition(firstpart+";")[0]
assignops(eingabe,False)[0]
codeblock(body)[0]
classdefinition(eingabe)[0]

#folgende Werte koennen von einigen Funktionen weitergegeben werden, werden aber nicht von parse(..) zurueckgegeben
gettypereturns:
"Error"
"byte"
"short"
"int"
"long"
"float"
"double"
"boolean"
"char"
"String"
'''



import re
from builtins import isinstance
import token

whitespaces = [' ','\t'] 

keywords = ["abstract", "continue", "for", "new", "switch", "assert", "default", "if", "package", "synchronized", "boolean", "do", "goto", "private", "this", "break", "double", "implements", "protected", "throw", "byte", "else", "import", "public", "throws", "case", "enum", "instanceof", "return", "transient", "catch", "extends", "int", "short", "try", "char", "final", "interface", "static", "void", "class", "finally", "long", "strictfp", "volatile", "const", "float", "native", "super", "while"]
prim_types = ["byte", "short", "int", "long", "float", "double", "boolean", "char", "String"]


Compops = ["<", ">", "<=", ">=", "!=", "=="]
Arops = ["%", "+", "-", "/", "*"]
Bitops = ["|", "&", "~", "<<", ">>", ">>>"]
Logicops = ["||", "&&", "!","^"]
Assignops = ["=","%=","+=","-=","/=","*=","|=","&=","~=","<<=",">>=",">>>=","^=",]

integertypes = ["int", "char", "short", "long", "byte"]
floattypes = ["float", "double"]

accessmodifiers = ["public", "private", "protected"]

labellistdict = {} #Eintrag: name -> funktion
variablenliste = [] #Eintrag: name
variablenval = {} #var -> value
arrayval = {} #arr -> valuelist
variablentypdict = {} #Eintrag: name -> typ
arraylist = [] #Eintrag: name
arraytypdict = {} #Eintrag: name -> typ
arraydimdict = {} #Eintrag: name -> dimension
methodlist = [] #Eintrag: name
methodreturndict = {} #Eintrag: name -> returntype
methodmodifierdict = {} #Eintrag: name -> accessmod
methodparamtypelist = {} #Eintrag name ->[type1 .. typeN]
objectlist = [] #Eintrag: 
objecttoclassdict = {} #Eintrag: objectname -> classname
classlist = [] #Eintrag: classname
classmodifierdict = {}
classvariablendict = {} #Eintrag -> [Klassenvariablen (name)]
classmethodendict = {} #Eintrag ->[Klassenmethode (name)]

'''
#Anmerkung 1: viele der Patterns sind so komplex, weil alle gueltigen zusaetzlichen Leerzeichen beruecksichtigt wurden

'''

allreturns = ["integer_literal_non","array_reassignment_wrong_dim","multidim_array_access_oof","multidim_array_reassignment_oof","types_non","arithmetic_operators_no_operator","arithmetic_operators_wrong_numops","arithmetic_operators_wrong_structure","arithmetic_operators_wrong_type","array_access_no_declaration","array_access_outofrange","array_access_unknown_array","array_access_wrong_structure","array_declaration_no_brackets","array_declaration_no_new","array_declaration_non_indextype","array_declaration_non_type","array_declaration_wrong_semicolon","array_declaration_wrong_structure","array_declaration_wrong_type","array_definition_initialization_name_double","array_definition_initialization_no_brackets","array_definition_initialization_wrong_semicolon","array_definition_initialization_wrong_structure","array_definition_name_double","array_definition_no_brackets","array_definition_wrong_semicolon","array_definition_wrong_structure","array_no_declaration","array_reassignment_unknown_array","array_reassignment_wrong_structure",
              "array_unknown_array","assignment_operators_badLType","assignment_operators_no_operator","assignment_operators_wrong_numops","assignment_operators_wrong_structure","assignment_operators_wrong_type","bitwise_operators_no_operator","bitwise_operators_wrong_numops","bitwise_operators_wrong_structure","bitwise_operators_wrong_type","boolean_expression_non","boolean_literals_non","char_literal_non","class_definition_invalid_accessmodifier","class_definition_invalid_identifier","class_definition_no_access_mod","class_definition_no_curly_brackets","class_definition_no_keyword","class_definition_no_mod","class_definition_wrong_structure","class_illegal_classblock","codeblock_no_brackets","codeblock_no_statement","comments_multiline_wrong_structure","comments_non","comments_singleline_wrong_structure","comparison_operators_no_operator","comparison_operators_wrong_numops","comparison_operators_wrong_structure",
              "comparison_operators_wrong_type","constructor_definition_wrong_modifier","constructor_definition_wrong_name","constructor_wrong_body","constructor_wrong_structure","constructor_wrong_variable_definition","do_while_break","do_while_continue","do_while_curly_brackets_not_matching","do_while_no_boolean_expression","do_while_no_keyword","do_while_non_codeblock","do_while_round_brackets_not_matching","do_while_wrong_semicolon","do_while_wrong_structure","expression_non","extended_for_break","extended_for_continue","extended_for_no_keyword","extended_for_no_variable_definition","extended_for_nonarray","extended_for_noncode_block","extended_for_nonstatement","extended_for_varar_mismatch","extended_for_wrong_structure","float_literals_no_point","float_literals_wrong_structure","float_literals_wrong_prefix","for_break","for_continue","for_no_boolean_expression","for_no_increment","for_no_keyword","for_no_variable_definition","for_noncode_block",
              "for_nonstatement","for_wrong_structure","identifiers_digit","identifiers_keyword","identifiers_nonletter","identifiers_null_boolean","if_brackets_not_matching","if_no_boolean_expression","if_no_keyword","if_non_codeblock","if_non_statement","if_wrong_structure","import_error_wildcard","import_identifier","import_no_keyword","import_wrong_semicolon","import_wrong_structure","integer_literals_binary_not_empty","integer_literals_hex_not_empty","integer_literals_non_binary","integer_literals_non_decimal","integer_literals_non_hex","integer_literals_non_octal","integer_literals_byte_oor","integer_literals_short_oor","integer_literals_long_oor","integer_literals_int_oor","integer_literals_char_oor","keyword_non","literal_non","logic_operators_no_operator","logic_operators_wrong_numops","logic_operators_wrong_structure","logic_operators_wrong_type","main_wrong","member_access_methods_unknown_member","member_access_methods_unknown_object","member_access_methods_wrong_structure","member_access_non_member","member_access_variables_unknown_member",
              "member_access_variables_unknown_object","member_access_variables_wrong_structure","memberaccess_wrong_structure","method_access_parameter_mismatch","method_access_unknown_method","method_access_wrong_semicolon","method_access_wrong_structure","method_definition_no_identifier","method_definition_wrong_modifier","method_definition_wrong_return","method_definition_wrong_structure","method_definition_wrong_type","method_definition_wrong_variable_definition","method_defintion_no_mod","multidim_array_declaration_bracketnumber_not_matching","multidim_array_declaration_wrong_structure","multidim_array_definition_name_double","multidim_array_definition_no_brackets","multidim_array_definition_wrong_semicolon","multidim_array_definition_wrong_structure","multidim_array_access_no_declaration","multidim_array_access_outof_dim","multidim_array_access_wrong_structure","multidim_array_reassignment_no_declaration","multidim_array_reassignment_outof_dim","multidim_array_reassignment_unknown_array","multidim_array_reassignment_wrong_structure",
              "null_literal_non","package_indentifier","package_no_keyword","package_wrong_semicolon","package_wrong_structure","postincdec_no_operator","postincdec_wrong_structure","postincdec_wrong_type","preincdec_no_operator","preincdec_wrong_structure","preincdec_wrong_type","statement_non","statement_wrong_semicolon","string_literal_non","string_literals_non","switch_break","switch_curly_brackets_not_matching","switch_no_keyword","switch_non_variable","switch_round_brackets_not_matching","switch_varval_mismatch","switch_wrong_case","switch_wrong_default","switch_wrong_structure","variable_access_unknown","variable_access_wrong_structure","variable_definition_initialization_contructor_parameter_mismatch","variable_definition_initialization_contructor_parameter_mismatch_len","variable_definition_initialization_name_double","variable_definition_initialization_non_identifier",
              "variable_definition_initialization_non_type","variable_definition_initialization_typeclass_no_new","variable_definition_initialization_typemismatch_boolean","variable_definition_initialization_typemismatch_char","variable_definition_initialization_typemismatch_class","variable_definition_initialization_typemismatch_float","variable_definition_initialization_typemismatch_integer","variable_definition_initialization_typemismatch_string","variable_definition_initialization_wrong_semicolon","variable_definition_initialization_wrong_structure","variable_definition_name_double","variable_definition_non_identifier",
              "variable_definition_non_type","variable_definition_wrong_semicolon","variable_definition_wrong_structure","variable_reassignment_wrong_structure","while_brackets_not_matching","while_break","while_continue","while_no_boolean_expression","while_no_keyword","while_non_codeblock","while_non_statement","while_wrong_structure","variable_definition_contructor_parameter_mismatch", "array_definition_non_identifier", "array_definition_non_type", "array_definition_initialization_non_type", "array_definition_initialization_typemismatch_integer", "array_definition_initialization_typemismatch_float", "array_definition_initialization_typemismatch_boolean", "array_definition_initialization_typemismatch_char", "array_definition_initialization_typemismatch_string", "array_definition_initialization_wrong_type", "array_definition_initialization_typeclass_no_new", "array_definition_initialization_typemismatch_class", "array_definition_initialization_contructor_parameter_mismatch", 
              "multidim_array_access_unknown_array","array_definition_initialization_contructor_parameter_mismatch_len", "array_declaration_name_double", "array_reassignment_non_type", "array_reassignment_non_identifier", "array_reassignment_wrong_semicolon", "inheritance_non_parent","inheritance_wrong_structure", "array_reassignment_name_double", "array_reassignment_wrong_type", "array_reassignment_typemismatch_integer", "array_reassignment_typemismatch_float", "array_reassignment_typemismatch_boolean", "array_reassignment_typemismatch_char", "array_reassignment_typemismatch_string", "array_reassignment_typeclass_no_new", "array_reassignment_typemismatch_class", "array_reassignment_contructor_parameter_mismatch", "array_reassignment_contructor_parameter_mismatch_len", "multidim_array_definition_non_identifier", "multidim_array_definition_non_type", "class_definition_name_double","member_access_methods_wrong_structure"]

def rennew():
  global variablenliste
  global variablentypdict
  global arraylist
  global arraytypdict
  global arraydimdict
  global methodlist
  global methodreturndict
  global methodmodifierdict
  global methodparamtypelist
  global objectlist
  global objecttoclassdict
  global classlist
  global classmodifierdict
  global classvariablendict
  global classmethodendict

  variablenliste = [] #Eintrag: name
  variablentypdict = {} #Eintrag: name -> typ
  arraylist = [] #Eintrag: name
  arraytypdict = {} #Eintrag: name -> typ
  arraydimdict = {} #Eintrag: name -> dimension
  methodlist = [] #Eintrag: name
  methodreturndict = {} #Eintrag: name -> returntype
  methodmodifierdict = {} #Eintrag: name -> accessmod
  methodparamtypelist = {} #Eintrag name ->[type1 .. typeN]
  objectlist = [] #Eintrag: 
  objecttoclassdict = {} #Eintrag: objectname -> classname
  classlist = [] #Eintrag: classname
  classmodifierdict = {}
  classvariablendict = {} #Eintrag -> [Klassenvariablen (name)]
  classmethodendict = {} #Eintrag ->[Klassenmethode (name)]

'''
###########################################################################
HILFSFUNKTIONEN
###########################################################################
'''

def listToenumartion(List):
  if(isinstance(List, list) == False): return List
  elif(len(List)==0): return ""
  elif(len(List)==1): return List[0]
  ret = ""
  for el in List[:-2]:
    ret += el+", "
  return ret +List[-2]+" or "+List[-1]

def inel(var, var2):
  
  if(isinstance(var2,list) != True):
    if(isinstance(var,list) != True):
      return var == var2
  
  if(isinstance(var,list) != True):
    if(isinstance(var2,list) == True):
      return var in var2
    
  if(isinstance(var2,list) != True):
    if(isinstance(var,list) == True):
      return var2 in var
  else: return set(var).issubset(var2) or set(var2).issubset(var)

def listelinvar(List,var):
  for el in List:
    if el in var: return True
  return False

 
def find(eingabe, search, n):
  if(n == 1): return eingabe.find(search)
  else: return eingabe.find(search, find(eingabe,search,n-1)+1)
 
def unnoetigewsentfernen(pattern,eingabe):
  #print(re.match(pattern,eingabe))
  if(re.match(pattern, eingabe) == None): 
    #print((re.match(patterntest, eingabe) == None) == True)
    return eingabe
  if(re.match(pattern, eingabe) != None):
    if(' ' not in eingabe): return eingabe
    backup = eingabe
    
    i = 1
    index_ws = find(eingabe,' ',i)
    while(True):
      eingabe = backup
      eingabe = eingabe.replace(eingabe[index_ws],'')
      if(re.match(pattern, eingabe)):
        backup = eingabe
        continue 
      else: break
      i=i+1
      index_ws = find(eingabe,' ',i)
        
    eingabe = backup  
    return eingabe

#ermittelt den typ einer expression, literals, variable oder den rueckgabetyp fuer methode
def gettype(data):
  while('  ' in data):data = data.replace('  ',' ')
  if(data.count('(') != data.count(')')): 
    return "Error"
  if(data == "null"): return "null"
  if(re.match(r"[\s]*\([^\s]+\)[\s]*",data)):
    data = data.replace("(","")
    data = data.replace(")","")
  datacpy = data
  data = data.replace(' ','')
  typop1 = "Error"
  if(arrayaccess(data+";", False)[0] == True): 
    typop1 = arraytypdict[data[:data.index('[')]]
  elif((data in variablenliste)):
    typop1 = variablentypdict[data]
  elif(methodaccess(data,True)[0] == True):
    typop1 = methodreturndict[data[:data.index('(')]]
  elif(listelinvar(Arops, data) == True and arops(data, False)[0] == True): 
    typop1 = arops(data, True)[0]
  elif(listelinvar(Bitops, data) == True and bitop(data, False)[0] == True): 
    typop1 = bitop(data, True)[0]
  elif(listelinvar(Logicops, data) and logicops(data, False)[0] == True):
    typop1 = logicops(data, True)[0]
  elif(listelinvar(Compops, data) and compops(data, False)[0] == True):
    typop1 = compops(data, True)[0]
  elif(listelinvar(Assignops, data) and assignops(data, False)[0] == True):
    typop1 = assignops(data, True)[0]
  elif(getLiteraltype(datacpy)[0] != "Error"):
    typop1 = getLiteraltype(datacpy)[0]
  if(typop1 == []): return ""
  return typop1

#split string with list of seperators
def multisplit(seplist, eingabe):
  #print(str(seplist)+" "+str(eingabe))
  if(seplist == [] or seplist == None): return eingabe
  else:
    if(isinstance(eingabe, list)):  
      newlist = eingabe
      while(eingabe != [] and eingabe != None):
        seperable = False
        for val in eingabe:
          if(seplist[0] not in val):continue
          else: 
            seperable = True
            break
          #val = eingabe[0]
        if(seperable == False): break
        if(isinstance(val, str)):
          if(seplist[0] in val):
            sublist = val.split(seplist[0])
            if(val in sublist): sublist.remove(val)
            if(sublist == None): sublist = []
            if('' in sublist): sublist.remove('')
            if(sublist == None): sublist = []
            newlist += sublist
            newlist.remove(val)
            
        if(val in eingabe): eingabe = eingabe.remove(val)
      return multisplit(seplist[1:], newlist)
    else: 
      eingabe = eingabe.split(seplist[0])
      return multisplit(seplist[1:],eingabe)
    

'''
###########################################################################
LEXIK
###########################################################################
'''
   
def javaletter(letter):
  if(letter.isalnum()): return True
  if(letter=='$' or letter=='_'): return True
  return False

def identifier(eingabe):
  pattern_digit = r"[0-9]+.*"
  notvalid = ["true", "false", "null"]
  if(re.match(pattern_digit, eingabe)):
    return ["identifiers_digit",eingabe]
  if((eingabe in keywords)): 
    return ["identifiers_keyword",eingabe]
  if((eingabe in notvalid)): 
    return ["identifiers_null_boolean",eingabe]
  if(re.findall(u"[^\u0000-\uFFFF]+", eingabe)!=[]):return ["identifiers_nonletter",eingabe]
  for character in eingabe:
    if(javaletter(character) != True): return ["identifiers_nonletter",eingabe]
  '''
  '''
  return [True,eingabe]


def keyword(eingabe):
  if(eingabe == ""): return ["keyword_non",eingabe]
  if(eingabe in keywords): return [True,eingabe]
  else: return ["keyword_non",eingabe]
  
def literal(eingabe):
  if(eingabe == ""): return ["literal_non",eingabe]
  if(charLiteral(eingabe)[0] == True): return [True,eingabe]
  if(stringLiteral(eingabe)[0] == True): return [True,eingabe]
  if(integerLiteral(eingabe)[0] == True): return [True,eingabe]
  if(floatLiteral(eingabe)[0] == True): return [True,eingabe]
  if(booleanLiteral(eingabe)[0] == True): return [True,eingabe]
  if(nullLiteral(eingabe)[0] == True): return [True,eingabe]
  return ["literal_non",eingabe]
  
def charLiteral(eingabe):
  if(eingabe.startswith('\'') != True or eingabe.endswith('\'') != True):return ["char_literal_non",eingabe]
  eingabe = eingabe.replace('\'','')
  if(len(eingabe) != 1): return ["char_literal_non",eingabe]
  else:
    escapes = ['\n','\r','\f','\\','\'','\"','\t','\b']
    if(eingabe.isalpha() == False and javaletter(eingabe) == False and eingabe not in escapes):return ["char_literal_non",eingabe]
    return [True,eingabe]

def booleanLiteral(eingabe):
  if(eingabe == "true" or eingabe == "false"):return [True,eingabe]
  return ["boolean_literals_non",eingabe]

def nullLiteral(eingabe):
  if(eingabe == ""): return ["null_literal_non",eingabe]
  if(eingabe == "null"): return [True,eingabe]
  else: return ["null_literal_non",eingabe]

def stringLiteral(eingabe):
  if(eingabe.startswith('"') != True or eingabe.endswith('"') != True):return ["string_literal_non",eingabe]
  for char in eingabe:
    if(charLiteral(char)[0] == False): return ["string_literals_non",eingabe]
  return [True,eingabe]

def integerLiteral(eingabe):
  if(eingabe == ""): return ["integer_literals_non_decimal",eingabe]
  eingabe = str(eingabe)
  if(eingabe.startswith("0b")): 
    if(len(eingabe) <= 2): return ["integer_literals_binary_not_empty",eingabe]
    for char in eingabe[2:]: 
      if not(char.isdigit() and int(char) < 2): return ["integer_literals_non_binary",str(char)]
    return [True,eingabe]
  elif(eingabe.startswith("0x")):
    if(len(eingabe) <= 2): return ["integer_literals_hex_not_empty",eingabe]
    for char in eingabe[2:]: 
      if not(char.isdigit() or char in ['A','B','C','D','E','F']): return ["integer_literals_non_hex",str(char)]
    return [True,eingabe]
  elif(eingabe.startswith("0")):
    for char in eingabe[1:]: 
      if not(char.isdigit() and int(char) < 8): return ["integer_literals_non_octal",str(char)]
    return [True,eingabe]
  else:
    for char in eingabe: 
      if not char.isdigit(): return ["integer_literals_non_decimal",str(char)]
  return [True,eingabe]
  
def floatLiteral(eingabe):
  if('.' not in eingabe): return ["float_literals_no_point",eingabe]
  ind = eingabe.index('.')
  post = ""
  cpy = eingabe
  if(len(re.findall(r"E[\d]+", eingabe[eingabe.index('.')+1:])) == 1):
    exp = re.findall(r"E[\d]+", eingabe[eingabe.index('.')+1:])[0]   
    eingabe = eingabe.replace(exp,"")
  if(eingabe[-1] in ['F','D']): 
    post = eingabe[ind+1:-1]
  elif(eingabe[-1].isdigit()):
    post = eingabe[ind+1:]
  else: return ["float_literals_wrong_structure",cpy]  
  pre = eingabe[:ind]
  if(not(pre == "" or pre.startswith('0x') or pre.startswith('0b') or pre.startswith('0') or integerLiteral(pre)[0] == True)):
    return ["float_literals_wrong_prefix",cpy]
  if(not(integerLiteral(post)[0] == True)):return [integerLiteral(post)[0],post]
  return [True,cpy]

def getLiteraltype(eingabe):
  while(eingabe.startswith(' ')):eingabe = eingabe[1:]
  while(eingabe.endswith(' ')):eingabe = eingabe[:-1]
  if(booleanLiteral(eingabe)[0] == True): return [["boolean"],eingabe]
  elif(nullLiteral(eingabe)[0] == True): return [["null"],""]
  elif(integerLiteral(eingabe)[0] == True): return [integertypes,eingabe]
  elif(floatLiteral(eingabe)[0] == True): return [floattypes,eingabe]
  elif(stringLiteral(eingabe)[0] == True): return [["String"],eingabe]
  elif(eingabe.startswith('\'') == True and eingabe.startswith('\'')== True and charLiteral(eingabe) == True): return [["char"],eingabe]
  else: return ["Error",eingabe]


'''
###########################################################################
SYNTAX
###########################################################################
'''   



def main(eingabe):
  patternmain = r"[\s]*public [\s]*static [\s]*void main[\s]*\([\s]*String\[\][\s]* [^\s]+[\s]*\)[\s]*\{[\s]*.*[\s]*\}[\s]*"
  patternmain2 = r"[\s]*public static void main[\s]*\([\s]*String [^\s]+[\s]*\[\][\s]*\)[\s]*\{[\s]*.*[\s]*\}[\s]*"
  if(re.match(patternmain, eingabe) or re.match(patternmain2, eingabe)):
    if(re.match(patternmain, eingabe)):eingabe = unnoetigewsentfernen(patternmain, eingabe)
    if(re.match(patternmain2, eingabe)):eingabe = unnoetigewsentfernen(patternmain2, eingabe)
    mul = eingabe.split(' ')
    if(identifier(mul[-1][-1])[0]): return [True,""]
    else: return ["main_wrong",""]
  else:
    return ["main_wrong",eingabe]
    
      
def imports(eingabe):
  numb_wildcards = 0
  patternimports = r"[\s]*import [\s]*[^\s]+[\s]*([\s]*\.[^\s]+[\s]*)*[\s]*;[\s]*"
  if("import" not in eingabe): return ["import_no_keyword",eingabe]
  if(re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return ["import_wrong_semicolon",eingabe]
  if(re.match(patternimports, eingabe)):
    eingabe = unnoetigewsentfernen(patternimports, eingabe)
    eingabe = eingabe[eingabe.index("import")+7:eingabe.index(';')]
    data = eingabe.split('.')
    for dat in data:   
      dat = dat.replace(' ','')   
      if("*" in dat):
        numb_wildcards+=1
        if(numb_wildcards > 1): return ["import_error_wildcard",dat]
      elif(identifier(dat)[0] != True): 
        return ["import_identifier",dat]
    return [True,eingabe]
  else: return ["import_wrong_structure",eingabe]
  
def packages(eingabe):
  patternpackage = r"[\s]*package [\s]*[^\s]+[\s]*([\s]*\.[^\s]+[\s]*)*[\s]*;[\s]*"
  if("package" not in eingabe): return ["package_no_keyword",eingabe]
  if(re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return ["package_wrong_semicolon",eingabe]
  if(re.match(patternpackage, eingabe)):
    eingabe = eingabe[eingabe.index("package")+8:eingabe.index(';')]
    data = eingabe.split('.')
    for dat in data:
      dat = dat.replace(' ','')   
      if(identifier(dat)[0] != True): return ["package_indentifier",dat]
    return [True,eingabe]
  else: return ["package_wrong_structure",eingabe]
  
'''
basics
'''


def comments(eingabe):
  if("/*" in eingabe and "*/" in eingabe): return [multiline_comment(eingabe)[0],eingabe]
  elif("//" in eingabe): return [singleline_comment(eingabe)[0],eingabe]
  else: return ["comments_non",eingabe]

def singleline_comment(eingabe):
  singleline = r"[\s]*//.+"
  if(re.match(singleline, eingabe)):return [True,eingabe]
  else: return ["comments_singleline_wrong_structure",eingabe]

def multiline_comment(eingabe):
  multiline = r"[\s]*/*.+"
  if(eingabe.endswith("*/") and re.match(multiline, eingabe)):return [True,eingabe]
  else: return ["comments_multiline_wrong_structure",eingabe]
  

def types(eingabe):
  if(eingabe in prim_types):return [True,eingabe]
  else: return ["types_non",eingabe]
  
def integertype(Type,value):
  if(value == "null"): return [True, value]
  if(re.match(r"[\d]+",value)):    
    value = int(value)
    if(Type == "byte"):
      if(value < -128 or value > 127): return ["integer_literals_byte_oor",value]
      else: return [True,value]
    elif(Type == "short"):
      if(value < -32768 or value > 32767): return ["integer_literals_short_oor",value]  
      else: return [True,value]
    elif(Type == "int"):
      if(value < -2147483648 or value > 2147483647): return ["integer_literals_int_oor",value]  
      else: return [True,value]
    elif(Type == "long"):
      if(value < -9223372036854775808 or value > 9223372036854775807): return ["integer_literals_long_oor",value]
      else: return [True,value]
    elif(Type == "char"):
      if(value < 0 or value > 65535): return ["integer_literals_char_oor",value]
      else: return [True,value]
    else: return ["integer_literal_non",value]
  else: 
    if(Type == "char" and re.match(r"'.'",value)): return [True,value]
    else: return ['integer_literal_non',value]
    

def variable_definition_initialization(eingabe,dsv_speichern):
  patterndefinit = r"[\s]*[^\s]+ [\s]*[^\s]+[\s]*=[\s]*[^\s]+[\s]*;[\s]*"
  patterndefinitnew = r"[\s]*[^\s]+ [\s]*[^\s]+[\s]*=[\s]*new [\s]*[^\s]+\([\s]*[^\s]?[\s]*([\s]*,[\s]*[^\s]+)*\)[\s]*;[\s]*"
  #if(re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return ["variable_definition_initialization_wrong_structure",eingabe]
  if("=" not in eingabe): return ["variable_definition_initialization_wrong_structure",eingabe]
  if(";" not in eingabe): return ["variable_definition_initialization_wrong_semicolon",eingabe]
  if(re.match(patterndefinit, eingabe) == None and re.match(patterndefinitnew, eingabe) == None):  
    return ["variable_definition_initialization_wrong_structure",eingabe]
  
  firstpart = eingabe[:eingabe.index('=')]
  if(variable_definition(firstpart+";",False)[0] != True): 
    if("variable_definition" in variable_definition(firstpart+";",False)[0]): 
      ret = variable_definition(firstpart+";",False)[0]
      if(ret != True): ret = ret.replace("variable_definition","variable_definition_initialization")
      return [ret,firstpart]
    else: return [variable_definition(firstpart+";",False)[0],firstpart]
  vd = eingabe.split(' ',1)
  vd[1] = vd[1][:vd[1].index(';')]
  if(vd[0] not in prim_types and vd[0] not in classlist): return ["variable_definition_initialization_non_type",vd[0]]
    
  vd[1] = vd[1].replace(" ","").split('=',1)
  if(identifier(vd[1][0])[0] != True):return ["variable_definition_initialization_non_identifier",vd[1][0]]
  if(vd[1] in variablenliste): return ["variable_definition_initialization_name_double",vd[1]]
   
  if(inel(vd[0],integertypes)):
    if(vd[1][1] != "null" and integerLiteral(vd[1][1])[0] != True and charLiteral(vd[1][1])[0] != True): return ["variable_definition_initialization_typemismatch_integer",vd[1][1]]
    if(integertype(vd[0], vd[1][1])[0] != True): 
      ausgabe = integertype(vd[0], vd[1][1]) 
      ausgabe[1] = vd[1][1]
      return ausgabe
  elif(inel(vd[0],floattypes)):
    if(vd[1][1] != "null" and floatLiteral(vd[1][1])[0]  != True and integerLiteral(vd[1][1])[0]  != True): return ["variable_definition_initialization_typemismatch_float",vd[1][1]]
  elif(vd[0] == "boolean"):
    if(vd[1][1] != "null" and booleanLiteral(vd[1][1])[0] != True and logicops(vd[1][1], False)[0]!= True and compops(vd[1][1], False)[0] != True): return ["variable_definition_initialization_typemismatch_boolean",vd[1][1]]
  elif(vd[0] == "char"):
    if(vd[1][1] != "null" and charLiteral(vd[1][1])[0]  != True): return ["variable_definition_initialization_typemismatch_char",vd[1][1]]
  elif(vd[0] == "String"):
    if(vd[1][1] != "null" and stringLiteral(vd[1][1])[0]  != True): return ["variable_definition_initialization_typemismatch_string",vd[1][1]]
  elif(vd[0] in classlist):
    if(vd[1][1] != "null"):
      newdef = eingabe[eingabe.index('=')+1:]
      patternnew = r"[\s]*new [\s]*[^\s]+([\s]*[^\s]?[\s]*[,^\s]*[\s]*);[\s]*"
      if("new" not in newdef): return ["variable_definition_initialization_typeclass_no_new",newdef]
      else: 
        if(re.match(patternnew, newdef)):
          classname = newdef[newdef.index("new")+4:newdef.index('(')]
          #paramlist = newdef[newdef.index('(')+1:-2]
          if(classname != vd[0]): return ["variable_definition_initialization_typemismatch_class",vd[0]]
          if(classname in classlist):
            params = newdef[newdef.index('(')+1:newdef.index(')')].replace(' ','').split(',')
            if('' in params):params.remove('')
            if(params==None): params = []
            if(classname in methodlist):
              konstruktorparams = methodparamtypelist[classname]
              if(konstruktorparams==None): konstruktorparams = []
              if(len(params) != len(konstruktorparams)): return ["variable_definition_initialization_contructor_parameter_mismatch_len",str(params)+" != "+str(konstruktorparams)]
              for i in params:
                if(not(inel(konstruktorparams.split(' '), gettype(params[i])))): return ["variable_definition_initialization_contructor_parameter_mismatch",konstruktorparams.split(' ')[0]+" "+params[i]]
            else: 
              if(params != []): return ["variable_definition_initialization_contructor_parameter_mismatch",eingabe]
          if(dsv_speichern == True):
            objecttoclassdict[vd[1][0]] = classname
            objectlist.append(vd[1][0])
          return [True,""]
        else: return ["variable_definition_initialization_wrong_structure",eingabe]
    if(dsv_speichern == True): 
      variablenliste.append(vd[1][0])
      variablentypdict[vd[1][0]] = vd[0]
  return [True,eingabe]
    
def variable_definition(eingabe,dsv_speichern):
  if(re.match("[\s]*[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[\s]*[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return ["variable_definition_wrong_semicolon",""]
  patterndefinit = r"[\s]*[^\s]+[\s]+[^\s]+[\s]*;[\s]*"
  if(re.match(patterndefinit, eingabe)): 
    eingabe = eingabe.replace(" ;",";")
    vd = eingabe.split(' ')
    vd[1] = vd[1][:-1]
    if(vd[0] not in prim_types and vd[0] not in classlist):
      #print(vd[0]+" not in typelist"+str(classlist))
      return ["variable_definition_non_type",vd[0]]
    if(identifier(vd[1])[0] != True):return ["variable_definition_non_identifier",vd[1]]
    if(vd[1] in variablenliste): return ["variable_definition_name_double",vd[1]]
      
    if(vd[0] in classlist):
      objecttoclassdict[vd[1]] = vd[0]
      objectlist.append(vd[1])
    #automatische initialisierung von variablen in java
    if(vd[0] in integertypes or vd[0] in floattypes):variablenval[vd[1]] = 0
    if(vd[0] == "String"):variablenval[vd[1]] = "\"\""
    else: variablenval[vd[1]] = "null"
    if(dsv_speichern == True):
      variablenliste.append(vd[1])
      variablentypdict[vd[1]] = vd[0]
    return [True,eingabe]
  else: return ["variable_definition_wrong_structure",eingabe]
  
def variable_access(eingabe):
  #patternvacc = r"[\s]*[^\s]+[\s]*;[\s]*"
  pattervprint = r"System.out.println\([\s]*[^\s]+[\s]*\)[\s]*" 
  patternvaracc = r"[\s]*[^\s]+[\s]*"
  if(re.match(pattervprint, eingabe) or re.match(patternvaracc, eingabe)): #re.match(pattermimport, eingabe)
    eingabe = eingabe.replace("System.out.println(","")
    eingabe = eingabe.replace(");","")
    eingabe = eingabe.replace(' ','')
    if(identifier(eingabe)[0] != True):
      return ["variable_access_wrong_structure",eingabe]
    if(eingabe in variablenliste): 
      return [True,eingabe]
    else: 
      return ["variable_access_unknown",eingabe]
  else: return ["variable_access_wrong_structure",eingabe]
  
def variable_reassignment(eingabe):  
  if(re.match(r"[\s]*[^\s]*[\s]*=[\s]*[^\s]*[^;]+;[\s]*", eingabe)):
    eingabe = eingabe.replace(';','')
    return [assignops(eingabe,False)[0],eingabe]
  else: return ["variable_reassignment_wrong_structure",eingabe] 

def expression(eingabe):
  if(variable_access(eingabe)[0] == True): return [True,eingabe]
  if(variable_reassignment(eingabe)[0] == True): return [True,eingabe]
  if(arrayaccess(eingabe, False)[0] == True): return [True,eingabe]
  if(multidim_arrayaccess(eingabe, False) == True): return [True,eingabe]
  if(methodaccess(eingabe,True)[0] == True): return [True,eingabe]
  if(membermethodaccess(eingabe,True)[0] == True): return [True,eingabe]
  
  if(arops(eingabe,False)[0] == True):return [True,eingabe]
  if(bitop(eingabe,False)[0] == True):return [True,eingabe]
  if(logicops(eingabe,False)[0] == True):return [True,eingabe]
  return ["expression_non",eingabe]

  
def statement(eingabe):
  if(re.match(r"[\s]*;[\s]*", eingabe)): return [True,eingabe]
  while(eingabe.endswith(' ')): eingabe = eingabe[:-1]
  while(eingabe.startswith(' ')): eingabe = eingabe[1:]
  
  if(re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return ["statement_wrong_semicolon",eingabe]
  if(re.match(r"[\s]*;[\s]*", eingabe) == True): return [True,eingabe] #"empty" statement

  #expression statements
  if(assignops(eingabe,False)[0] == True):return [True,eingabe]
  if(preincdec(eingabe,False)[0] == True): return [True,eingabe]
  if(postincdec(eingabe,False)[0] == True): return [True,eingabe]
  if(methodaccess(eingabe,False)[0] == True): return [True,eingabe]
   
  #declaration statements  
  if(variable_definition(eingabe,True)[0] == True): return [True,eingabe]
  if(variable_definition_initialization(eingabe,True)[0] == True): return [True,eingabe]
  
  if(arraydefinition(eingabe)[0] == True): return [True,eingabe]
  if(array_declaration(eingabe)[0] == True): return [True,eingabe]
  if(arraydefinitialisation(eingabe)[0] == True): return [True,eingabe]
  if(arrayreassignment(eingabe)[0] == True): return [True,eingabe]
  if(multidim_array_definition(eingabe)[0] == True): return [True,eingabe]
  if(multidim_array_declaration(eingabe)[0] == True): return [True,eingabe]
  if(multidim_array_reassignment(eingabe)[0] == True): return [True,eingabe]
    
  #controll flow statements
  if(if_statements(eingabe)[0] == True): return [True,eingabe]
  if(while_statements(eingabe)[0] == True): return [True,eingabe]
  if(do_while_statement(eingabe)[0] == True): return [True,eingabe]
  if(switch_statement(eingabe)[0] == True): return [True,eingabe]
  if(for_statement(eingabe)[0] == True): return [True,eingabe]
  if(extended_for_statement(eingabe)[0] == True): return [True,eingabe]

  if(re.match("System.out.println(.+);", eingabe) and eingabe.endswith(");")):
    eingabe = eingabe.replace("System.out.println(","")
    eingabe = eingabe.replace(");","")
    if(methodaccess(eingabe,False)[0] == True): return [True,eingabe]
    if(variable_access(eingabe)[0] == True): return [True,eingabe]
    if(arrayaccess(eingabe,False)[0] == True): return [True,eingabe]
    if(literal(eingabe)[0] == True): return [True,eingabe] 
  return ["statement_non",eingabe]
#print(identifier("9"))
#print(import_("import a.b.9;"))

def codeblock(eingabe):
  global variablenliste
  #variablenlistcopy = variablenliste.copy()
  variablenlistecopy = []
  for e in variablenliste:
    variablenlistecopy.append(e)
  #if(re.match(r"(\s)*", eingabe)):return [True,eingabe]
  while(eingabe.endswith(' ')): eingabe = eingabe[:-1]
  while(eingabe.startswith(' ')): eingabe = eingabe[1:]
  if(eingabe.startswith('{') and eingabe.endswith('}')):
    Statement = ""
    while(eingabe.endswith(' ')): eingabe = eingabe[:-1]
    while(eingabe.startswith(' ')): eingabe = eingabe[1:]
    for char in eingabe[1:-1]:
      Statement+=char
      #print(Statement+" "+str(statement(Statement)[0]))
      if(statement(Statement)[0] == True):
        Statement = ""
        continue
      if(Statement.startswith('{') and Statement.endswith('}')):
        if(codeblock(Statement[1:-1])[0] == True):
          Statement = ""
          continue
        else:
          return [codeblock(Statement)[0],Statement]
      #returns wie assignments behandeln
      if(re.match(r"[\s]*return[\s]*[^\s]+[\s]*;[\s]*", Statement)):
        Statement = ""
        continue
      
    #print("."+Statement+".")  
    #print(re.match(r"[\s]+", Statement) == None)  
    #print(Statement != "")
    while(Statement.endswith(' ')): Statement = Statement[:-1]
    while(Statement.startswith(' ')): Statement = Statement[1:]
    if(Statement != ""): 
      return ["codeblock_no_statement",Statement]
    else:
      variablenliste = variablenlistecopy #scope of variables
      return [True,eingabe]
  else: 
    return ["codeblock_no_brackets",eingabe]


'''
operators
'''


def memberaccess(eingabe):
  patternmember = r"[^\s]+(\.[^\s]+)*[\s]*(;)*[\s]*"
  if(re.match(patternmember, eingabe)):
    data = eingabe[:-1].split('.',1)
    if(data[0] in objectlist):
      Class = objecttoclassdict[data[0]]
      if(data[1] in classvariablendict[Class]): return [True,eingabe]
      else: return ["member_access_non_member",data[1]]
    elif("(" in data[0] and data[0][data[0].index('('):] in methodlist):
      if(methodaccess(data[0],True)[0] != True): 
        return ["member_access_non_member",data[0]]
    else: return ["member_access_non_member",data[0]]
  else: return ["memberaccess_wrong_structure",eingabe]

#if getType is true; logicops will return the type of a valid operation  

def preincdec(eingabe, getType):
  patterpreincdecadd = r"[\s]*\++[^\s]+[\s]*"
  patterpreincdecsub = r"[\s]*\--[^\s]+[\s]*"
  if("++" not in eingabe and "--" not in eingabe): return ["preincdec_no_operator",eingabe]
  if(re.match(patterpreincdecadd, eingabe) or re.match(patterpreincdecsub, eingabe)):
    eingabe = eingabe[2:-1]
    typop = gettype(eingabe)
    if inel(typop,integertypes) != True:
      return ["preincdec_wrong_type",typop]
    else: 
      if(getType == True): return [integertypes,eingabe]
      else: return [True,eingabe]
  return ["preincdec_wrong_structure",eingabe]

def postincdec(eingabe, getType):
  patterpostincdecadd = r"[\s]*[^\s]+\++[\s]*"
  patterpostincdecsub = r"[\s]*[^\s]+\--[\s]*"
  if("++" not in eingabe and "--" not in eingabe): return ["postincdec_no_operator",eingabe]
  if(re.match(patterpostincdecadd, eingabe) or re.match(patterpostincdecsub, eingabe)):
    eingabe = eingabe[:-3]
    typop = gettype(eingabe)
    if inel(typop,integertypes) != True: return ["postincdec_wrong_type",typop]
    else: 
      if(getType == True): return [integertypes,eingabe]
      else: return [True,eingabe]
  return ["postincdec_wrong_structure",eingabe]

def logicops(eingabe, getType):
  eingabe = eingabe.replace(" ","")

  for op in Logicops:
    if(op in eingabe):
      data = eingabe.split(op,1)
      # or re.match(r"[\s]*[^\s]+[\s]+[^\s]+[\s]*", data[0]) or re.match(r"[\s]*[^\s]+[\s]+[^\s]+[\s]*", data[1]
      if(len(data)!=2): 
        return ["logic_operators_wrong_numops",str(data)]
      else:
        if(len(data)==2 and op == "&&" or op =="||" or op=='^'):       
          #print(data[0]+" "+data[1])
          #ermittle typen der variablen
          typop1 = gettype(data[0])    
          typop2 = gettype(data[1])
          if(typop1 == "Error"): return ["logic_operators_wrong_structure",data[0]]           
          if(typop2 == "Error"): return ["logic_operators_wrong_structure",data[1]]           
          #print(data[0]+": "+str(typop1))
          #print(data[1]+": "+str(typop2))  
  
          if("boolean" in typop1):
            if("boolean" in typop2):
              if(getType == True): return ["boolean",eingabe] 
              elif(getType == False): return [True,eingabe]
              else: 
                print("wrong parametervalue: "+getType)
                exit(-1)
            else: return ["logic_operators_wrong_type",typop1]
          else: return ["logic_operators_wrong_type",typop2]
          
        elif(op == "!" and len(data) == 2):
          #ermittle typ der variable
          typop1 = gettype(data[1])
          if(typop1 == "Error"): return ["logic_operators_wrong_structure",data[1]]  
          if(getType == True):
            if("boolean" in typop1):return ["boolean",eingabe] 
            else: return ["logic_operators_wrong_type",typop1]
          elif(getType == False):
            if("boolean" in typop1):return [True,eingabe] 
            else: return ["logic_operators_wrong_type",typop1]
          else: 
            print("wrong parametervalue: "+getType)
            exit(-1)  
        else: return ["logic_operators_wrong_numops",str(data)]
  return ["logic_operators_no_operator",op]

#if getType is true; compops will return the type of a valid operation  
def compops(eingabe, getType):
    
  for op in Compops:
    if(op in eingabe):
      #eingabe = eingabe.replace(" ","")wafawf
      data = eingabe.split(op,1)
      if(len(data)!=2): return ["comparison_operators_wrong_numops",str(data)]
      else:
        #print(data[0]+" "+data[1])
        #ermittle typen der variablen
        typop1 = gettype(data[0])
        typop2 = gettype(data[1])
        if(typop1 == "Error"): return ["comparison_operators_wrong_structure",typop1]
        if(typop2 == "Error"): return ["comparison_operators_wrong_structure",typop2]
        
        if(getType == True):
          if((inel(typop1,integertypes) or inel(typop1,floattypes)) and (inel(typop2,integertypes) or inel(typop2,floattypes))):return ["boolean",eingabe]
          if(typop1 != "" and typop2 != "" and (typop1 == typop2 or typop1 in typop2 or typop2 in typop1) and (op == "==" or op == "!=")): return ["boolean",eingabe]    
          else: return ["comparison_operators_wrong_type",eingabe]
        elif(getType == False):
          if((inel(typop1,integertypes) or inel(typop1,floattypes)) and (inel(typop2,integertypes) or inel(typop2,floattypes))):return [True,eingabe]
          if(typop1 != "" and typop2 != "" and inel(typop1,typop2) and (op == "==" or op == "!=")): return [True,eingabe]  
          else: 
            return ["comparison_operators_wrong_type",eingabe]
        else: 
          print("wrong parametervalue: "+getType)
          exit(-1)
  return ["comparison_operators_no_operator",op]

#if getType is true; arops will return the type of a valid operation
def arops(eingabe, getType):
  numintop = "%"
  numstringnumstringop = "+"
    
  for op in Arops:
    if(op in eingabe):
      eingabe = eingabe.replace(op+' ',op).replace(' '+op,op)
      
      
      data = eingabe.split(op,1)
      if(len(data)!=2 ): 
        return ["arithmetic_operators_wrong_numops",eingabe]
      else:
        #ermittle typen der variablen
        typop1 = gettype(data[0])
        typop2 = gettype(data[1])
        #print(data[0]+" "+str(typop1))
        #print(data[1]+" "+str(typop2))

        if(typop1 == "Error"): return ["arithmetic_operators_wrong_structure",data[0]]
        if(typop2 == "Error"): 
          return ["arithmetic_operators_wrong_structure",data[1]]
        if(getType == True):
          if(op == numintop and inel(typop2,integertypes)):return [typop1,""]  
          if(op != numintop and (inel(typop1,floattypes)  or inel(typop2,floattypes))  and (inel(typop1,integertypes) or inel(typop2,integertypes))): return [floattypes,""]
          if(op != numintop and (inel(typop1,integertypes) and inel(typop2,integertypes))): return [integertypes,""]
          if(op == numstringnumstringop and (inel(typop1,floattypes)  or inel(typop2,floattypes))  and (inel(typop1,integertypes) or inel(typop2,integertypes))): return [floattypes,""]
          if(op == numstringnumstringop and (inel(typop1,integertypes) and inel(typop2,integertypes))): return [integertypes,""]
          if(op == numstringnumstringop and inel("String",typop1) and inel("String",typop2)): return ["String",""]
          return ["arithmetic_operators_wrong_type",eingabe]
        elif(getType == False):
          if(op == numintop and inel(typop2,integertypes)):return [True,eingabe]  
          if(op != numintop and (inel(typop1,floattypes)  or inel(typop2,floattypes))  and (inel(typop1,integertypes) or inel(typop2,integertypes))):return [True,eingabe] 
          if(op != numintop and (inel(typop1,integertypes) and inel(typop2,integertypes))): return [True,""]
          if(op == numstringnumstringop and (inel(typop1,floattypes)  or inel(typop2,floattypes))  and (inel(typop1,integertypes) or inel(typop2,integertypes))): return [True,eingabe]
          if(op == numstringnumstringop and inel("String",typop1) and inel("String",typop2)): return [True,eingabe]
          if(op == numstringnumstringop and inel(typop1,integertypes) and inel(typop2,integertypes)): return [True,eingabe]
          return ["arithmetic_operators_wrong_type",eingabe]
        else: 
          print("wrong parametervalue: "+getType)
          exit(-1)
  return ["arithmetic_operators_no_operator",op]
  
#if getType is true; assignops will return the type of a valid operation  
def assignops(eingabe, getType):

  numnumops = ["-=", "*=","/="] #left and right site can be int literal, float literal
  numintops = ["%=", "<<=", ">>=", ">>>=", ] #left site can be int, float, rigth side an intliteral
  intintops = ["&=",  "^=", "|="] #left site can be int, rigth side an intliteral
  
  numstringintops = ["+="]  #left side can be a string, int, right side a int
  allallops = ["="]
  
  Assignops = numstringintops+numnumops+numintops+intintops+allallops
  noOp = True
  for op in Assignops:
    if op in eingabe: 
      noOp = False
      break
  if(noOp == True): return ["assignment_operators_no_operator",eingabe]
  
  patternop = r"[\s]*[^\s]+[\s]*[\s]*.?=[\s]*[^\s]+[\s]*"
  if(re.match(patternop, eingabe)):
    
    #linke Seite muss Variable sein
    data = None
    for op in Assignops:
      if(op in eingabe):
        data = eingabe.split(op,1)#replace(' ','')
        var = data[0].replace(' ','')
        if(var not in variablenliste):
          #print(var+" not in "+str((variablenliste)))
          return ["assignment_operators_badLType",var]
        break
      elif(op == allallops):
        data = eingabe.split(op,1)
        var = data[0]
        #print(data)
        if(var not in variablenliste):
          #print(var in variablenliste)
          return ["assignment_operators_badLType",var]
    
    if(data== None or len(data)!=2): return ["assignment_operators_wrong_numops",str(data)]
    
    typop1 = gettype(data[0])
    typop2 = gettype(data[1])
    if(typop1 == "Error"): return ["assignment_operators_wrong_structure",data[0]]
    if(typop2 == "Error"): return ["assignment_operators_wrong_structure",data[1]]
    #print(data[0]+" "+str(typop1))
    #print(data[1]+" "+str(typop2))
    #if(typop1 == "double"):print(str(typop1)+" "+str(typop2))
    
    
    for op in numnumops:
      if(op in eingabe):
        if(inel(typop1, integertypes) or inel(typop1, floattypes)):
          if(inel(typop2, integertypes) or inel(typop2, floattypes)):
            if(getType==False):return [True,eingabe]
            else: return [typop1,eingabe]
          else: return ["assignment_operators_wrong_type",typop2]
        else: return ["assignment_operators_wrong_type",typop1]
          
    for op in numintops:
      if(op in eingabe): 
        if(inel(typop1, integertypes) or inel(typop1, floattypes)):
          if(inel(typop2, integertypes)):
            if(getType==False):return [True,eingabe]
            else: return [typop1,eingabe]
          else: return ["assignment_operators_wrong_type",typop2]
        else: return ["assignment_operators_wrong_type",typop1]
    
    for op in intintops:
      if(op in eingabe):
          if(inel(typop1, integertypes)):
            if(inel(typop2, integertypes)):
              if(getType==False):return [True,eingabe]
              else: return [typop1,eingabe]
            else: return ["assignment_operators_wrong_type",typop2]
          else: return ["assignment_operators_wrong_type",typop1]
    
    for op in numstringintops:
      if(op in eingabe):
        if(inel(typop1, integertypes) or inel(typop1, floattypes)  or (inel(typop1, ["String"]) and inel(typop2,['String']))):
          if(inel(typop2, typop1) or inel(typop1, typop2)):
            if(getType==False):return [True,eingabe]
            else: return [typop1,eingabe]
          else:
            return ["assignment_operators_wrong_type",typop2]
        else:           
          #print(typop1)
          return ["assignment_operators_wrong_type",typop1]
    
    for op in allallops:
      if op in eingabe:
        if(typop2 == "null"): return [True,eingabe]
        if(inel(typop1, ["float","double"]) and inel(typop2, integertypes)): 
          if(getType==False):return [True,eingabe]
          else: return [typop1,eingabe]
        elif(typop1 == typop2 or inel(typop1, typop2) or inel(typop2, typop1)): 
          if(getType==False):return [True,eingabe]
          else: return [typop1,eingabe]
        else: 
          #print(data[0]+" "+typop1)
          #print(data[1]+" "+typop2)
          return ["assignment_operators_wrong_type",eingabe]
 
    return ["assignment_operators_no_operator",eingabe]
  else: return ["assignment_operators_wrong_structure",eingabe]
  
def bitop(eingabe,getType): 
  patternop = r"[\s]*[^\s][\s]*[^\s]+[\s]*[^\s]+"
  
  bitops = ["|", "&", "~", "<<", ">>", ">>>"]
  noOp = True
  for op in bitops:
    if op in eingabe: 
      noOp = False
      break
  if(noOp == True): return ["bitwise_operators_no_operator",eingabe]
  
  if(re.match(patternop, eingabe)):
    
    for op in bitops:
      if(op in eingabe):
        data = eingabe.split(op,1)
        typop1 = gettype(data[0])
        typop2 = gettype(data[1])
        if(typop1 == "Error"): return ["bitwise_operators_wrong_structure",typop1]
        if(typop2 == "Error"): return ["bitwise_operators_wrong_structure",typop2]
        if(len(data)!=2 ): return ["bitwise_operators_wrong_numops",str(data)]
        
        if(inel(typop1, integertypes) and inel(typop2, integertypes)): 
          if(getType == True): return [typop1,""]
          elif(getType == False):return [True,eingabe]
          else: 
            print("wrong parametervalue: "+getType)
            exit(-1)
        else: 
          return ["bitwise_operators_wrong_type",typop1]
    return ["bitwise_operators_no_operator",op]
    
  else: return ["bitwise_operators_wrong_structure",eingabe]
    
  
'''
controll structure
'''

def matchbreak(eingabe):
  if(re.match("[\s]*break[\s]*;[\s]*", eingabe)):return [True,eingabe]
  return [str(False),eingabe]

def matchcontinue(eingabe):
  if(re.match("[\s]*continue[\s]*;[\s]*", eingabe)):return [True,eingabe]
  return [str(False),eingabe]

def booleanexpression(eingabe):
  if(inel(gettype(eingabe),"boolean")): return [True,eingabe]
  else: 
    return ["boolean_expression_non",eingabe]

def if_statements(eingabe):
  #variablenlistcopy = variablenliste
  if("if" not in eingabe): return ["if_no_keyword",eingabe]
  if(eingabe.count(")") != eingabe.count("(")  or eingabe.count(")")+eingabe.count("(")<2): return ["if_brackets_not_matching",eingabe]
  patternif1 = r"[\s]*if[\s]*\(.+\)[\s]*[^\s]*;[\s]*"
  patternif2 = r"[\s]*if[\s]*\(.+\)[\s]*\{.*\}[\s]*"
  patternif3 = r"[\s]*if[\s]*\(.+\)[\s]*;[\s]*"
  
  if(re.match(patternif1, eingabe) or re.match(patternif2, eingabe) or re.match(patternif3, eingabe)):
    ind_openingbracket = eingabe.index("(") 
    ind_closingbracket = eingabe[ind_openingbracket:].index(")") #rindex findet die letzte instanz des substrings - notwending damit boolean expressions 
    booleanxpre = eingabe[ind_openingbracket+1:ind_closingbracket+ind_openingbracket]
    if(booleanexpression(booleanxpre)[0] != True):
      return ["if_no_boolean_expression",booleanxpre]
    if(re.match(patternif3, eingabe)): 
      return [True,eingabe]
    elif(re.match(patternif1, eingabe)): 
      Statement = eingabe[ind_closingbracket+ind_openingbracket+1:]
      if(statement(Statement)[0] != True): return ["if_non_statement",Statement]
    elif(re.match(patternif2, eingabe)):
      Codeblock = eingabe[ind_closingbracket+ind_openingbracket+1:]
      if(codeblock(Codeblock)[0] != True): return ["if_non_codeblock",Codeblock]
    else: return ["if_wrong_structure",""]
    return [True,eingabe]
  else: 
    if("if" in eingabe):return ["if_wrong_structure",eingabe]
 
def while_statements(eingabe):
  if("while" not in eingabe): return ["while_no_keyword",eingabe]
  if(eingabe.count(")") != eingabe.count("(")  or eingabe.count(")")+eingabe.count("(")<2): return ["while_brackets_not_matching",eingabe]
  patternwhile1 = r"[\s]*while[\s]*\(.+\)[\s]*[^\s]*;[\s]*"
  patternwhile2 = r"[\s]*while[\s]*\(.+\)[\s]*\{.*\}[\s]*"
  patternwhile3 = r"[\s]*while[\s]*\(.+\)[\s]*;[\s]*"
    
  if(re.match(patternwhile1, eingabe) or re.match(patternwhile2, eingabe) or re.match(patternwhile3, eingabe)):
    ind_openingbracket = eingabe.index("(") 
    ind_closingbracket = eingabe[ind_openingbracket:].index(")") 
    booleanxpre = eingabe[ind_openingbracket+1:ind_closingbracket+ind_openingbracket]
    
    if(booleanexpression(booleanxpre)[0] != True): return ["while_no_boolean_expression",booleanxpre]
    if(re.match(patternwhile3, eingabe)): return [True,eingabe]
    elif(re.match(patternwhile1, eingabe)): 
      #print(eingabe)
      Statement = eingabe[ind_closingbracket+1+ind_openingbracket:]
      
      if("break" in Statement):    
        if(len(re.findall(r"[\s]*break[\s]*;[\s]*", Statement)) != 1): return ["while_break",Statement]
        else:      
          Statement = Statement.replace("break", "")
      if("continue" in Statement):
        if(len(re.findall(r"[\s]*continue[\s]*;[\s]*", Statement)) != 1): return ["while_continue",Statement]
        else:      
          Statement = Statement.replace("continue", "")
      
      if(statement(Statement)[0] != True): return ["while_non_statement",Statement]
    elif(re.match(patternwhile2, eingabe)):
      Codeblock = eingabe[ind_closingbracket+1+ind_openingbracket:]
      if(re.match(patternwhile2, eingabe)):
        
        if("break" in Codeblock):    
          if(len(re.findall(r"[\s]*break[\s]*;[\s]*", Codeblock)) != 1): return ["while_break",Codeblock]
          else:      
            Codeblock = Codeblock.replace("break", "")
        if("continue" in Codeblock):
          if(len(re.findall(r"[\s]*continue[\s]*;[\s]*", Codeblock)) != 1): return ["while_continue",Codeblock]
          else:      
            Codeblock = Codeblock.replace("continue", "")
     
      if(codeblock(Codeblock)[0] != True): return ["while_non_codeblock",Codeblock]
    else: return ["while_wrong_structure",""]
    return [True,eingabe]
  else: 
    if("while" in eingabe):return ["while_wrong_structure",eingabe]
 
  
def do_while_statement(eingabe):
  if(eingabe.endswith(r"[\s]*;[\s]*") != True and eingabe.endswith(r";[\s]*") != True and eingabe.endswith(r";") != True): return ["do_while_wrong_semicolon",eingabe]
  if("do" not in eingabe or "while" not in eingabe): return ["do_while_no_keyword",eingabe]
  
  if(eingabe.count(")") != eingabe.count("(")  or eingabe.count(")")+eingabe.count("(")<2): return ["do_while_round_brackets_not_matching",eingabe]
  if(eingabe.count("}") != eingabe.count("{")  or eingabe.count("}")+eingabe.count("{")<2): return ["do_while_curly_brackets_not_matching",eingabe]
  patterndowhile = r"[\s]*do[\s]*\{.*\}[\s]*while[\s]*\([^\s]+\)[\s]*;[\s]*"
  if(re.match(patterndowhile, eingabe)):
    ind_openingbracket = eingabe.index("(") 
    ind_closingbracket = eingabe[ind_openingbracket:].index(")")
    Booleanxpre = eingabe[ind_openingbracket+1:ind_closingbracket+ind_openingbracket]
    ind_openingbracket = eingabe.index("{") 
    ind_closingbracket = eingabe.index("}") 
    Codeblock = eingabe[ind_openingbracket:ind_closingbracket+1]
    
    if("break" in Codeblock):    
        if(len(re.findall(r"[\s]*break[\s]*;[\s]*", Codeblock)) != 1): return ["do_while_break",Codeblock]
        else:      
          Codeblock = Codeblock.replace("break", "")
    if("continue" in Codeblock):
      if(len(re.findall(r"[\s]*continue[\s]*;[\s]*", Codeblock)) != 1): return ["do_while_continue",Codeblock]
      else:      
        Codeblock = Codeblock.replace("continue", "")
             
    #print(Booleanxpre+" "+Statement)
    if(booleanexpression(Booleanxpre)[0] != True): return ["do_while_no_boolean_expression",Booleanxpre]
    if(codeblock(Codeblock)[0] != True): return ["do_while_non_codeblock",Codeblock]
    return [True,eingabe]
  else: return ["do_while_wrong_structure",eingabe]

def switch_statement(eingabe):
  if("switch" not in eingabe): return ["switch_no_keyword",eingabe]
  
  if(eingabe.count(")") != eingabe.count("(")  or eingabe.count(")")+eingabe.count("(")<2): return ["switch_round_brackets_not_matching",eingabe]
  if(eingabe.count("}") != eingabe.count("{")): return ["switch_curly_brackets_not_matching",eingabe]
  patternswitch1 = r"[\s]*switch[\s]*(\([^\s]+\))[\s]*{([\s]*case[\s]+[^\s]+[\s]*:[\s]*.+)*([\s]*default[\s]*:.+)*}"
  patternswitch2 = r"[\s]*switch[\s]*(\([^\s]+\))[^\s]+;[\s]*"
  
  ind_openingbracket = eingabe.index("(") 
  ind_closingbracket = eingabe[ind_openingbracket:].index(")")
  Variable = eingabe[ind_openingbracket+1:ind_closingbracket+ind_openingbracket]
  if(variable_access(Variable)[0] != True or inel(gettype(Variable),["char", "byte", "short", "int", "Byte", "String"]) != True): 
    return ["switch_non_variable",eingabe]
    
  if(re.match(patternswitch1, eingabe)):
    ind_openingbracket = eingabe.index("{") 
    ind_closingbracket = eingabe.index("}") 
    Codeblock = eingabe[ind_openingbracket+1:ind_closingbracket+1]
    print(Codeblock)
    if(Codeblock==""):return [True,eingabe]

    patterncaseblock = r"[\s]*case[\s]+[^\s]+[\s]*:[\s]*\{[\s]*[^\s]*[\s]*\}[\s]*"
    patterncasestatement = r"[\s]*case[\s]+[^\s]+[\s]*:[\s]*[^\s]+[\s]*;[\s]*"
    patterndefaultblock = r"[\s]*default[\s]*:[\s]*\{[\s]*[^\s]*[\s]*\}[\s]*"
    patterndefaultstatement = r"[\s]*default[\s]*:[\s]*[^\s]+[\s]*;[\s]*"

    Statement = ""
    for char in Codeblock:
      Statement += char
      if(re.match(patterncaseblock, Statement) or re.match(patterncasestatement, Statement) and Statement.count('{') ==  Statement.count('}')):
        Statement = Statement[Statement.index("case")+5:]
             
        Value = Statement[:Statement.index(':')]
        if(variablentypdict[Variable] in ["char", "byte", "short", "int"]):
          if(integerLiteral(Value)[0] == True):       
            if("break" in Statement):
              print(Statement)
              print(Statement.count("break")) 
              print(len(re.findall(r"[\s]*break[\s]*;[\s]*", Statement)))
              if(len(re.findall(r"[\s]*break[\s]*;[\s]*", Statement)) != 1): return ["switch_break",Statement]
              else:      
                #Statement = Statement.replace("break", "")
                Statement = Statement.replace("break;", "")
            if(statement(Statement[Statement.index(':')+1:])[0] != True): 
              return ["switch_wrong_case",Statement[Statement.index(':')+1:]]
          else: return ["switch_varval_mismatch",Value+" not a Integertype"]
        else: return ["switch_varval_mismatch", Variable+" not in "+str(["char", "byte", "short", "int"])]
        Statement = ""
      elif(re.match(patterndefaultblock, Statement) or re.match(patterndefaultstatement, Statement) and Statement.count('{') ==  Statement.count('}')):
        Statement = Statement[Statement.index("default")+8:]
        
        if("break" in Statement):    
          if(len(re.findall(r"[\s]*break[\s]*;[\s]*", Statement)) != 1): return ["while_break",Statement]
          else:      
            Statement = Statement.replace("break", "")
        
        if(statement(Statement)[0] != True):
            return ["switch_wrong_default",Statement]
        Statement = ""
    if(Statement != ""):return ["switch_wrong_structure",eingabe]
    if(Statement == "" or re.match(r"[^\s]+",Statement) == None): return [True,eingabe]
  elif(re.match(patternswitch2, eingabe)):return [True,eingabe]
  return ["switch_wrong_structure",eingabe]
  
#methods: def, zugriff

def extended_for_statement(eingabe):
  patternexfor1 = r"[\s]*for[\s]*\([\s]*[^\s]+ [\s]*[^\s]+[\s]*:[\s]*[^\s]+\).*;"
  patternexfor2 = r"[\s]*for[\s]*\([\s]*[^\s]+ [\s]*[^\s]+[\s]*:[\s]*[^\s]+\)[\s]*{.*}[\s]*"
  patternexfor3 = r"[\s]*for[\s]*\([\s]*[^\s]+ [\s]*[^\s]+[\s]*:[\s]*[^\s]+\)[\s]*;[\s]*"

  
  if("for" not in eingabe): return ["extended_for_no_keyword",eingabe]
  
  if(re.match(patternexfor1, eingabe) or re.match(patternexfor2, eingabe) or re.match(patternexfor3, eingabe)):
    head = eingabe[eingabe.index('(')+1:eingabe.index(')')]
    data = head.split(':')
    a = variable_definition(data[0]+";",False)[0]
    if(a != True): 
      return ["extended_for_no_variable_definition",data[0]+";"]
    data[1] = data[1].replace(" ","")
    if(data[1] not in arraylist): 
      #print("."+data[1]+".")
      return ["extended_for_nonarray",data[1]]
    else: 
      if(arraytypdict[data[1]] != data[0].split(' ')[0]): return ["extended_for_varar_mismatch",data[1]]
    body = eingabe[eingabe.index(')')+1:]
    
    if("break" in body):    
      if(len(re.findall(r"[\s]*break[\s]*;[\s]*", body)) != 1): return ["extended_for_break",body]
      else:      
        body = body.replace("break", "")
    if("continue" in body):
        if(len(re.findall(r"[\s]*continue[\s]*;[\s]*", body)) != 1): return ["extended_for_continue",body]
        else:      
          body = body.replace("continue", "")
    
    if(re.match(patternexfor3, eingabe)):return [True,eingabe]
    elif(re.match(patternexfor2, eingabe)):
      if(codeblock(body)[0] != True): return ["extended_for_noncode_block",body]
      else: return [True,eingabe]
    elif(re.match(patternexfor1, eingabe)):
      if(statement(body)[0] != True): 
        return ["extended_for_nonstatement",body]
      else: return [True,eingabe]
    return ["extended_for_wrong_structure",eingabe]
  else: return ["extended_for_wrong_structure",eingabe]

def for_statement(eingabe):
  global variablenliste
  #variablenlistecopy = variablenliste.copy()
  variablenlistecopy = []
  for e in variablenliste:
    variablenlistecopy.append(e)
  if("for" not in eingabe):return ["for_no_keyword",eingabe]
  
  #[\s]*
  patternfor1 = r"[\s]*for[\s]*\([\s]*[^\s]*[\s]*[^\s]*[\s]*;[\s]*[^\s]*[\s]*;[\s]*[^\s]*[\s]*\)[^\s]*[\s]*;[\s]*"
  patternfor2 = r"[\s]*for[\s]*\([\s]*[^\s]*[\s]*[^\s]*[\s]*;[\s]*[^\s]*[\s]*;[\s]*[^\s]*[\s]*\)[\s]*{.*}[\s]*"
  patternfor3 = r"[\s]*for[\s]*\([\s]*[^\s]*[\s]*;[\s]*[^\s]*[\s]*;[\s]*[^\s]*[\s]*\)[^\s]*[\s]*;[\s]*"
  patternfor4 = r"[\s]*for[\s]*\([\s]*[^\s]*[\s]*;[\s]*[^\s]*[\s]*;[\s]*[^\s]*[\s]*\)[\s]*{.*}[\s]*"
  
  if(re.match(patternfor1, eingabe) or re.match(patternfor2, eingabe) or re.match(patternfor3, eingabe) or re.match(patternfor4, eingabe)):
    head = eingabe[eingabe.index('(')+1: eingabe.index(')')]
    statements = head.split(';')
    if(variable_definition_initialization(statements[0]+";",False)[0] != True):
      variablenliste = variablenlistecopy
      if(variable_definition(statements[0]+";",False)[0] != True):
        variablenliste = variablenlistecopy
        if(statement(statements[0]+";")[0] != True):
          a = statements[0].replace(' ','')
          if(assignops(eingabe, False)[0] != True and statements[0] != "" and a != ""): 
            return ["for_no_variable_definition",statements[1]]
    if(not(booleanexpression(statements[1])[0] == True)):
      if(statements[1] != "" and re.match(r"[^\s]+",statements[1]) != None):
        return ["for_no_boolean_expression",statements[1]]
    if(not(assignops(statements[2]+";", False)[0] == True and preincdec(statements[2]+";", False)[0] == True and postincdec(statements[2]+";", False)[0] == True or statement(statements[2]+";")[0] == True )):
      a = statements[2].replace(' ','')
      if(statements[2] != "" and a != ""):
        return ["for_no_increment",statements[2]]
    
   
    if(re.match(patternfor2, eingabe) or re.match(patternfor4, eingabe)):
      body = eingabe[eingabe.index('{'):]     
      
      if("break" in body):    
        if(len(re.findall(r"[\s]*break[\s]*;[\s]*", body)) != 1): return ["for_break",body]
        else:      
          body = body.replace("break", "")
      if("continue" in body):
        if(len(re.findall(r"[\s]*continue[\s]*;[\s]*", body)) != 1): return ["for_continue",body]
        else:      
          body = body.replace("continue", "")
       
      if(re.match(r"[\s]*\{[\s]*\}[\s]*",body) == None):
        if(codeblock(body)[0] != True): return ["for_noncode_block",body]
    else: 
      body = eingabe[eingabe.index(')')+1:]
      if(re.match(r"[\s]*;[\s]*",body) == None):
        if(statement(body)[0] != True): return ["for_nonstatement",body]
    if(re.match(r"[\s]*;[\s]*", body)): return [True,eingabe]
    variablenliste = variablenlistecopy
    if(codeblock(body)[0] == True): return [True,eingabe]
    if(statement(body)[0] == True): return [True,eingabe]
    else: return ["for_wrong_structure",eingabe]
  else: return ["for_wrong_structure",eingabe]
  
'''
arrays
'''


def arraydefinition(eingabe):
  if("[]" not in eingabe or (eingabe.count("[") != 1 or eingabe.count("]") != 1)): return ["array_definition_no_brackets",eingabe]
  if(re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return ["array_definition_wrong_semicolon",eingabe]

  patterarrdef1 = r"[\s]*[^\s]+[\s]*[^\s]+[\s]*\[\][\s]*;[\s]*"
  patterarrdef2 = r"[\s]*[^\s]+[\s]*\[\][\s]*[^\s]+[\s]*;[\s]*"

  if(re.match(patterarrdef1, eingabe) or re.match(patterarrdef2, eingabe)):
    vd = eingabe.replace("[]","")
       
    if(variable_definition(vd,False)[0] == True):
      arrayname = vd.split(' ')[1].replace(';','')
      if(arrayname in arraylist): return ["array_definition_name_double",arrayname]

      arraylist.append(arrayname)
      arraytypdict[arrayname] = vd.split(' ')[0]
      
      return [True,eingabe]
    else: 
      
      ret = variable_definition(vd,False)[0]
      if(ret != True): ret = ret.replace("variable", "array")
      return [ret,eingabe]
    
  else: return ["array_definition_wrong_structure",eingabe]

def array_declaration(eingabe):
  if("[]" not in eingabe or (eingabe.count("[") != 2 or eingabe.count("]") != 2)): return ["array_declaration_no_brackets",eingabe]
  if(not("new" in eingabe)): return ["array_declaration_no_new",eingabe]
  if (re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return ["array_declaration_wrong_semicolon",eingabe]

  patterarrdefinit1 = r"[\s]*[^\s]+[\s]*\[\][\s]*[^\s]+[\s]*=[\s]*new [\s]*[^\s]+[\s]*\[[0-9]+\];[\s]*"
  patterarrdefinit2 = r"[\s]*[^\s]+[\s]+[^\s]+[\s]*\[\][\s]*=[\s]*new [\s]*[^\s]+[\s]*\[[0-9]+\];[\s]*"
  
  if(re.match(patterarrdefinit1, eingabe) or re.match(patterarrdefinit2, eingabe)):
    eingabe = eingabe.replace('  ',' ')
    leftside = eingabe[:eingabe.index("=")].replace("[]","")
    rightside = eingabe[eingabe.index("="):]
    if(not(listelinvar(prim_types, rightside) or listelinvar(classlist, rightside))): return ["array_declaration_non_type",rightside]
    if(not(listelinvar(prim_types, leftside) or listelinvar(classlist, leftside))): return ["array_declaration_non_type",leftside]
    else:
      arrayname = leftside.split(' ')[1].replace("[]","")
      arraytype = leftside.split(' ')[0].replace("[]","")
      arraytyperight = rightside[1:rightside.index("[")].replace("new", "").replace(' ', '')
      if(arraytype != arraytyperight): return ["array_declaration_wrong_type",arraytype+" != "+arraytyperight]
      arraylist.append(arrayname)
      arraytypdict[arrayname] = arraytype
      arraydimdict[arrayname] = rightside[rightside.index('[')+1:rightside.index(']')]
      return [True,eingabe]  
  else: return ["array_declaration_wrong_structure",eingabe]

def arraydefinitialisation(eingabe):
  if("[]" not in eingabe or eingabe.count("[") != 1 or eingabe.count("]") != 1 ): return ["array_definition_initialization_no_brackets",eingabe]
  if(not("new" in eingabe or ("{" in eingabe and "}" in eingabe and (eingabe.count("{") == 1 or eingabe.count("}") == 1)) or "null" in eingabe)): return ["array_definition_initialization_no_brackets",eingabe]
  if (re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return ["array_definition_initialization_wrong_semicolon",eingabe]

  eingabe = eingabe.replace(', ',',').replace(' ,',',') #dirtyfix
  patterarrdefinit1 = r"[\s]*[^\s]+ [\s]*[^\s]+[\s]*\[\][\s]*=[\s]*\{[\s]*[^\s]+[\s]*([\s]*\,[\s]*[^\s]+])*\};[\s]*"
  patterarrdefinit2 = r"[\s]*[^\s]+[\s]*\[\][\s]*[^\s]+[\s]*=[\s]*\{[\s]*[^\s]+[\s]*([\s]*\,[\s]*[^\s]+])*\};[\s]*"
  patterarrdefinitNULL1 = r"[\s]*[^\s]+[\s]+[^\s]+[\s]*\[\][\s]*=[\s]*null[\s]*;[\s]*"
  patterarrdefinitNULL2 = r"[\s]*[^\s]+[\s]*\[\][\s]*[\s]+[^\s]+[\s]*=[\s]*null[\s]*;[\s]*"


  if(re.match(patterarrdefinit1, eingabe) or re.match(patterarrdefinit2, eingabe) or re.match(patterarrdefinitNULL1, eingabe) or re.match(patterarrdefinitNULL2, eingabe)):
    eingabe = eingabe.replace('  ',' ')
    leftside = eingabe[:eingabe.index("=")+1].replace("[]","")
    rightside = eingabe[eingabe.index('=')+1:]
    
    if("null" not in rightside):
      values = eingabe[eingabe.index("{")+1:eingabe.index("}")].replace(" ","").split(",")
  
      for value in values:
        name = leftside.split(' ')[1]
        if(name in variablenliste): variablenliste.remove(name)
        if(name in variablenliste): variablenliste.remove(name)
        valid = variable_definition_initialization(leftside+" "+value+";",False)[0]
        #print(name)
        if(valid != True):
          if(name in variablenliste): variablenliste.remove(name)
          if(name in variablenliste): variablenliste.removeall(name)
          ret = variable_definition_initialization(leftside+" "+value+";",False)[0].replace("variable","array")
          return [ret,leftside+" "+value]
        else:
          if(leftside.split(' ')[1] in arraylist): return ["array_definition_initialization_name_double",leftside]
          if(name in variablenliste): variablenliste.remove(name) #fix fuer seiteneffekt von variable_definition_initialization
          if(name in variablenliste): variablenliste.removeall(name)
      arrayname = leftside.split(' ')[1].replace("[]","").replace("=","")
      arraytype = leftside.split(' ')[0].replace("[]","")
      arraydimdict[arrayname] = len(values)
      arraylist.append(arrayname)
      arraytypdict[arrayname] =  arraytype
      return [True,eingabe]
    else:
      arrayname = leftside.split(' ')[1].replace("[]","").replace("=","")
      arraytype = "null"
      arraydimdict[arrayname] = 0
      arraylist.append(arrayname)
      arraytypdict[arrayname] =  arraytype
      return [True,eingabe]
  else: return ["array_definition_initialization_wrong_structure",eingabe]
     
def arrayreassignment(eingabe):
  if(";" not in eingabe): return ["array_reassignment_wrong_semicolon",eingabe]
  patternarrayredef= r"[\s]*[^\s]+[\s]*\[([0-9])+\][\s]*=[\s]*.+;[\s]*"
  if(re.match(patternarrayredef, eingabe)):
    name = eingabe[:eingabe.index('[')]
    if(name not in arraylist): return ["array_reassignment_unknown_array",name]
    if(name not in arraydimdict.keys()): return ["array_no_declaration",eingabe]
    else:
      dim = eingabe[eingabe.index('[')+1:eingabe.index(']')]
      if(int(dim)<0 or int(dim)>=int(arraydimdict[name])): return ["array_reassignment_wrong_dim",str(dim)+" is not "+str(arraydimdict[name])]
      Type = arraytypdict[name]
      valid = variable_definition_initialization(Type+" "+name+" = "+eingabe[eingabe.index('=')+1:],False)[0]
      if(name in variablenliste): variablenliste.remove(name)
      if(name in variablenliste): variablenliste.remove(name)
      if(valid != True): 
        ret = valid.replace("variable_definition_initialization", "array_reassignment")
        #print("wad: "+str(ret))
        if(name in variablenliste): variablenliste.remove(name)
        if(name in variablenliste): variablenliste.remove(name)
        return [ret,Type+" "+name+" = "+eingabe[eingabe.index('=')+1:]+";"]
      else: return [True,eingabe]
        
  else: 
    return ["array_reassignment_wrong_structure",eingabe]

def arrayaccess(eingabe, gettyp):
  patternarrayreacc= r"[\s]*[^\s]+[\s]*\[[0-9]+\][\s]*"
  patternprint = r"System.out.println\([\s]*[^\s]+[\s]*\[[0-9]+\][\s]*\);"
  if(re.match(patternprint, eingabe) or re.match(patternarrayreacc, eingabe)): #re.match(patternarrayreacc, eingabe) or'''
    if(re.match(patternprint, eingabe)): 
      eingabe = eingabe.replace("System.out.println(","")
      eingabe = eingabe.replace(");",";")
    name = eingabe[:eingabe.index('[')].replace(' ','')
    if(name not in arraylist): return ["array_access_unknown_array",name]
    if(name not in arraydimdict.keys()): return ["array_access_no_declaration",name]
    else: 
      index = eingabe[eingabe.index('[')+1:eingabe.index(']')]
      if(int(index) <= int(arraydimdict[name]) or int(index) < 0):
        if(gettyp == False): return [True,eingabe]
        elif(gettyp == True): return [arraytypdict[name],eingabe]
        else:
          print("wrong parameter value")
          exit(-1)
      else: return ["array_access_outofrange",index]
  else: return ["array_access_wrong_structure",eingabe]

#arrays: def, init, zugriff (Operator [])
def multidim_array_definition(eingabe):
  if("[]" not in eingabe or (eingabe.count("[") <= 1 or eingabe.count("]") <=  1)): return ["multidim_array_definition_no_brackets",eingabe]
  if(re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return ["multidim_array_definition_wrong_semicolon",eingabe]

  patterarrdef1 = r"[\s]*[^\s]+[\s]+[^\s]+([\s]*\[\][\s]*)+[\s]*;[\s]*"
  patterarrdef2 = r"[\s]*[^\s]+([\s]*\[\][\s]*)+[\s]+[^\s]+[\s]*;[\s]*"

  if(re.match(patterarrdef1, eingabe) or re.match(patterarrdef2, eingabe)):
    eingabe = eingabe.replace("[]","")
       
    if(variable_definition(eingabe,False)[0] == True):
      arrayname = eingabe.split(' ')[1].replace(';','')
      if(arrayname in arraylist): return ["multidim_array_definition_name_double",arrayname]

      arraylist.append(arrayname)
      arraytypdict[eingabe.split(' ')[1]] = eingabe.split(' ')[0]

      return [True,eingabe]
    else: 
      ret = variable_definition(eingabe,False)[0]
      if(ret != True): ret = ret.replace("variable", "multidim_array")
      return [ret,eingabe]
    
  else: return ["multidim_array_definition_wrong_structure",eingabe]

def multidim_array_declaration(eingabe):
  if("[]" not in eingabe or (eingabe.count("[") <= 1 or eingabe.count("]") <=  1)): return ["array_declaration_no_brackets",eingabe]
  if(not("new" in eingabe)): return ["array_declaration_no_new",eingabe]
  if(re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return ["array_declaration_wrong_semicolon",eingabe]

  patterarrdefinit1 = r"[\s]*[^\s]+[\s]*([\s]*\[\][\s]*)+[\s]*[^\s]+[\s]*=[\s]*new [^\s]+[\s]*(\[[0-9]+\])+[\s]*;[\s]*"
  patterarrdefinit2 = r"[\s]*[^\s]+ [\s]*[^\s]+([\s]*\[\][\s]*)+[\s]*=[\s]*new [^\s]+[\s]*(\[[0-9]+\])+[\s]*;[\s]*"

  if(re.match(patterarrdefinit1, eingabe) or re.match(patterarrdefinit2, eingabe)):
    eingabe = eingabe.replace('  ',' ')
    leftside = eingabe[:eingabe.index("=")]
    rightside = eingabe[eingabe.index("="):]
    dims = re.findall(r"\[[0-9]+\]", rightside)
    if(dims == None or leftside.count("[]") != len(dims)): return ["multidim_array_declaration_bracketnumber_not_matching",leftside]
  
    Type = leftside
    Type = Type.replace("[]","").split(' ')[0]
    if(not(listelinvar(prim_types, Type) or listelinvar(classlist, Type))): return ["array_declaration_non_type",Type]
    else:
      arrayname = leftside.split(' ')[1].replace("[]","").replace(Type,"")
      arraylist.append(arrayname)
      arraytypdict[arrayname] = Type
      
      dimlist = []
      for dim in dims:
        dim = dim.replace('[','').replace(']','')
        if(re.match(r"[0-9]", dim) == None): return ["array_declaration_non_indextype",dim]
        dimlist.append(int(dim))
      arraydimdict[arrayname] = dimlist
      return [True,eingabe]  
  else: return ["multidim_array_declaration_wrong_structure",eingabe]

'''
def multidim_arraydefinitialisation(eingabe):
  if("[]" not in eingabe): return "array_definition_initialization_no_brackets"
  if(not("new" in eingabe or ("{" in eingabe and "}" in eingabe))): return "array_definition_initialization_no_brackets"
  if (re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return "array_definition_initialization_wrong_semicolon"

  patterarrdefinit1 = r"[^\s]+[\s]*(\[\])+ [^\s]+[\s]*=[\s]*new .+"
  patterarrdefinit2 = r"[^\s]+ [\s]*[^\s]+(\[\])+[\s]*=[\s]*new .+"

  if(re.match(patterarrdefinit1, eingabe) or re.match(patterarrdefinit2, eingabe)):
    
    dimensionlist = []
    patternatom = r"[^(\}||\{)]+"
    
    
    eingabe = eingabe.replace('  ',' ')
    leftside = eingabe[:eingabe.index("=")+1].replace("[]","")
    values = eingabe[eingabe.index("{")+1:eingabe.index("}")].replace(" ","").split(",")

    for value in values:
      name = 
      valid = variable_definition_initialization(leftside+" "+value+";")
      if(valid != True):
        ret = variable_definition_initialization(leftside+" "+value+";").replace("variable","array")
        if(name in variablenliste): variablenliste.remove(name)
        if(name in variablenliste): variablenliste.remove(name)
        return ret
      else:
        if(leftside.split(' ')[1] in arraylist): return "array_definition_initialization_name_double"
        if(name in variablenliste): variablenliste.remove(name)
        if(name in variablenliste): variablenliste.remove(name) #fix fuer seiteneffekt von variable_definition_initialization
   
    arrayname = leftside.split(' ')[1].replace("[]","")
    arraytype = leftside.split(' ')[0].replace("[]","")
    arraydimdict[arrayname] = len(values)
    arraylist.append(arrayname)
    arraytypdict[arrayname] =  arraytype
    return [True,eingabe]
  else: return "array_definition_initialization_wrong_structure"
     
'''
def multidim_array_reassignment(eingabe):
  patternarrayredef= r"[\s]*[^\s]+[\s]*\[[0-9]+\][\s]*=[\s]*.+;[\s]*"
  if(re.match(patternarrayredef, eingabe)):
    name = eingabe[:eingabe.index('[')]
    if(name not in arraylist): return ["multidim_array_reassignment_unknown_array",eingabe]
    if(name not in arraydimdict.keys()): return ["multidim_array_reassignment_no_declaration",name]
    else:
      ersterteil = eingabe[:eingabe.index('=')]
      dimteil = ersterteil[ersterteil.index('['):ersterteil.rindex(']')+1]
      i = 0
      for dim in re.findall(r"\[[\d]+\]",dimteil):
        if(int(dim[1:-1]) < 0 or int(dim[1:-1]) > int(arraydimdict[name][i])): return ["multidim_array_reassignment_oof",str(dim[1:-1])+" not in "+str(arraydimdict[name][i])]
        i+=1
      #if(int(dim)<0 or int(dim)>=int(arraydimdict[name])): return ["array_reassignment_wrong_dim",str(dim)+" is not "+str(arraydimdict[name])]

      dimlistacc = re.findall(r"\[[0-9]+\]", eingabe[eingabe.index('['):eingabe.index('=')])
      dimlistarr = arraydimdict[name]
      if(len(dimlistacc) != len(dimlistarr)): return ["multidim_array_reassignment_outof_dim",len(dimlistacc)]
      for i in range(len(dimlistacc)):
        dimlistacc[i] = dimlistacc[i].replace('[','').replace(']','')
        if(int(dimlistacc[i]) < 0 or int(dimlistacc[i]) > dimlistarr[i]): return ["multidim_array_reassignment_outof_dim",dimlistacc]
        
      Type = arraytypdict[name]
      valid = variable_definition_initialization(Type+" "+name+" = "+eingabe[eingabe.index('=')+1:],False)[0]
      if(name in variablenliste): variablenliste.remove(name)
      if(name in variablenliste): variablenliste.remove(name)
      if(valid != True): 
        ret = variable_definition_initialization(Type+" "+name+" = "+eingabe[eingabe.index('=')+1:],False)[0]
        if(ret != True): ret = ret.replace("variable_definition_initialization", "array_reassignment")
        if(name in variablenliste): variablenliste.remove(name)
        if(name in variablenliste): variablenliste.remove(name)
        return [ret,Type+" "+name+" = "+eingabe[eingabe.index('=')+1:]]
      else: return [True,eingabe]
        
  else: 
    return ["multidim_array_reassignment_wrong_structure",eingabe]

def multidim_arrayaccess(eingabe, gettype):
  patternarrayacc= r"[\s]*[^\s]+[\s]*\[[0-9]+\][\s]*[\s]*"
  patternarraysyso= r"System.out.println\([\s]*[^\s]+[\s]*\[[0-9]+\][\s]*[\s]*\)[\s]*;[\s]*"
  if(re.match(patternarrayacc, eingabe) or re.match(patternarraysyso, eingabe)):
    eingabe = eingabe.replace("System.out.println(","")
    a = re.findall(r"[\s]*\)[\s]*;[\s]*",eingabe)
    if(a != None and isinstance(a,list) and len(a) == 1):
      a = a[0]
      if(isinstance(a,str)): eingabe = eingabe.replace(a,"")
    #print(eingabe)
    name = eingabe[:eingabe.index('[')]
    if(name not in arraylist): return ["multidim_array_access_unknown_array",name]
    if(name not in arraydimdict.keys()): return ["multidim_array_access_no_declaration",name]
    else:
      ersterteil = eingabe
      dimteil = ersterteil[ersterteil.index('['):ersterteil.rindex(']')+1]
      i = 0
      for dim in re.findall(r"\[[\d]+\]",dimteil):
        if(int(dim[1:-1]) < 0 or int(dim[1:-1]) > int(arraydimdict[name][i])): return ["multidim_array_access_oof",str(dim[1:-1])+" not in "+str(arraydimdict[name][i])]
        i+=1
        
      dimlistacc = re.findall(r"\[[0-9]+\]", eingabe[eingabe.index('['):])
      dimlistarr = arraydimdict[name]
      if(len(dimlistacc) != len(dimlistarr)): return ["multidim_array_access_outof_dim",len(dimlistacc)]
      for i in range(len(dimlistacc)):
        dimlistacc[i] = dimlistacc[i].replace('[','').replace(']','')
        if(int(dimlistacc[i]) < 0 or int(dimlistacc[i]) > dimlistarr[i]): return ["multidim_array_access_outof_dim",int(dimlistacc[i])]
        
      Type = arraytypdict[name]    
      valid = variable_definition(Type+" "+name+";",False)[0]
      if(valid != True): 
        ret = variable_definition(Type+" "+name+";",False)[0]
        return [ret,Type+" "+name+";"]
      else: return [True,eingabe]
        
  else: 
    return ["multidim_array_access_wrong_structure",eingabe]

'''
CLASSES
'''

def constructordefinition(classname, eingabe):
  eingabe = eingabe.replace(", ",",")
  patternmethoddef = r"[\s]*[^\s]*[\s]*[^\s]*[\s]*[^\s]+ [^\s]+(.*){.*}[\s]*"
  

  if(re.match(patternmethoddef, eingabe)):

    modifiers = []
    name = []
   
    data = eingabe[:eingabe.index('(')].split(' ')   
    patternaccessreturnname = r"[^\s]+ [^\s]+"
    
    if(re.match(patternaccessreturnname, eingabe[:eingabe.index('(')])):
      if(data[0] in accessmodifiers):
        if(data[1] == classname):
          modifiers = [data[0]]
          name = data[1]
        else: return ["constructor_definition_wrong_name",data[1]]
      else: return ["constructor_definition_wrong_modifier",data[0]]
    else: return ["constructor_wrong_structure",eingabe[:eingabe.index('(')]]
    
    methodlist.append(name)
    methodmodifierdict[name] = modifiers
    
    paramlist = eingabe[eingabe.index('(')+1:eingabe.index(')')].split(',').remove('')
    if(paramlist != None):
      for param in paramlist:
        ret = variable_definition(param+";",False)[0]
        if(ret != True): return ["constructor_wrong_variable_definition",param]      

    body = eingabe[eingabe.index('{'):]  
    if(codeblock(body)[0] == True): 
      methodlist.append(name)
      methodmodifierdict[name] = modifiers
      methodparamtypelist[name] = paramlist
      return [True,eingabe]
    else: return ["constructor_wrong_body",codeblock(body)[0]]
  return ["constructor_wrong_structure",eingabe]
   
def methoddefinition(eingabe):
  global variablenliste
  #variablenlistecopy = variablenliste.copy()
  variablenlistecopy = []
  for e in variablenliste:
    variablenlistecopy.append(e)
    
  eingabe = eingabe.replace(", ",",")
  patternmethoddef = r"[\s]*[^\s]*[\s]*[^\s]*[\s]*[^\s]+ [^\s]+(.*){.*}[\s]*"
  if(re.match(patternmethoddef, eingabe)):
    modifiers = []
    name = []
    returntype = ""
   
    data = eingabe[:eingabe.index('(')].split(' ')
    
    patternvollstaendig = r"[^\s]+ [^\s]+ [^\s]+ [^\s]+"
    patternaccessreturnname = r"[^\s]+ [^\s]+ [^\s]+"
    patternreturnname = r"[^\s]+ [^\s]+"
    if(re.match(patternvollstaendig, eingabe[:eingabe.index('(')])):
      if(data[0] in accessmodifiers or data[0] == "static"):
        if(data[1] in accessmodifiers or data[1] == "static" and data[1] != data[0]):
          if(data[2] in prim_types or data[2] == "void"):
            if(identifier(data[3])[0] == True):
              if(data[1] == data[0]): return ["method_definition_wrong_modifier",data[1]]
              modifiers = [data[0],data[1]]
              returntype = data[2]
              name = data[3]
            else: return ["method_definition_no_identifier",data[3]]
          else: 
            #print(data[2])
            return ["method_definition_wrong_type",data[2]]
        else: return ["method_definition_wrong_modifier",data[1]]
      else: return ["method_definition_wrong_modifier",data[0]]
    elif(re.match(patternaccessreturnname, eingabe[:eingabe.index('(')])):
      if(data[0] in accessmodifiers or data[0] == "static"):
        if(data[1] in prim_types or data[1] == "void"):
          if(identifier(data[2])[0] == True):
            modifiers = [data[0]]
            returntype = data[1]
            name = data[2]
          else: return ["method_definition_no_identifier",data[2]]
        else: return ["method_definition_wrong_type",data[1]]
      else: return ["method_definition_wrong_modifier",data[0]]
    elif(re.match(patternreturnname, eingabe[:eingabe.index('(')])):
      if(data[0] == "void" or data[0] in prim_types):
        if(identifier(data[1])[0] == True):
            returntype = data[0]
            name = data[1]
        else: return ["method_definition_no_identifier",data[1]]
      else: return ["method_definition_wrong_type",data[0]]
      
    pre = eingabe[:eingabe.index('(')].split(' ')
    if(len(pre) < 2): return ["method_definition_wrong_structure",eingabe]  
    returntype = pre[len(pre)-2]
    name = pre[len(pre)-1]
    
    paramlist = eingabe[eingabe.index('(')+1:eingabe.index(')')].split(',')
    if('' in paramlist): paramlist = paramlist.remove('')
    if(paramlist != None):
      for param in paramlist:
        ret = variable_definition(param+";",False)[0]
        if(name in variablenliste): variablenliste.remove(name)
        if(name in variablenliste): variablenliste.remove(name)
        if(ret != True and ret != "variable_definition_name_double"): 
          ret = arraydefinition(param+";")[0]
          if(name in variablenliste): variablenliste.remove(name)
          if(name in variablenliste): variablenliste.remove(name)
          if(ret != True and ret != "array_definition_name_double"): 
            #print(ret)
            return ["method_definition_wrong_variable_definition",param]   
    else: paramlist = []  
    body = eingabe[eingabe.index('{'):]  
    if(codeblock(body)[0] == True): 
      #pruefe rueckgabetyp
      if("return" in body):
        rueckgabe = body[body.index('return')+6:body.index('}')]
        rueckgabe = rueckgabe[:rueckgabe.index(';')]
        rueckgabetyp = gettype(rueckgabe)
        #print(rueckgabe+" "+str(rueckgabetyp))
        if(inel(rueckgabetyp,returntype) != True):return ["method_definition_wrong_return", rueckgabe+" is not of the type "+returntype]
      
      methodlist.append(name)
      methodreturndict[name] = returntype
      methodmodifierdict[name] = modifiers
      methodparamtypelist[name] = paramlist
      variablenliste = variablenlistecopy
      return [True,eingabe]
    else: return [codeblock(body)[0],body]
  else: return ["method_definition_wrong_structure",eingabe]

def methodmoddef(eingabe):
  cmod = False
  mods = []
  for m in accessmodifiers: mods.append(m)
  mods.append("static")
  for mod in mods:
    if(mod in eingabe):
      eingabe = eingabe.replace(mod,"")
      cmod = True
  if(cmod == False):return ["method_defintion_no_mod",eingabe]
  return [methoddefinition(eingabe)[0],eingabe]
  
  
  
def methodaccess(eingabe,expression):
  patternmethodaccess1 = r"[\s]*[^\s]+[^\s]*\(.*\)(;)?[\s]*"
  #if(expression == False):
  #  if(re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe): return ["method_access_wrong_semicolon",eingabe]
  
  if(re.match(patternmethodaccess1, eingabe)):
    name = eingabe[:eingabe.index('(')]
    if(name not in methodlist): return ["method_access_unknown_method",name]
    #patternparam = r"[[^\s]?[,[^\s]?[^\s]+]*[^\s]?"
    parameterlist = eingabe[eingabe.index('(')+1:eingabe.index(')')].split(',')
    if('' in parameterlist): parameterlist = parameterlist.remove('')
    if(parameterlist == None): parameterlist = []
    if(parameterlist != [] and methodparamtypelist[name] != []):
      paramtypelist = methodparamtypelist[name]
      if(len(paramtypelist) != len(parameterlist)): return ["method_access_parameter_mismatch","The definition has a different number of parameters ("+str(len(paramtypelist))+")"]
      for i in range(eingabe[eingabe.index('(')+1:eingabe.index(')')].count(',')+1):
        param = parameterlist[i].replace(",","").replace(' ','')
        typeparam = ""
        if(param in variablenliste): typeparam = variablentypdict[param]
        elif(getLiteraltype(param)[0] != "Error"): typeparam = getLiteraltype(param)[0]
        if(inel(typeparam,paramtypelist[i].split(' ')[0]) == False):    
          return ["method_access_parameter_mismatch",str(paramtypelist[i]).split(' ')[0]+" "+str(typeparam)]
      return [True,eingabe]
    elif(len(parameterlist) != len(methodparamtypelist[name])):
      return ["method_access_parameter_mismatch",eingabe]
    else: 
      return [True,eingabe]
  return ["method_access_wrong_structure",eingabe]

def classdefinition_inheritance(eingabe):
  patternclassdefinitionextends = r"[\s]*[^\s]*[\s]*class [^\s]+[\s]*extends [^\s]+[\s]*{.*}[\s]*"
  if(re.match(patternclassdefinitionextends, eingabe)): return classdefinition(eingabe)
  else: return ["inheritance_wrong_structure",eingabe]

def classdefinition(eingabe):
  global variablenliste
  #variablenlistcopy = variablenliste.copy()
  variablenlistecopy = []
  for e in variablenliste:
    variablenlistecopy.append(e)
  patternclassdefinition = r"[\s]*[^\s]*[\s]*class [^\s]+[\s]*{.*}[\s]*"
  patternclassdefinitionextends = r"[\s]*[^\s]*[\s]*class [^\s]+[\s]*extends [^\s]+[\s]*{.*}[\s]*"
  
  if("class" not in eingabe): return ["class_definition_no_keyword",eingabe]
  if("{" not in eingabe or "}" not in eingabe): return ["class_definition_no_curly_brackets",eingabe]
    
  if(re.match(patternclassdefinitionextends, eingabe)):  
    parentname = eingabe[eingabe.index('extends')+7:eingabe.index('{')]
    while(parentname.startswith(' ')):parentname=parentname[1:]
    while(parentname.endswith(' ')):parentname=parentname[:-1]
    if(parentname not in classlist): 
      return ["inheritance_non_parent",eingabe]
    else: 
      eingabe = eingabe.replace(eingabe[eingabe.index('extends'):eingabe.index('{')],"")
      

  if(re.match(patternclassdefinition, eingabe)):
    head = eingabe[:eingabe.index('{')]
    
    modifier = ""
    name =""
    
    data = head.split(' ')
    
    patternmodifiername = r"[\s]*[^\s]+ [\s]*[^\s]+ [\s]*[^\s]+"
    patternnname = r"[^\s]+[\s]* [^\s]+[\s]*"
    
    if(re.match(patternmodifiername, head)):
      if(data[0] in accessmodifiers):
        if(identifier(data[2])[0] == True):
          modifier = data[0]
          name = data[2]
        else: return ["class_definition_invalid_identifier",data[2]]
      else: return ["class_definition_invalid_accessmodifier",data[0]]
    elif(re.match(patternnname, head)):
      if(identifier(data[1])[0] == True):
          name = data[1]
      else: return ["class_definition_invalid_identifier",data[1]]

    if(name in classlist): return ["class_definition_name_double",name]

   
    body = eingabe[eingabe.index('{')+1:eingabe.rindex('}')]#rindex bloed
    varmetdef = ""
    classmethodenliste = []
    classvariablenliste = []
    if(body != ""):
      for token in body.split(' '):
        varmetdef += token
        if(variable_definition(varmetdef,False)[0] == True):
          classvariablenliste.append(varmetdef[:-1])
          varmetdef = ""
          continue
        elif(variable_definition_initialization(varmetdef,False)[0] == True):
          classvariablenliste.append(varmetdef[:-1])
          varmetdef = "" 
          continue 
        elif(methoddefinition(varmetdef)[0] == True):
          classmethodenliste.append(varmetdef) 
          varmetdef = ""
          continue 
        elif(constructordefinition(name, varmetdef)[0] == True):
          varmetdef = ""
          continue 
        else: 
          varmetdef+=" "
          continue
    if(varmetdef != ""): 
      #print("class_definition error: "+varmetdef)
      return ["class_illegal_classblock",varmetdef]
    else: 
      classvariablendict[name] = []
      classmethodendict[name] = []
      for var in classvariablenliste:
        classvariablendict[name].append(var)
      for met in classmethodenliste:
        classmethodendict[name].append(met)
      
      classlist.append(name)
      classmodifierdict[name] = modifier
      variablenliste = variablenlistecopy
      return [True,eingabe]
  else: return ["class_definition_wrong_structure",eingabe]
   
def class_definition_with_modifier(eingabe):
  ret = False
  for mod in ["static","abstract","final"]:
    if mod in eingabe:
      ret = True
      eingabe = eingabe.replace(mod,"")
      break
  if(ret == False): return ["class_definition_no_mod",eingabe]    
  else: return [classdefinition(eingabe)[0],eingabe] 


def class_definition_with_access_modifier(eingabe):
  ret = [False,""]
  for mod in ["public","private","protected"]:
    if mod in eingabe:
      ret = True
      if(eingabe.startswith(mod)!=True): 
        return ["class_definition_wrong_structure",""]      
      eingabe = eingabe.replace(mod,"")
  if(ret == [False,""]): return ["class_definition_no_access_mod",eingabe]    
  else: return [classdefinition(eingabe)[0],eingabe]
   
   
def membervariable_access(eingabe):
  patternobjacc = r"[\s]*[^\s]+\.[^\s]+[\s]*"
  if(re.match(patternobjacc, eingabe)):
    data = eingabe[:-1].split('.',1)
    if(data[0] not in objectlist): return ["member_access_variables_unknown_object",data[0]]
    else:
      classofobj = objecttoclassdict[data[0]]
      #print(classofobj)
      #print(classvariablendict[classofobj])
      for member in classvariablendict[classofobj]:
        if(data[1] in member): return [True,eingabe]
      return ["member_access_variables_unknown_member",data[1]]
     
  else: return ["member_access_variables_wrong_structure",eingabe]
  
  
def membermethodaccess(eingabe,expression):
  patternobjacc = r"[\s]*[^\s]+\.[^\s]+\(.*\)(;)?[\s]*"
  if(expression == False): 
    if(re.match("[^;]*[\s]*;[\s]*", eingabe) == None or re.match("[^;]*[\s]*;[\s]*", eingabe).group(0) != eingabe):
      return ["method_access_wrong_semicolon",eingabe]
  if(re.match(patternobjacc, eingabe)):
    data = eingabe[:-1].split('.',1)
    if(data[0] not in objectlist): 
      return ["member_access_methods_unknown_object",data[0]]
    else:
      classofobj = objecttoclassdict[data[0]]
      for member in classmethodendict[classofobj]:
        modmemname = member[:member.index('(')].split(' ')
        modmemname = modmemname[len(modmemname)-1]
        if(modmemname == data[1][:data[1].index('(')]):
          a = methodaccess(data[1], False)
          return a
      return ["member_access_methods_unknown_member",data[1]]
     
  else: return ["member_access_methods_wrong_structure",eingabe]

def parse(eingabe, parsecommand):
    rennew() 
    #print(eingabe+" "+str(parsecommand))
    #print(parsecommand)
    if(' ' in parsecommand): parsecommand = parsecommand.split(' ')
    if(isinstance(parsecommand, list)): a = multiparse(eingabe, parsecommand)
    else: a = parse_wre(eingabe,parsecommand)
    return a
  
def parse_wre(eingabe, typ):
  typ = typ.replace('\r','')
  while("  " in eingabe):eingabe = eingabe.replace('  ',' ')
  eingabe = eingabe.replace('\n',' ')
     
  #programm structure
  if(typ == "programm_structure_main"): return main(eingabe)
  elif(typ == "programm_structure_import"): return imports(eingabe)
  elif(typ == "programm_structure_packages"): return packages(eingabe)
  
  #basics
  elif(typ == "comments"): return comments(eingabe)
  elif(typ == "identifiers"): return identifier(eingabe)
  elif(typ == "keywords"): return keyword(eingabe)
  elif(typ == "types"): return types(eingabe)
  elif(typ == "literals"): return literal(eingabe)
  elif(typ == "integer_literals"): return integerLiteral(eingabe)
  elif(typ == "floating-point_literals"): return floatLiteral(eingabe)
  elif(typ == "character_literals"): return charLiteral(eingabe)
  elif(typ == "string_literals"): return stringLiteral(eingabe)
  elif(typ == "boolean_literals"): return booleanLiteral(eingabe)
  elif(typ == "null_literal"): return nullLiteral(eingabe)
  elif(typ == "variable_definition"): return variable_definition(eingabe,True)
  elif(typ == "variable_definition_initialization"): return variable_definition_initialization(eingabe,True)
  elif(typ == "variable_reassignment"):return variable_reassignment(eingabe)
  elif(typ == "variable_access"): return variable_access(eingabe)
  elif(typ == "assignments"):return variable_reassignment(eingabe)
  
  #arrays
  elif(typ == "array_definition"): return arraydefinition(eingabe)
  elif(typ == "array_declaration"): return array_declaration(eingabe)
  elif(typ == "array_definition_initialization"): return arraydefinitialisation(eingabe)
  elif(typ == "array_reassignment"): return arrayreassignment(eingabe)
  elif(typ == "array_access"): return arrayaccess(eingabe,False)
  elif(typ == "multidim_array_definition"): return multidim_array_definition(eingabe) #TODO
  elif(typ == "multidim_array_declaration"): return multidim_array_declaration(eingabe) #TODO
  #elif(typ == "multidim_array_definition_initialisation"): return multidim_arraydefinitialisation(eingabe) #TODO
  elif(typ == "multidim_array_reassignment"): return multidim_array_reassignment(eingabe) #TODO
  elif(typ == "multidim_array_access"): return multidim_arrayaccess(eingabe,False) #TODO

  #operators
  elif(typ == "arithmetic_operators"): return arops(eingabe,False)
  elif(typ == "operators_prefix"): return preincdec(eingabe,False)
  elif(typ == "operators_postfix"): return postincdec(eingabe,False)
  elif(typ == "class_and_method_operators"): return memberaccess(eingabe)
  elif(typ == "logic_operators"): return logicops(eingabe, False)
  elif(typ == "comparison_operators"): return compops(eingabe, False)
  elif(typ == "assignment_operators"): return assignops(eingabe, False)
  elif(typ == "bitwise_operators"): return bitop(eingabe, False)
  
  #statements
  elif(typ == "expressions"): return expression(eingabe)
  elif(typ == "statements"): return statement(eingabe)
  elif(typ == "code_blocks"): return codeblock(eingabe)
  
  #controll structures
  elif(typ == "boolean_expression"): return booleanexpression(eingabe)
  elif(typ == "if"): return if_statements(eingabe)
  elif(typ == "while"): return while_statements(eingabe)
  elif(typ == "switch"): return switch_statement(eingabe)
  elif(typ == "do_while"): return do_while_statement(eingabe)
  elif(typ == "extended_for"): return extended_for_statement(eingabe)
  elif(typ == "for"): return for_statement(eingabe)
  elif(typ == "break"): return matchbreak(eingabe)
  elif(typ == "continue"): return matchcontinue(eingabe)
  
  #methods
  elif(typ == "method_definition"): return methoddefinition(eingabe)
  elif(typ == "method_modifiers"): return methodmoddef(eingabe)
  elif(typ == "method_access"): return methodaccess(eingabe, False)

  #classes
  elif(typ == "class_definition"): return classdefinition(eingabe)
  elif(typ == "class_definition_inheritance"): return classdefinition_inheritance(eingabe)
  elif(typ == "access_modifiers"): return class_definition_with_access_modifier(eingabe)
  elif(typ == "class_modifiers"):return class_definition_with_modifier(eingabe)
  elif(typ == "object_declaration"): return variable_definition_initialization(eingabe)
  elif(typ == "class_fields"): return classdefinition(eingabe)
  elif(typ == "member_access_variables"): return membervariable_access(eingabe)
  elif(typ == "member_access_methods"): return membermethodaccess(eingabe,False)

  else: 
    print("Command \""+str(typ)+"\" cannot be parsed!")
    print(str(typ)=="method_access")
    print(repr(typ)+"!="+"method_access")
    print(str(typ)==str("method_access"))
    exit(-1)
    
    
def multiparse(eingabe, befehle):
  #print("test"+eingabe)
  rennew()
  #befehle = befehle.split(' ')
  if(len(befehle) < 2):
    print("falsche eingabe fuer multiparse: "+str(befehle))
    exit(-1)
  wort = ""
  inc = 0
  for token in eingabe.split(' '):
    if(token == ""): continue
    wort += token+' '
    #print(wort+" "+befehle[inc])
    if(inc == len(befehle) and wort!=""): 
      #print(wort+" "+befehle[inc])
      return parse_wre(wort, befehle[inc])
    if(parse_wre(wort, befehle[inc])[0] == True):
      wort = ""
      inc += 1
    #else: print(parse_wre(wort, befehle[inc])[0])
  if(wort != ""):
    return parse_wre(wort, befehle[inc])
  else: return [True, eingabe] 

