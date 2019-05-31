'''
Created on 09.04.2019

@author: Johannes
'''
import unittest
from project.lehre.Expertenmodell import Expertenmodell
from project.lehre.Syntaxkonzept import Syntaxkonzept

ep = Expertenmodell("en")

class Test(unittest.TestCase): 

  def testMC(self): 
    #lesson: programm_structure
    if(ep.bewerten("programm_structure", "programm_structure_main", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc programm_structure_main: wrong result")
    if(ep.bewerten("programm_structure", "programm_structure_import", "test_mc", 0, "1") != "fehlerfrei"): raise AssertionError("mc programm_structure_import: wrong result")
    if(ep.bewerten("programm_structure", "programm_structure_packages", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc programm_structure_packages: wrong result")
    if(ep.bewerten("programm_structure", "programm_structure_packages", "test_mc", 1, "1;2") != "fehlerfrei"): raise AssertionError("mc programm_structure_packages2: wrong result")

    #lesson: basics
    if(ep.bewerten("basics", "comments", "test_mc", 0, "1;2") != "fehlerfrei"): raise AssertionError("mc comments: wrong result")
    if(ep.bewerten("basics", "comments", "test_mc", 1, "1;3") != "fehlerfrei"): raise AssertionError("mc comments2: wrong result")
    if(ep.bewerten("basics", "comments", "test_mc", 2, "1;2;3") != "fehlerfrei"): raise AssertionError("mc comments3: wrong result")
    if(ep.bewerten("basics", "keywords", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc keywords: wrong result")
    if(ep.bewerten("basics", "keywords", "test_mc", 1, "1;2") != "fehlerfrei"): raise AssertionError("mc keywords2: wrong result")
    if(ep.bewerten("basics", "keywords", "test_mc", 2, "1") != "fehlerfrei"): raise AssertionError("mc keywords3: wrong result")
    if(ep.bewerten("basics", "literals", "test_mc", 0, "1") != "fehlerfrei"): raise AssertionError("mc literals: wrong result")
    if(ep.bewerten("basics", "literals", "test_mc", 1, "4") != "fehlerfrei"): raise AssertionError("mc literals2: wrong result")
    if(ep.bewerten("basics", "literals", "test_mc", 2, "1") != "fehlerfrei"): raise AssertionError("mc literals3: wrong result")
    if(ep.bewerten("basics", "integer_literals", "test_mc", 0, "3") != "fehlerfrei"): raise AssertionError("mc integer_literals: wrong result")
    if(ep.bewerten("basics", "integer_literals", "test_mc", 1, "2;4") != "fehlerfrei"): raise AssertionError("mc integer_literals2: wrong result")
    if(ep.bewerten("basics", "floating-point_literals", "test_mc", 0, "3;2") != "fehlerfrei"): raise AssertionError("mc floating-point_literals: wrong result")
    if(ep.bewerten("basics", "character_literals", "test_mc", 0, "3,4,1") != "fehlerfrei"): raise AssertionError("mc character_literals: wrong result")
    if(ep.bewerten("basics", "string_literals", "test_mc", 0, "2,3") != "fehlerfrei"): raise AssertionError("mc string_literals: wrong result")
    if(ep.bewerten("basics", "boolean_literals", "test_mc", 0, "1,4") != "fehlerfrei"): raise AssertionError("mc boolean_literals: wrong result")
    if(ep.bewerten("basics", "boolean_literals", "test_mc", 1, "2") != "fehlerfrei"): raise AssertionError("mc boolean_literals2: wrong result")
    if(ep.bewerten("basics", "null_literal", "test_mc", 0, "1") != "fehlerfrei"): raise AssertionError("mc null_literal: wrong result")
    if(ep.bewerten("basics", "null_literal", "test_mc", 1, "3") != "fehlerfrei"): raise AssertionError("mc null_literal2: wrong result")
    if(ep.bewerten("basics", "identifiers", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc identifiers: wrong result")
    if(ep.bewerten("basics", "identifiers", "test_mc", 1, "4,3") != "fehlerfrei"): raise AssertionError("mc identifiers2: wrong result")
    if(ep.bewerten("basics", "identifiers", "test_mc", 2, "1") != "fehlerfrei"): raise AssertionError("mc identifiers3: wrong result")
    if(ep.bewerten("basics", "types", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc types: wrong result")
    if(ep.bewerten("basics", "variable_definition", "test_mc", 0, "1") != "fehlerfrei"): raise AssertionError("mc variable_definition: wrong result")
    if(ep.bewerten("basics", "variable_definition", "test_mc", 1, "3,4") != "fehlerfrei"): raise AssertionError("mc variable_definition2: wrong result")
    if(ep.bewerten("basics", "variable_definition_initialization", "test_mc", 0, "1")!= "fehlerfrei"): raise AssertionError("mc variable_definition_initialization: wrong result")
    if(ep.bewerten("basics", "variable_access", "test_mc", 0, "3,1") != "fehlerfrei"): raise AssertionError("mc variable_access: wrong result")
    if(ep.bewerten("basics", "variable_reassignment", "test_mc", 0, "1,3") != "fehlerfrei"): raise AssertionError("mc variable_reassignment: wrong result")

    #arrays
    if(ep.bewerten("arrays", "array_definition", "test_mc", 0, "1,2") != "fehlerfrei"): raise AssertionError("mc array_definition: wrong result")
    if(ep.bewerten("arrays", "array_declaration", "test_mc", 0, "3,2,1") != "fehlerfrei"): raise AssertionError("mc array_declaration: wrong result")
    if(ep.bewerten("arrays", "array_definition_initialization", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc array_definition_initialization: wrong result")
    if(ep.bewerten("arrays", "array_access", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc array_access: wrong result")
    if(ep.bewerten("arrays", "array_reassignment", "test_mc", 0, "1") != "fehlerfrei"): raise AssertionError("mc array_reassignment: wrong result")
    if(ep.bewerten("arrays", "multidim_array_definition", "test_mc", 0, "3") != "fehlerfrei"): raise AssertionError("mc multidim_array_definition: wrong result")
    if(ep.bewerten("arrays", "multidim_array_declaration", "test_mc", 0, "1,2") != "fehlerfrei"): raise AssertionError("mc multidim_array_declaration: wrong result")
    if(ep.bewerten("arrays", "multidim_array_access", "test_mc", 0, "5") != "fehlerfrei"): raise AssertionError("mc multidim_array_access: wrong result")
    if(ep.bewerten("arrays", "multidim_array_reassignment", "test_mc", 0, "4") != "fehlerfrei"): raise AssertionError("mc multidim_array_reassignment: wrong result")

    #lesson: operators
    if(ep.bewerten("operators", "arithmetic_operators", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc arithmetic_operators: wrong result")
    if(ep.bewerten("operators", "operators_prefix", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc operators_prefix: wrong result")
    if(ep.bewerten("operators", "operators_postfix", "test_mc", 0, "1") != "fehlerfrei"): raise AssertionError("mc operators_postfix: wrong result")
    if(ep.bewerten("operators", "comparison_operators", "test_mc", 0, "3") != "fehlerfrei"): raise AssertionError("mc comparison_operators: wrong result")
    if(ep.bewerten("operators", "logic_operators", "test_mc", 0, "1") != "fehlerfrei"): raise AssertionError("mc logic_operators: wrong result")
    if(ep.bewerten("operators", "bitwise_operators", "test_mc", 0, "2,3") != "fehlerfrei"): raise AssertionError("mc bitwise_operators: wrong result")
    if(ep.bewerten("operators", "assignment_operators", "test_mc", 0, "2,3") != "fehlerfrei"): raise AssertionError("mc assignment_operators: wrong result")
    
    #lesson: statements
    if(ep.bewerten("statements", "expressions", "test_mc", 0, "1;2;4") != "fehlerfrei"): raise AssertionError("mc expressions: wrong result")
    if(ep.bewerten("statements", "statements", "test_mc", 0, "1,3,2,4") != "fehlerfrei"): raise AssertionError("mc statements: wrong result")
    if(ep.bewerten("statements", "code_blocks", "test_mc", 0, "1") != "fehlerfrei"): raise AssertionError("mc code_blocks: wrong result")
    if(ep.bewerten("statements", "code_blocks", "test_mc", 1, "1,2,3") != "fehlerfrei"): raise AssertionError("mc code_blocks2: wrong result")
    if(ep.bewerten("statements", "code_blocks", "test_mc", 2, "3") != "fehlerfrei"): raise AssertionError("mc code_blocks3: wrong result")

    #lesson: controll_structures
    if(ep.bewerten("controll_structures", "boolean_expression", "test_mc", 0, "4,2") != "fehlerfrei"): raise AssertionError("mc boolean_expression: wrong result")
    if(ep.bewerten("controll_structures", "if", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc if: wrong result")
    if(ep.bewerten("controll_structures", "switch", "test_mc", 0, "1") != "fehlerfrei"): raise AssertionError("mc switch: wrong result")
    if(ep.bewerten("controll_structures", "switch", "test_mc", 1, "1,4,3") != "fehlerfrei"): raise AssertionError("mc switch2: wrong result")
    if(ep.bewerten("controll_structures", "while", "test_mc", 0, "4") != "fehlerfrei"): raise AssertionError("mc while: wrong result")
    if(ep.bewerten("controll_structures", "do_while", "test_mc", 0, "1,2") != "fehlerfrei"): raise AssertionError("mc do_while: wrong result")
    if(ep.bewerten("controll_structures", "for", "test_mc", 0, "2,3") != "fehlerfrei"): raise AssertionError("mc for: wrong result")
    if(ep.bewerten("controll_structures", "extended_for", "test_mc", 0, "1") != "fehlerfrei"): raise AssertionError("mc extended_for: wrong result")
    if(ep.bewerten("controll_structures", "break", "test_mc", 0, "4") != "fehlerfrei"): raise AssertionError("mc break: wrong result")
    if(ep.bewerten("controll_structures", "continue", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc continue: wrong result")

    #lesson: methods
    if(ep.bewerten("methods", "method_definition", "test_mc", 0, "1,2,3") != "fehlerfrei"): raise AssertionError("mc method_definition: wrong result")
    if(ep.bewerten("methods", "method_modifiers", "test_mc", 0, "1,2,3") != "fehlerfrei"): raise AssertionError("mc method_modifiers: wrong result")
    if(ep.bewerten("methods", "method_access", "test_mc", 0, "1,3,2") != "fehlerfrei"): raise AssertionError("mc method_access: wrong result")

    #lesson: classes
    if(ep.bewerten("classes", "class_definition", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc class_definition: wrong result")
    if(ep.bewerten("classes", "class_modifiers", "test_mc", 0, "1,2,3") != "fehlerfrei"): raise AssertionError("mc class_modifiers: wrong result")
    if(ep.bewerten("classes", "access_modifiers", "test_mc", 0, "3") != "fehlerfrei"): raise AssertionError("mc access_modifiers: wrong result")
    if(ep.bewerten("classes", "object_declaration", "test_mc", 0, "2") != "fehlerfrei"): raise AssertionError("mc object_declaration: wrong result")
    if(ep.bewerten("classes", "class_fields", "test_mc", 0, "1") != "fehlerfrei"): raise AssertionError("mc class_fields: wrong result")
    if(ep.bewerten("classes", "member_access_variables", "test_mc", 0, "1,2") != "fehlerfrei"): raise AssertionError("mc member_access_variables: wrong result")
    if(ep.bewerten("classes", "member_access_methods", "test_mc", 0, "1,2") != "fehlerfrei"): raise AssertionError("mc member_access_methods: wrong result")
    pass


  def testLT(self): 
    #lesson: programm_structure
    if(ep.bewerten("programm_structure", "programm_structure_main", "test_lt", 0, "void") != "fehlerfrei"): raise AssertionError("lt programm_structure_main: wrong result")
    if(ep.bewerten("programm_structure", "programm_structure_main", "test_lt", 1, "application") != "fehlerfrei"): raise AssertionError("lt programm_structure_main2: wrong result")
    if(ep.bewerten("programm_structure", "programm_structure_import", "test_lt", 0, "reference") != "fehlerfrei"): raise AssertionError("lt programm_structure_import: wrong result")
    if(ep.bewerten("programm_structure", "programm_structure_import", "test_lt", 1, "beginning") != "fehlerfrei"): raise AssertionError("lt programm_structure_import2: wrong result")
    if(ep.bewerten("programm_structure", "programm_structure_import", "test_lt", 2, ";") != "fehlerfrei"): raise AssertionError("lt programm_structure_import3: wrong result")
    if(ep.bewerten("programm_structure", "programm_structure_packages", "test_lt", 0, ".") != "fehlerfrei"): raise AssertionError("lt programm_structure_packages: wrong result")

    #lesson: basics
    if(ep.bewerten("basics", "comments", "test_lt", 0, "/") != "fehlerfrei"): raise AssertionError("lt comments: wrong result")
    if(ep.bewerten("basics", "keywords", "test_lt", 0, "float") != "fehlerfrei"): raise AssertionError("lt keywords: wrong result")
    if(ep.bewerten("basics", "literals", "test_lt", 0, "1") != "fehlerfrei"): raise AssertionError("lt literals: wrong result")
    if(ep.bewerten("basics", "literals", "test_lt", 1, ".") != "fehlerfrei"): raise AssertionError("lt literals2: wrong result")
    if(ep.bewerten("basics", "integer_literals", "test_lt", 0, "0b") != "fehlerfrei"): raise AssertionError("lt integer_literals: wrong result")
    if(ep.bewerten("basics", "integer_literals", "test_lt", 1, "int") != "fehlerfrei"): raise AssertionError("lt integer_literals2: wrong result")
    if(ep.bewerten("basics", "integer_literals", "test_lt", 2, "0b10;") != "fehlerfrei"): raise AssertionError("ltinteger_literals3: wrong result")
    if(ep.bewerten("basics", "floating-point_literals", "test_lt", 0, "9.8F;") != "fehlerfrei"): raise AssertionError("lt floating-point_literals: wrong result")
    if(ep.bewerten("basics", "floating-point_literals", "test_lt", 1, "9.8D;") != "fehlerfrei"): raise AssertionError("lt floating-point_literals2: wrong result")
    if(ep.bewerten("basics", "character_literals", "test_lt", 0, "'b'") != "fehlerfrei"): raise AssertionError("lt character_literals: wrong result")
    if(ep.bewerten("basics", "string_literals", "test_lt", 0, "\"a\"") != "fehlerfrei"): raise AssertionError("lt string_literals: wrong result")
    if(ep.bewerten("basics", "string_literals", "test_lt", 1, "\"tree\"") != "fehlerfrei"): raise AssertionError("lt string_literals2: wrong result")
    if(ep.bewerten("basics", "boolean_literals", "test_lt", 1, "false") != "fehlerfrei"): raise AssertionError("lt boolean_literals: wrong result")
    if(ep.bewerten("basics", "boolean_literals", "test_lt", 0, "false") != "fehlerfrei"): raise AssertionError("lt boolean_literals2: wrong result")
    if(ep.bewerten("basics", "null_literal", "test_lt", 0, "true") != "fehlerfrei"): raise AssertionError("lt null_literal: wrong result")
    if(ep.bewerten("basics", "null_literal", "test_lt", 1, "null") != "fehlerfrei"): raise AssertionError("lt null_literal2: wrong result")
    if(ep.bewerten("basics", "identifiers", "test_lt", 0, "a") != "fehlerfrei"): raise AssertionError("lt identifiers: wrong result")
    if(ep.bewerten("basics", "types", "test_lt", 0, "float, double") != "fehlerfrei"): raise AssertionError("lt types: wrong result")
    if(ep.bewerten("basics", "types", "test_lt", 1, "boolean") != "fehlerfrei"): raise AssertionError("lt types2: wrong result")
    if(ep.bewerten("basics", "variable_definition", "test_lt", 0, "double a") != "fehlerfrei"): raise AssertionError("lt variable_definition: wrong result")
    if(ep.bewerten("basics", "variable_definition_initialization", "test_lt", 0, "\"jerry\"") != "fehlerfrei"): raise AssertionError("lt variable_definition_initialization: wrong result")
    if(ep.bewerten("basics", "variable_access", "test_lt", 0, "var") != "fehlerfrei"): raise AssertionError("lt variable_access: wrong result")
    if(ep.bewerten("basics", "variable_reassignment", "test_lt", 0, "\"anna\"") != "fehlerfrei"): raise AssertionError("lt variable_reassignment: wrong result")

    #arrays
    if(ep.bewerten("arrays", "array_definition", "test_lt", 0, "[5];") != "fehlerfrei"): raise AssertionError("lt array_definition: wrong result")
    if(ep.bewerten("arrays", "array_declaration", "test_lt", 0, "[]=new int[10];") != "fehlerfrei"): raise AssertionError("lt array_declaration: wrong result")
    if(ep.bewerten("arrays", "array_definition_initialization", "test_lt", 0, "{1,2,3};") != "fehlerfrei"): raise AssertionError("lt array_definition_initialization: wrong result")
    if(ep.bewerten("arrays", "array_definition_initialization", "test_lt", 1, "\"tom\"") != "fehlerfrei"): raise AssertionError("lt array_definition_initialization2: wrong result")
    if(ep.bewerten("arrays", "array_access", "test_lt", 0, "[0]") != "fehlerfrei"): raise AssertionError("lt array_access: wrong result")
    if(ep.bewerten("arrays", "array_access", "test_lt", 1, "b[0]+b[1]+b[2]") != "fehlerfrei"): raise AssertionError("lt array_access2: wrong result")
    if(ep.bewerten("arrays", "array_reassignment", "test_lt", 0, "[2]") != "fehlerfrei"): raise AssertionError("lt array_reassignment: wrong result")
    if(ep.bewerten("arrays", "array_reassignment", "test_lt", 1, "[0]") != "fehlerfrei"): raise AssertionError("lt array_reassignment2: wrong result")
    if(ep.bewerten("arrays", "multidim_array_definition", "test_lt", 0, "[][][]") != "fehlerfrei"): raise AssertionError("lt multidim_array_definition: wrong result")
    if(ep.bewerten("arrays", "multidim_array_declaration", "test_lt", 0, "[2]") != "fehlerfrei"): raise AssertionError("lt multidim_array_declaration: wrong result")
    if(ep.bewerten("arrays", "multidim_array_access", "test_lt", 0, "[0][1];") != "fehlerfrei"): raise AssertionError("lt multidim_array_access: wrong result")
    if(ep.bewerten("arrays", "multidim_array_reassignment", "test_lt", 0, "[1][0]") != "fehlerfrei"): raise AssertionError("lt multidim_array_reassignment: wrong result")

    #lesson: operators
    if(ep.bewerten("operators", "arithmetic_operators", "test_lt", 0, "+") != "fehlerfrei"): raise AssertionError("lt arithmetic_operators: wrong result")
    if(ep.bewerten("operators", "arithmetic_operators", "test_lt", 1, "*") != "fehlerfrei"): raise AssertionError("lt arithmetic_operators2: wrong result")
    if(ep.bewerten("operators", "arithmetic_operators", "test_lt", 2, "23") != "fehlerfrei"): raise AssertionError("lt arithmetic_operators3: wrong result")
    if(ep.bewerten("operators", "operators_prefix", "test_lt", 0, "++a") != "fehlerfrei"): raise AssertionError("lt operators_prefix: wrong result")
    if(ep.bewerten("operators", "operators_postfix", "test_lt", 0, "a++") != "fehlerfrei"): raise AssertionError("lt operators_postfix: wrong result")
    if(ep.bewerten("operators", "comparison_operators", "test_lt", 0, "<") != "fehlerfrei"): raise AssertionError("lt comparison_operators: wrong result")
    if(ep.bewerten("operators", "logic_operators", "test_lt", 0, "||") != "fehlerfrei"): raise AssertionError("lt logic_operators: wrong result")
    if(ep.bewerten("operators", "logic_operators", "test_lt", 1, "&&") != "fehlerfrei"): raise AssertionError("lt logic_operators2: wrong result")
    if(ep.bewerten("operators", "bitwise_operators", "test_lt", 0, ">>>") != "fehlerfrei"): raise AssertionError("lt bitwise_operators: wrong result")
    if(ep.bewerten("operators", "assignment_operators", "test_lt", 0, "*=3") != "fehlerfrei"): raise AssertionError("lt assignment_operators: wrong result")
    if(ep.bewerten("operators", "assignment_operators", "test_lt", 1, "2") != "fehlerfrei"): raise AssertionError("lt assignment_operators2: wrong result")
    
    #lesson: statements
    if(ep.bewerten("statements", "expressions", "test_lt", 0, "2") != "fehlerfrei"): raise AssertionError("lt expressions: wrong result")
    if(ep.bewerten("statements", "statements", "test_lt", 0, "+=") != "fehlerfrei"): raise AssertionError("lt statements: wrong result")
    if(ep.bewerten("statements", "code_blocks", "test_lt", 0, "{") != "fehlerfrei"): raise AssertionError("lt code_blocks: wrong result")
    if(ep.bewerten("statements", "code_blocks", "test_lt", 1, "{ and }") != "fehlerfrei"): raise AssertionError("lt code_blocks2: wrong result")
    
    #lesson: controll_structures
    if(ep.bewerten("controll_structures", "boolean_expression", "test_lt", 0, "&&") != "fehlerfrei"): raise AssertionError("lt boolean_expression: wrong result")
    if(ep.bewerten("controll_structures", "if", "test_lt", 0, "if(!(x>0||x==0))") != "fehlerfrei"): raise AssertionError("lt if: wrong result")
    if(ep.bewerten("controll_structures", "if", "test_lt", 1, "if(p%2==0){}") != "fehlerfrei"): raise AssertionError("lt if2: wrong result")
    if(ep.bewerten("controll_structures", "switch", "test_lt", 0, "short") != "fehlerfrei"): raise AssertionError("lt switch: wrong result")
    if(ep.bewerten("controll_structures", "while", "test_lt", 0, "while(x<10)") != "fehlerfrei"): raise AssertionError("lt while: wrong result")
    if(ep.bewerten("controll_structures", "while", "test_lt", 1, "true") != "fehlerfrei"): raise AssertionError("lt while2: wrong result")
    if(ep.bewerten("controll_structures", "do_while", "test_lt", 0, "do") != "fehlerfrei"): raise AssertionError("lt do_while: wrong result")
    if(ep.bewerten("controll_structures", "do_while", "test_lt", 1, "do{++a;}") != "fehlerfrei"): raise AssertionError("lt do_while2: wrong result")
    if(ep.bewerten("controll_structures", "for", "test_lt", 0, "i<=10") != "fehlerfrei"): raise AssertionError("lt for: wrong result")
    if(ep.bewerten("controll_structures", "for", "test_lt", 1, "c=0;c<10;c++") != "fehlerfrei"): raise AssertionError("lt for2: wrong result")
    if(ep.bewerten("controll_structures", "extended_for", "test_lt", 0, ":") != "fehlerfrei"): raise AssertionError("lt extended_for: wrong result")
    if(ep.bewerten("controll_structures", "extended_for", "test_lt", 1, "short c={1,2,3};") != "fehlerfrei"): raise AssertionError("lt extended_for2: wrong result")
    if(ep.bewerten("controll_structures", "break", "test_lt", 0, "break") != "fehlerfrei"): raise AssertionError("lt break: wrong result")
    if(ep.bewerten("controll_structures", "continue", "test_lt", 0, "continue") != "fehlerfrei"): raise AssertionError("lt continue: wrong result")

    #lesson: methods
    if(ep.bewerten("methods", "method_definition", "test_lt", 0, "public void") != "fehlerfrei"): raise AssertionError("lt method_definition: wrong result")
    if(ep.bewerten("methods", "method_definition", "test_lt", 1, "public static int add") != "fehlerfrei"): raise AssertionError("lt method_definition2: wrong result")
    if(ep.bewerten("methods", "method_modifiers", "test_lt", 0, "static") != "fehlerfrei"): raise AssertionError("lt method_modifiers: wrong result")
    if(ep.bewerten("methods", "method_modifiers", "test_lt", 1, "public") != "fehlerfrei"): raise AssertionError("lt method_modifiers2: wrong result")
    if(ep.bewerten("methods", "method_access", "test_lt", 0, "Math.random()") != "fehlerfrei"): raise AssertionError("lt method_access: wrong result")
    if(ep.bewerten("methods", "method_access", "test_lt", 1, "print(addfive(3));") != "fehlerfrei"): raise AssertionError("lt method_access2: wrong result")

    #lesson: classes
    if(ep.bewerten("classes", "class_definition", "test_lt", 0, "A{ }") != "fehlerfrei"): raise AssertionError("lt class_definition: wrong result")
    if(ep.bewerten("classes", "class_definition", "test_lt", 1, "public B(){System.out.println(\"created!\");}") != "fehlerfrei"): raise AssertionError("lt class_definition2: wrong result")
    if(ep.bewerten("classes", "class_modifiers", "test_lt", 0, "abstract") != "fehlerfrei"): raise AssertionError("lt class_modifiers: wrong result")
    if(ep.bewerten("classes", "class_modifiers", "test_lt", 1, "final") != "fehlerfrei"): raise AssertionError("lt class_modifiers2: wrong result")
    if(ep.bewerten("classes", "access_modifiers", "test_lt", 0, "public") != "fehlerfrei"): raise AssertionError("lt access_modifiers: wrong result")
    if(ep.bewerten("classes", "access_modifiers", "test_lt", 1, "private class test{}") != "fehlerfrei"): raise AssertionError("lt access_modifiers2: wrong result")
    if(ep.bewerten("classes", "object_declaration", "test_lt", 0, "Word") != "fehlerfrei"): raise AssertionError("lt object_declaration: wrong result")
    if(ep.bewerten("classes", "class_fields", "test_lt", 0, "int value;") != "fehlerfrei"): raise AssertionError("lt class_fields: wrong result")
    if(ep.bewerten("classes", "class_fields", "test_lt", 1, "String name;") != "fehlerfrei"): raise AssertionError("lt class_fields2: wrong result")
    if(ep.bewerten("classes", "member_access_variables", "test_lt", 0, ".width") != "fehlerfrei"): raise AssertionError("lt member_access_variables: wrong result")
    if(ep.bewerten("classes", "member_access_methods", "test_lt", 0, "get_width()") != "fehlerfrei"): raise AssertionError("lt member_access_methods: wrong result")
    pass


  def testLTMCex(self):
    for l in ep.lessons:
      for k in ep.lessoninhalte[l]:
        for v in Syntaxkonzept(ep.lessoninhalte[l]).test_lt:
          print(ep.zugriffLehreinheit(l, k, "test_lt", v))
        for v in Syntaxkonzept(ep.lessoninhalte[l]).test_mc:
          print(ep.zugriffLehreinheit(l, k, "test_mc", v)) 
    pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()