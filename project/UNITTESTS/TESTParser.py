'''
Created on 09.04.2019

@author: Johannes
'''
import unittest

'''
Created on 26.03.2019

@author: johan
'''

import os
import sys
sys.path.append(os.path.abspath('../lehre'))
from javaparsing.parser import parse,multiparse #@Unresolvedimport

class Test(unittest.TestCase):
    
  def multiparse(self):
    '''
    if(multiparse("short c; c", ["variable_definition","variable_access"])[0] != True): raise AssertionError("variable_access")
    if(multiparse("short c; System.out.println(c);", ["variable_definition","variable_access"])[0] != True): raise AssertionError("variable_access")
   
    if(multiparse("short c; c=0;", ["variable_definition","variable_reassignment"])[0] != True): raise AssertionError("variable_reassignment")       
    if(multiparse("short c; c = 9;", ["variable_definition","variable_reassignment"])[0] != True): raise AssertionError("variable_reassignment")       
    if(multiparse("short c; c=null;", ["variable_definition","variable_reassignment"])[0] != True): raise AssertionError("variable_reassignment")       

    if(multiparse("int c; ++c", ["variable_definition","operators_prefix"])[0] != True): raise AssertionError("operators_prefix")      
    if(multiparse("int c; c--", ["variable_definition","operators_postfix"])[0] != True): raise AssertionError("operators_postfix")      
    if(multiparse("String c; c=\"anna\";", ["variable_definition","assignment_operators"])[0] != True): raise AssertionError("assignment_operators")      
    if(multiparse("short c; c<<2", ["variable_definition","bitwise_operators"])[0] != True): raise AssertionError("bitwise_operators")     
    if(multiparse("short c; switch(c)break;", ["variable_definition","switch"])[0] != True): raise AssertionError("switch")      
    if(multiparse("int c[]; for(int k: c)break;", ["array_definition","extended_for"])[0] != True): raise AssertionError("extended_for")      
    if(multiparse("void test(){} test();", ["method_definition","method_access"])[0] != True): raise AssertionError("method_access")      
    if(multiparse("int c[] = new int[2]; c[0]", ["array_declaration","array_access"])[0] != True): raise AssertionError("array_access")      
    if(multiparse("int c[] = new int[2]; c[0] = 5;", ["array_declaration","array_reassignment"])[0] != True): raise AssertionError("array_reassignment")      
    if(multiparse("int c[][] = new int[2][2]; c[0][1]", ["multidim_array_declaration","multidim_array_access"])[0] != True): raise AssertionError("multidim_array_access")      
    if(multiparse("int c[][] = new int[2][2]; c[0][1]=2;", ["multidim_array_declaration","multidim_array_reassignment"])[0] != True): raise AssertionError("multidim_array_reassignment")      
    if(multiparse("class A{} A a = new A();", ["class_definition","object_declaration"])[0] != True): raise AssertionError("object_declaration")   
    if(multiparse("class Person{String name;} Person tom = new Person(); tom.name", ["class_definition","variable_definition_initialization","member_access_variables"])[0] != True): raise AssertionError("member_access_variables")   
    if(multiparse("class Abstract{void test(){}} Abstract A = new Abstract(); A.test();", ["class_definition","variable_definition_initialization","member_access_methods"])[0] != True): raise AssertionError("member_access_methods")   
    '''
    pass
    

    
  def testcorrect_ws(self):
    a=""
    b=[]
    '''
    '''
    #lesson: programm_structure
  
    b.append(parse("   public      static      void      main(String   a[]){}","programm_structure_main"))
    b.append(parse("public   static   void   main(String[]   a){}","programm_structure_main"))
    b.append(parse("  import   a  ;  ","programm_structure_import"))
    b.append(parse("  package   a  ;  ","programm_structure_packages"))
    #lesson: basics
    b.append(parse("// a","comments"))
    b.append(parse("int","types"))
    b.append(parse("float","types"))
    b.append(parse("String","types"))
    b.append(parse("char","types"))
    b.append(parse("byte","types"))
  
    b.append(parse("    {  }   ","code_blocks"))
    b.append(parse("    { int a; }   ","code_blocks"))
    b.append(parse("id","identifiers"))
    b.append(parse("id1","identifiers"))
  
    b.append(parse("int","keywords"))
    b.append(parse("2","literals"))
    b.append(parse("2","integer_literals"))
    b.append(parse("0xA","integer_literals"))
    b.append(parse("02","integer_literals"))
    b.append(parse("0b01","integer_literals"))
    b.append(parse("2.0","floating-point_literals"))
    b.append(parse("2.21E3D","floating-point_literals"))
    b.append(parse("\"\"","string_literals"))
    b.append(parse("'a'","character_literals"))
    b.append(parse("true","boolean_literals"))
    b.append(parse("null","null_literal"))
    b.append(parse("int a  ;  ","variable_definition"))
    b.append(parse("int a  =  9  ;  ","variable_definition_initialization"))

    #lesson: operators
    b.append(parse("  2 + 2  ","arithmetic_operators"))
    b.append(multiparse("int c; ++c", ["variable_definition","operators_prefix"]))
    b.append(multiparse("int c; c++",["variable_definition", "operators_postfix"]))
    b.append(parse("2  <  3","comparison_operators"))
    b.append(parse("  true  ||    false || 3 <2  ","logic_operators"))
    #print("TEST1")
    b.append(multiparse("int k; k = 3",["variable_definition", "assignment_operators"]))
    b.append(multiparse("int k; k  | 3",["variable_definition", "bitwise_operators"]))
    b.append(multiparse("int a; a  =  3;",["variable_definition","variable_reassignment"]))
    b.append(multiparse("int a; a  = a|  3;",["variable_definition","variable_reassignment"]))
    #b.append(multiparse("int a; a = 3 + 2 + 5 | 2 << 2;",["variable_definition","variable_reassignment"]))
        
    #lesson: controll_structures
    b.append(parse("true","boolean_expression"))
    b.append(parse(" if  (  true  )  ; ","if"))
    b.append(parse("if(  true )  {  }  ","if"))
    b.append(parse("if(  true )  {  }  ","if"))
    b.append(parse("if(  true )  {  int a;}  ","if"))
    b.append(parse("while(1<2)break;","while"))
    b.append(parse("  while  (  true )  ; ","while"))
    b.append(parse(" while  (true  ) {  } ","while"))
    b.append(parse("do{}while(true);","do_while"))
    b.append(parse("for(;;);","for"))
    b.append(multiparse("int c; switch(c)break;",["variable_definition","switch"]))
    b.append(multiparse("int c[]; for(int k: c)break;", ["array_definition","extended_for"]))
    b.append(multiparse("int c[]; for(int k: c)break;", ["array_definition","extended_for"]))
    b.append(parse(" for ( ; ; ) ; ","for"))
    b.append(parse("for(;;) { } ","for"))
    b.append(parse("for(int d;;) ; ","for"))
    b.append(parse("for(int g=0;;);","for"))
    b.append(parse("for(int d;;){}","for"))
    b.append(parse("for(int g=0;;){}","for"))
    b.append(multiparse("short c; switch(c)break;", ["variable_definition","switch"]))
    b.append(parse("break;","break"))
    b.append(parse("continue;","continue"))
    #lesson: methods
    b.append(parse("void test(){}","method_definition"))
    b.append(parse("public void test(){}","method_definition"))
    b.append(parse("static void test(){}","method_definition"))
    b.append(parse("public static void test(){}","method_definition"))
    b.append(multiparse("void test(){} test();", ["method_definition","method_access"]))
    b.append(parse("void test(){}","method_definition"))
    #lessons: arrays
    b.append(parse("int a[] = { 1 , 2 };","array_definition_initialization"))
    b.append(parse("int[] a = { 1 , 2 };","array_definition_initialization"))
    b.append(parse("char a[] = {'a','b'};","array_definition_initialization"))
    b.append(parse("char a[] = {'a',12};","array_definition_initialization"))
    b.append(parse("int a[] = new int[2];","array_declaration"))
    b.append(parse("int[] a = new int[2];","array_declaration"))
    b.append(parse("int a[];","array_definition"))
    b.append(parse("int[] a;","array_definition"))
    b.append(multiparse("int c[] = new int[2]; c[0]", ["array_declaration","array_access"]))
    b.append(multiparse("int c[] = new int[2]; c[0] = 5;", ["array_declaration","array_reassignment"]))
    b.append(multiparse("int c[] = new int[2]; c[0] = null;", ["array_declaration","array_reassignment"]))
    b.append(parse("int a[][];","multidim_array_definition"))
    b.append(parse("int[][] a;","multidim_array_definition"))
    b.append(multiparse("int c[][] = new int[2][2]; c[0][1]=2;", ["multidim_array_declaration","multidim_array_reassignment"]))
    b.append(multiparse("int a[][] = new int[2][2]; a[0][0] = 1;", ["multidim_array_declaration","multidim_array_reassignment"]))
    b.append(multiparse("int c[][] = new int[2][2]; c[0][1]=null;", ["multidim_array_declaration","multidim_array_reassignment"])) 

    #lesson: classes
    b.append(parse("class A {} ","class_definition"))
    b.append(parse("class A {public A(){}} ","class_definition"))    
    b.append(parse("class A {} class B extends A{}","class_definition class_definition_inheritance"))    
    b.append(parse("abstract class A {} ","class_modifiers"))
    b.append(parse("public class A {} ","access_modifiers"))
    b.append(multiparse("class Person{String name;} Person tom = new Person(); tom.name", ["class_definition","variable_definition_initialization","member_access_variables"])) 
    b.append(multiparse("class Abstract{void test(){}} Abstract A = new Abstract(); A.test();",["class_definition","variable_definition_initialization","member_access_methods"]))
    b.append(parse("class A{}","class_definition"))
  
    '''
    '''
    correct = True
    for k in b:
      if("True" not in str(k[0])):
        print("incorrect: "+str(k))
        correct = False
    if(correct):
      #print("all correct")     
      pass
                   
  def testall_errors(self):
    a = 0
    #lesson: programm_structure
    if(parse("a","programm_structure_main")[0] != "main_wrong"): raise AssertionError("main_wrong")
    if(parse("a;","programm_structure_import")[0] != "import_no_keyword"): raise AssertionError("import_no_keyword")
    if(parse("import a","programm_structure_import")[0] != "import_wrong_semicolon"): raise AssertionError("import_wrong_semicolon")
    if(parse("import 1;","programm_structure_import")[0] != "import_identifier"): raise AssertionError("import_identifier")
    if(parse("import a.*.*;","programm_structure_import")[0] != "import_error_wildcard"): raise AssertionError("import_error_wildcard")
    if(parse(" a.import*; ","programm_structure_import")[0] != "import_wrong_structure"): raise AssertionError("import_wrong_structure")
    if(parse("    a  ;  ","programm_structure_packages")[0] != "package_no_keyword"): raise AssertionError("package_no_keyword")
    if(parse("  package   a ","programm_structure_packages")[0] != "package_wrong_semicolon"): raise AssertionError("package_wrong_semicolon")
    if(parse("  package   1a  ;  ","programm_structure_packages")[0] != "package_indentifier"): raise AssertionError("package_indentifier")
    if(parse("    a package ;  ","programm_structure_packages")[0] != "package_wrong_structure"): raise AssertionError("package_wrong_structure")
    if(parse("7","identifiers")[0] != "identifiers_digit"): raise AssertionError("identifiers_digit")  

    #lesson: basics
    if(parse("int","identifiers")[0] != "identifiers_keyword"): raise AssertionError("identifiers_keyword")
    if(parse("null","identifiers")[0] != "identifiers_null_boolean"): raise AssertionError("identifiers_null_boolean")
    if(parse("  a","comments")[0] != "comments_non"): raise AssertionError("comments_non")
    if(parse("/*  */a","comments")[0] != "comments_multiline_wrong_structure"): raise AssertionError("comments_multiline_wrong_structure")
    if(parse("  a","comments")[0] != "comments_non"): raise AssertionError("comments_non")
    if(parse("a","types")[0] != "types_non"): raise AssertionError("types_non")
    if(parse("a","keywords")[0] != "keyword_non"): raise AssertionError("keyword_non")
    if(parse("0b","integer_literals")[0] != "integer_literals_binary_not_empty"): raise AssertionError("integer_literals_binary_not_empty")
    if(parse("0x","integer_literals")[0] != "integer_literals_hex_not_empty"): raise AssertionError("integer_literals_hex_not_empty")
    if(parse("0b2","integer_literals")[0] != "integer_literals_non_binary"): raise AssertionError("integer_literals_non_binary")
    if(parse("0xZ","integer_literals")[0] != "integer_literals_non_hex"): raise AssertionError("integer_literals_non_hex")
    if(parse("09","integer_literals")[0] != "integer_literals_non_octal"): raise AssertionError("integer_literals_non_octal")
    if(parse("R","integer_literals")[0] != "integer_literals_non_decimal"): raise AssertionError("integer_literals_non_decimal")
    if(parse("2,0","floating-point_literals")[0] != "float_literals_no_point"): raise AssertionError("float_literals_no_point")
    if(parse("Eafw2.0","floating-point_literals")[0] != "float_literals_wrong_prefix"): raise AssertionError("float_literals_wrong_prefix")
    if(parse("a","string_literals")[0] != "string_literal_non"): raise AssertionError("string_literal_non")
    if(parse("a","character_literals")[0] != "char_literal_non"): raise AssertionError("char_literal_non")
    if(parse("a","boolean_literals")[0] != "boolean_literals_non"): raise AssertionError("boolean_literals_non")
    if(parse("a","null_literal")[0] != "null_literal_non"): raise AssertionError("null_literal_non")
    if(parse("int 5  ;  ","variable_definition")[0] != "variable_definition_non_identifier"): raise AssertionError("variable_definition_non_identifier")
    #NICHT PRUEFBAR MIT EINER ANSWEISUNG
      #if(parse("int a  ;  ","variable_definition")[0] != "variable_definition_name_double"): raise AssertionError("")
      #if(parse("int a  ","variable_definition")[0] != "variable_definition_wrong_semicolon"): raise AssertionError("")

    if(parse("awd a  ;  ","variable_definition")[0] != "variable_definition_non_type"): raise AssertionError("variable_definition_non_type")
    if(parse(" ;  ","variable_definition")[0] != "variable_definition_wrong_structure"): raise AssertionError("variable_definition_wrong_structure")
    if(parse("int a  =  9    ","variable_definition_initialization")[0] != "variable_definition_initialization_wrong_semicolon"): raise AssertionError("variable_definition_initialization_wrong_semicolon")
    if(parse("byte a  =  214414;","variable_definition_initialization")[0] != "integer_literals_byte_oor"): raise AssertionError("integer_literals_byte_oor")
    if(parse("short a  =  999999999999999;    ","variable_definition_initialization")[0] != "integer_literals_short_oor"): raise AssertionError("integer_literals_short_oor")
    if(parse("int a  =  99999999999;","variable_definition_initialization")[0] != "integer_literals_int_oor"): raise AssertionError("integer_literals_int_oor")
    if(parse("long a  =  99999999999999999999999;","variable_definition_initialization")[0] != "integer_literals_long_oor"): raise AssertionError("integer_literals_long_oor")
    if(parse("char a  =  999999999999;","variable_definition_initialization")[0] != "integer_literals_char_oor"): raise AssertionError("integer_literals_char_oor")
    if(parse("kal a  =  9  ;  ","variable_definition_initialization")[0] != "variable_definition_initialization_non_type"):     raise AssertionError("variable_definition_initialization_non_type")
    if(parse("int 1a  =  9  ;  ","variable_definition_initialization")[0] != "variable_definition_initialization_non_identifier"):  raise AssertionError("variable_definition_initialization_non_identifier")
    if(parse("System.out.println(a,.);","variable_access")[0] != "variable_access_wrong_structure"): raise AssertionError("variable_access_unknown")
    if(parse("System.out.println(awfawa);","variable_access")[0] != "variable_access_unknown"): raise AssertionError("variable_access_unknown")
    #KEINE FEHLER -> ASSIGNOPS
      #if(parse("a  =  9;","variable_reassignment")[0] != "main_wrong"): raise AssertionError("") 
      #if(parse("a=9;","variable_reassignment")[0] != "main_wrong"): raise AssertionError("")
      #if(parse("a=9;","variable_reassignment")[0] != "main_wrong"): raise AssertionError("")
    #lesson: arrays
    if(parse("int a;","array_definition")[0] != "array_definition_no_brackets"): raise AssertionError("array_definition_no_brackets") 
    if(parse("int [];","array_definition")[0] != "array_definition_wrong_structure"): raise AssertionError("array_definition_wrong_structure") 
    if(parse("int 1a[];","array_definition")[0] != "array_definition_non_identifier"): raise AssertionError("array_definition_non_identifier") 

    if(parse("bla 1a[];","array_definition")[0] != "array_definition_non_type"): raise AssertionError("array_definition_non_type") 
    #if(parse("int a[];","array_definition") != "array_definition_name_double"): raise AssertionError("") 
    if(parse("int ;a[]","array_definition")[0] != "array_definition_wrong_semicolon"): raise AssertionError("array_definition_wrong_semicolon") 
    if(parse("int a[] = int[2];","array_declaration")[0] != "array_declaration_no_new"): raise AssertionError("array_declaration_no_new") 
    if(parse("int a[] = new int[2]","array_declaration")[0] != "array_declaration_wrong_semicolon"): raise AssertionError("array_declaration_wrong_semicolon") 
    #if(parse("int a[] = new int[2];","array_declaration") != "array_declaration_name_double"): raise AssertionError("") 
    if(parse("hsre a[] = new int[2];","array_declaration")[0] != "array_declaration_non_type"): raise AssertionError("array_declaration_non_type") 
    if(parse("int a[] = new String[2];","array_declaration")[0] != "array_declaration_wrong_type"): raise AssertionError("array_declaration_wrong_type") 
    if(parse("int a[] new int[2];","array_declaration")[0] != "array_declaration_wrong_structure"): raise AssertionError("array_declaration_wrong_structure") 
    if(parse("int a[] = { 1 , 2 ;","array_definition_initialization")[0] != "array_definition_initialization_no_brackets"): raise AssertionError("array_definition_initialization_no_brackets") 
    if(parse("int a[] = { 1 , 2 }","array_definition_initialization")[0] != "array_definition_initialization_wrong_semicolon"): raise AssertionError("array_definition_initialization_wrong_semicolon") 
    #if(parse("int a[] = { 1 , 2 };","array_definition_initialization")[0] != "array_definition_initialization_name_double"): raise AssertionError("") 
    if(parse("bla a[] = { 1 , 2 };","array_definition_initialization")[0] != "array_definition_initialization_non_type"): raise AssertionError("array_definition_initialization_non_type") 
    if(parse("String a[] = { 1 , 2 };","array_definition_initialization")[0] != "array_definition_initialization_typemismatch_string"): raise AssertionError("array_definition_initialization_typemismatch_string") 
    if(parse("int a[] { 1 , 2 };","array_definition_initialization")[0] != "array_definition_initialization_wrong_structure"): raise AssertionError("array_definition_initialization_wrong_structure") 
    if(parse("System.out.println(rsr[0]);","array_access")[0] != "array_access_unknown_array"): raise AssertionError("array_access_unknown_array") 
    if(parse("System.out.println(ar]);","array_access")[0] != "array_access_wrong_structure"): raise AssertionError("array_access_wrong_structure") 
    #if(parse("System.out.println(ar[1000]);","array_access")[0] != "array_access_outofrange"): raise AssertionError("array_access_outofrange") 
    #if(parse("System.out.println(a]);","array_access")[0] != "array_access_no_declaration"): raise AssertionError("") 
    if(parse("nom\";","array_reassignment")[0] != "array_reassignment_wrong_structure"): raise AssertionError("array_reassignment_wrong_structure") 
    if(parse("alpha[0]=\"tom\";","array_reassignment")[0] != "array_reassignment_unknown_array"): raise AssertionError("array_reassignment_unknown_array") 
    #if(parse("names[0]=2awd;","array_reassignment")[0] != "array_reassignment_typemismatch_string"): raise AssertionError("array_reassignment_typemismatch_string") 
    #if(parse("names[0]=2;","array_reassignment")[0] != "array_reassignment_typemismatch_string"): raise AssertionError("array_reassignment_typemismatch_string") 
    #if(parse("names[0]=\"tom\";","array_reassignment")[0] != "array_reassignment_name_double"): raise AssertionError("") 
    if(parse("awf a[][] int;","multidim_array_definition")[0] != "multidim_array_definition_wrong_structure"): raise AssertionError("multidim_array_definition_wrong_structure")
    if(parse("awf a[][] int","multidim_array_definition")[0] != "multidim_array_definition_wrong_semicolon"): raise AssertionError("multidim_array_definition_wrong_semicolon")
    if(parse("awf a;","multidim_array_definition")[0] != "multidim_array_definition_no_brackets"): raise AssertionError("multidim_array_definition_no_brackets")
    #if(parse("int a[][];","multidim_array_definition")[0] != "multidim_array_definition_name_double"): raise AssertionError("")
    if(parse("wafwa a[][];","multidim_array_definition")[0] != "multidim_array_definition_non_type"): raise AssertionError("multidim_array_definition_non_type")
    #if(parse("a[0][1000] = 1;","multidim_array_reassignment")[0] != "multidim_array_reassignment_outof_dim"): raise AssertionError("multidim_array_reassignment_outof_dim") 
    if(parse("awwfa[0][0] = 1;","multidim_array_reassignment")[0]!= "multidim_array_reassignment_unknown_array"): raise AssertionError("multidim_array_reassignment_unknown_array") 
    if(multiparse("int a[][] = new int[1][1]; a[110][0] = 1;",["multidim_array_declaration","multidim_array_reassignment"])[0]!= "multidim_array_reassignment_oof"): raise AssertionError("multidim_array_reassignment_oof") 
    if(parse("a[0awfaw][231^2121230] = 1;","multidim_array_reassignment")[0]!= "multidim_array_reassignment_wrong_structure"): raise AssertionError("multidim_array_reassignment_wrong_structure") 
    #if(parse("a[0][0] = 1;","multidim_array_reassignment")[0]!= "multidim_array_reassignment_no_declaration"): raise AssertionError("") 
    #lesson: operators
    if(parse("  2 2  ","arithmetic_operators")[0] != "arithmetic_operators_no_operator"): raise AssertionError("arithmetic_operators_no_operator")   
    if(parse("2 + 2 2","arithmetic_operators")[0] != "arithmetic_operators_wrong_structure"): raise AssertionError("arithmetic_operators_wrong_structure") 
    if(parse("  2 + true  ","arithmetic_operators")[0] != "arithmetic_operators_wrong_type"): raise AssertionError("arithmetic_operators_wrong_type")   
    if(parse("1;","operators_prefix")[0] != "preincdec_no_operator"): raise AssertionError("preincdec_no_operator")
    if(parse("++a;","operators_prefix")[0] != "preincdec_wrong_type"): raise AssertionError("preincdec_wrong_type")
    if(parse("1++;","operators_prefix")[0] != "preincdec_wrong_structure"): raise AssertionError("preincdec_wrong_structure")
    if(parse("1;","operators_postfix")[0] != "postincdec_no_operator"): raise AssertionError("postincdec_no_operator")
    if(parse("a--;","operators_postfix")[0] != "postincdec_wrong_type"): raise AssertionError("postincdec_wrong_type")
    if(parse("--1;","operators_postfix")[0] != "postincdec_wrong_structure"): raise AssertionError("postincdec_wrong_structure")
    if(parse("2 3","comparison_operators")[0] != "comparison_operators_no_operator"): raise AssertionError("comparison_operators_no_operator")
    if(parse("2  <  3 2","comparison_operators")[0] != "comparison_operators_wrong_structure"): raise AssertionError("comparison_operators_wrong_structure")
    if(parse("2  <  false","comparison_operators")[0] != "comparison_operators_wrong_type"): raise AssertionError("comparison_operators_wrong_type")
    if(parse("  true","logic_operators")[0] != "logic_operators_no_operator"): raise AssertionError("logic_operators_no_operator")
    if(parse("  true  ||","logic_operators")[0] != "logic_operators_wrong_structure"): raise AssertionError("logic_operators_wrong_structure")
    if(parse("  true  ||    3  ","logic_operators")[0] != "logic_operators_wrong_type"): raise AssertionError("logic_operators_wrong_type")
    if(parse("  true  ||   2 false  ","logic_operators")[0] != "logic_operators_wrong_structure"): raise AssertionError("logic_operators_wrong_structure")
    if(parse("c2","assignment_operators")[0] != "assignment_operators_no_operator"):raise AssertionError("assignment_operators_no_operator")
    if(parse("=2","assignment_operators")[0] != "assignment_operators_wrong_structure"): raise AssertionError("assignment_operators_wrong_structure")
    if(parse("1=2","assignment_operators")[0] != "assignment_operators_badLType"): raise AssertionError("assignment_operators_badLType")
    #if(parse("c=2 2","assignment_operators")[0] != "assignment_operators_wrong_structure"): raise AssertionError("assignment_operators_wrong_structure")
    #if(parse("c=2","assignment_operators")[0] != "assignment_operators_wrong_type"): raise AssertionError("")
    if(parse("=2","assignment_operators")[0] != "assignment_operators_wrong_structure"): raise AssertionError("assignment_operators_wrong_structure")
    if(parse("k  | 3 3","bitwise_operators")[0] != "bitwise_operators_wrong_structure"): raise AssertionError("bitwise_operators_wrong_structure")
    if(parse("k  3","bitwise_operators")[0] != "bitwise_operators_no_operator"): raise AssertionError("bitwise_operators_no_operator")
    #if(parse("k  | false","bitwise_operators")[0] != "bitwise_operators_wrong_type"): raise AssertionError("bitwise_operators_wrong_type")
    if(parse("k  |  2 3","bitwise_operators")[0] != "bitwise_operators_wrong_structure"): raise AssertionError("bitwise_operators_wrong_structure")
    #lesson: statements
    if(parse("awfwaf","expressions")[0] != "expression_non"): raise AssertionError("expression_non")
    if(parse("awfwaf;","statements")[0] != "statement_non"): raise AssertionError("statement_non")
    if(parse("awfwaf","code_blocks")[0] != "codeblock_no_brackets"): raise AssertionError("codeblock_no_brackets")
    if(parse("{wafwaf}","code_blocks")[0] != "codeblock_no_statement"):  raise AssertionError("codeblock_no_statement")
    #lesson: controll_structures
    if(parse("awfw","boolean_expression")[0] != "boolean_expression_non"): raise AssertionError("boolean_expression_non")   
    if(parse("  (  true  )  ; ","if")[0] != "if_no_keyword"): raise AssertionError("if_no_keyword")
    if(parse(" if  ((  true  )  ; ","if")[0] != "if_brackets_not_matching"): raise AssertionError("if_brackets_not_matching")
    if(parse(" if  (  afwa  )  ; ","if")[0] != "if_no_boolean_expression"): raise AssertionError("if_no_boolean_expression")
    if(parse(" if  (  true  ){wafwa} ","if")[0] != "if_non_codeblock"): raise AssertionError("if_non_codeblock")
    if(parse(" if  (  true  )awfwaf; ","if")[0] != "if_non_statement"): raise AssertionError("if_non_statement")
    if(parse(" if  )( ; ","if")[0] != "if_wrong_structure"): raise AssertionError("if_wrong_structure")
    if(parse("    (  true )  ; ","while")[0] != "while_no_keyword"): raise AssertionError("while_no_keyword")
    if(parse("  while    true )  ; ","while")[0] != "while_brackets_not_matching"): raise AssertionError("while_brackets_not_matching")
    if(parse("  while  (  bib )  ; ","while")[0] != "while_no_boolean_expression"): raise AssertionError("while_no_boolean_expression")
    if(parse("  while  (  true )  wafw; ","while")[0] != "while_non_statement"): raise AssertionError("while_non_statement")
    if(parse("  while  (  true )  {awd} ","while")[0] != "while_non_codeblock"): raise AssertionError("while_non_codeblock")
    if(parse("  while  (  true )  break; break; ","while")[0] != "while_break"): raise AssertionError("while_break")
    if(parse("  while  (  true )  continue; continue; ","while")[0] != "while_continue"): raise AssertionError("while_continue")
    if(parse("    (  true )  ;while ","while")[0] != "while_wrong_structure"): raise AssertionError("while_wrong_structure")  
    if(parse("do{}(true);","do_while")[0] != "do_while_no_keyword"): raise AssertionError("do_while_no_keyword")
    if(parse("do{}whiletrue);","do_while")[0] != "do_while_round_brackets_not_matching"): raise AssertionError("do_while_round_brackets_not_matching")
    if(parse("do{while(true);","do_while")[0] != "do_while_curly_brackets_not_matching"): raise AssertionError("do_while_curly_brackets_not_matching")
    if(parse("do{}while(awd);","do_while")[0] != "do_while_no_boolean_expression"): raise AssertionError("do_while_no_boolean_expression")
    if(parse("do{awdwa}while(true);","do_while")[0] != "do_while_non_codeblock"): raise AssertionError("do_while_non_codeblock")
    if(parse("do{break;break;}while(true);","do_while")[0] != "do_while_break"): raise AssertionError("do_while_break")
    if(parse("do{continue;continue;}while(true);","do_while")[0] != "do_while_continue"): raise AssertionError("do_while_continue")
    if(parse("while(true)do{};","do_while")[0] != "do_while_wrong_structure"): raise AssertionError("do_while_wrong_structure")
    if(parse("(;;);","for")[0] != "for_no_keyword"): raise AssertionError("for_no_keyword")
    if(parse("for(awd;;);","for")[0] != "for_no_variable_definition"): raise AssertionError("for_no_variable_definition")
    if(parse("for(;awf;);","for")[0] != "for_no_boolean_expression"): raise AssertionError("for_no_boolean_expression")
    if(parse("for(;;afw);","for")[0] != "for_no_increment"): raise AssertionError("for_no_increment")
    if(parse("for(;;){break ;break ;}","for")[0] != "for_break"): raise AssertionError("for_break")
    if(parse("for(;;){continue;continue;}","for")[0] != "for_continue"): raise AssertionError("for_continue")
    if(parse("for(;;){wafw}","for")[0] != "for_noncode_block"): raise AssertionError("for_noncode_block")
    if(parse("for(;;)wdaadw;","for")[0] != "for_nonstatement"): raise AssertionError("for_nonstatement")
    if(parse("for(;;awff;","for")[0] != "for_wrong_structure"): raise AssertionError("for_wrong_structure")
    if(parse("(int b:ar);","extended_for")[0] != "extended_for_no_keyword"): raise AssertionError("extended_for_no_keyword")
    if(parse("for(awf awf:ar);","extended_for")[0] != "extended_for_no_variable_definition"): raise AssertionError("extended_for_no_variable_definition")
    if(parse("for(int b:awdawdr);","extended_for")[0] != "extended_for_nonarray"): raise AssertionError("extended_for_nonarray")
    #if(parse("for(String b:ar);","extended_for")[0] != "extended_for_varar_mismatch"): raise AssertionError("extended_for_varar_mismatch")
    #if(parse("for(int b:ar){wf}","extended_for")[0] != "extended_for_noncode_block"): raise AssertionError("extended_for_noncode_block")
    #if(parse("for(int b:ar)awf;","extended_for")[0] != "extended_for_nonstatement"): raise AssertionError("extended_for_nonstatement")
    #if(parse("for(int b:ar){break;break;}","extended_for")[0] != "extended_for_break"): raise AssertionError("extended_for_break")
    #if(parse("for(int b:ar){continue;continue;}","extended_for")[0] != "extended_for_continue"): raise AssertionError("extended_for_continue")
    #if(parse("for nt b:ar);","extended_for")[0] != "extended_for_wrong_structure"): raise AssertionError("extended_for_wrong_structure")
    #if(parse("(c)break;","switch")[0] != "switch_no_keyword"): raise AssertionError("switch_no_keyword")
    if(parse("switchc)break;","switch")[0] != "switch_round_brackets_not_matching"): raise AssertionError("switch_round_brackets_not_matching")
    #if(parse("switch(c){","switch")[0] != "switch_curly_brackets_not_matching"): raise AssertionError("switch_curly_brackets_not_matching")
    if(parse("switch(1)break;","switch")[0] != "switch_non_variable"): raise AssertionError("switch_non_variable")
    #if(parse("switch(c){default: break;}","switch")[0] != "switch_wrong_default"): raise AssertionError("switch_wrong_default")
    #if(parse("switch(c){case 0: awfa}","switch")[0] != "switch_wrong_structure"): raise AssertionError("switch_wrong_structure")
    #if(parse("switch(c){case awd: awfaw;}","switch")[0] != "switch_varval_mismatch"): raise AssertionError("switch_varval_mismatch")
    #if(parse("switch(c){case 0: awfaw;}","switch")[0] != "switch_wrong_case"): raise AssertionError("switch_wrong_case")  
    #if(parse("switch(c){case 0: {break; break;}}","switch")[0] != "switch_wrong_case"): raise AssertionError("switch_wrong_case")
    #lesson: methods
    if(parse("test(){}","method_definition")[0] != "method_definition_wrong_structure"): raise AssertionError("method_definition_wrong_structure")   
    if(parse("void 1(){}","method_definition")[0] != "method_definition_no_identifier"): raise AssertionError("method_definition_no_identifier")   
    if(parse("awd test(){}","method_definition")[0] != "method_definition_wrong_type"): raise AssertionError("method_definition_wrong_type")   
    if(parse("awfaw void test(){}","method_definition")[0] != "method_definition_wrong_modifier"): raise AssertionError("method_definition_wrong_modifier")   
    if(parse("void test(awda){}","method_definition")[0] != "method_definition_wrong_variable_definition"): raise AssertionError("method_definition_wrong_variable_definition")   
    if(parse("int test(){return 'a';}","method_definition")[0] != "method_definition_wrong_return"): raise AssertionError("method_definition_wrong_return")   
    #if(parse("add(}","method_access")[0] != "method_access_wrong_structure"): raise AssertionError("method_access_wrong_structure")   
    #if(parse("bla(1,2);","method_access")[0] != "method_access_unknown_method"): raise AssertionError("method_access_unknown_method")   
    #if(parse("add(1);","method_access")[0] != "method_access_parameter_mismatch"): raise AssertionError("method_access_parameter_mismatch")   
    #if(parse("add(1,'2');","method_access")[0] != "method_access_parameter_mismatch"): raise AssertionError("method_access_parameter_mismatch")   
    #if(parse("void test(){}","method_modifiers")[0] != "method_defintion_no_mod"): raise AssertionError("method_defintion_no_mod")   
    
    #lesson: classes
    if(parse(" A {} ","class_definition")[0] != "class_definition_no_keyword"): raise AssertionError("class_definition_no_keyword")
    if(parse("class A { ","class_definition")[0] != "class_definition_no_curly_brackets"): raise AssertionError("class_definition_no_curly_brackets")
    if(parse("class 1A {} ","class_definition")[0] != "class_definition_invalid_identifier"): raise AssertionError("class_definition_invalid_identifier")
    if(parse("awf class A {} ","class_definition")[0] != "class_definition_invalid_accessmodifier"): raise AssertionError("class_definition_invalid_accessmodifier")
    if(parse("class A {awd} ","class_definition")[0] != "class_illegal_classblock"): raise AssertionError("class_illegal_classblock")
    if(parse("class awd s A {} ","class_definition")[0] != "class_definition_wrong_structure"): raise AssertionError("class_definition_wrong_structure")
    #if(parse("class A {} ","class_definition")[0] != "class_definition_name_double"): raise AssertionError("")  
    if(parse("class A {} class B extends C{}","class_definition class_definition_inheritance")[0] != "inheritance_non_parent"): raise AssertionError("class_definition_inheritance")  
    if(parse("class A {} class B extend C{}","class_definition class_definition_inheritance")[0] != "inheritance_wrong_structure"): raise AssertionError("inheritance_wrong_structure")  
    if(parse("class A {} ","class_modifiers")[0] != "class_definition_no_mod"): raise AssertionError("class_definition_no_mod")
    if(parse("abstract class A {} ","access_modifiers")[0] != "class_definition_no_access_mod"): raise AssertionError("class_definition_no_access_mod")
    #if(parse("tom.;","member_access_variables")[0] != "member_access_variables_wrong_structure"): raise AssertionError("member_access_variables_wrong_structure")
    #if(parse("wad.name;","member_access_variables")[0] != "member_access_variables_unknown_object"): raise AssertionError("member_access_variables_unknown_object")
    #if(parse("tom.namawde;","member_access_variables")[0] != "member_access_variables_unknown_member"): raise AssertionError("member_access_variables_unknown_member")
    #if(parse("test().A;","member_access_methods")[0] != "member_access_methods_wrong_structure"): raise AssertionError("member_access_methods_wrong_structure")
    #if(parse("AB.test();","member_access_methods")[0] != "member_access_methods_unknown_object"): raise AssertionError("member_access_methods_unknown_object")
    #if(parse("A.tawdest();","member_access_methods")[0] != "member_access_methods_unknown_member"): raise AssertionError("member_access_methods_unknown_member")
    #print("all errors")
    pass
    
    
    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
