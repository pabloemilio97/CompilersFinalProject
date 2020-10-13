#Pablo Andrade A01193740
#Andrés Aguirre A01039656

import ply.lex as lex
import ply.yacc as yacc

#pending: add string for declaration?
reserved = {
    'program': 'PROGRAM',
    'main': 'MAIN',
    'function': 'FUNCTION',
    'void': 'VOID',
    'let': 'LET',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'read': 'READ',
    'write': 'WRITE',
    'for': 'FOR',
    'while': 'WHILE',
    'return': 'RETURN',
    'to': 'TO',
}

tokens = [
    'ID', 'AND', 'OR', 'COMMENT', 'COLON', 'SEMICOLON', 'LBRACKET', 'RBRACKET', 'LCURLY', 'RCURLY', 'EQUALS', 'DOUBLEEQUALS', 'NOTEQUALS', 'GREATERTHAN', 'LESSTHAN', 'LPAREN', 'RPAREN', 'DOT', 'COMMA', 'CTESTRING',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'CTEI', 'CTEF',
] + list(reserved.values())

t_COLON      = r':'
t_SEMICOLON  = r';'
t_LCURLY    = r'{'
t_RCURLY    = r'}'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_DOUBLEEQUALS = r'=='
t_NOTEQUALS = r'!='
t_EQUALS    = r'='
t_GREATERTHAN  = r'>'
t_LESSTHAN     = r'<'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_DOT       = r'\.'
t_COMMA     = r'\,'
t_CTESTRING = r'".*"'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_MULTIPLY  = r'\*'
t_DIVIDE    = r'/'
t_CTEI      = r'[1-9][0-9]*'
t_CTEF      = r'[1-9][0-9]*\.[0-9]'
t_AND       = r'\&'
t_OR       = r'\|'
t_ignore_COMMENT = r'%%.*%%'

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value, 'ID')# Check for reserved words
  return t

start = 'PROGRAM_RULE'

def p_empty(p):
    'empty :'
    pass

def p_PROGRAM_RULE(p):
    'PROGRAM_RULE : PROGRAM ID SEMICOLON VARS BODY MAIN'
    pass

def p_MAIN_RULE(p):
    'MAIN_RULE : MAIN LPAREN RPAREN LCURLY STATEMENTS RCURLY'
    pass

def p_BODY(p):
    '''BODY : FUNCTION_RULE BODY
    | empty'''
    pass

def p_TYPE(p):
    '''TYPE : INT
    | FLOAT
    | CHAR'''
    pass

def p_VARS(p):
    '''VARS : LET TYPE COLON ID_LIST SEMICOLON VARS
    | empty'''
    pass

def p_ID_LIST(p):
    '''ID_LIST : ID ID_LIST_AUX
    | MULTIDIMENSIONAL ID_LIST_AUX'''
    pass

def p_ID_LIST_AUX(p):
    '''ID_LIST_AUX : COMMA ID_LIST
    | empty'''
    pass 

def p_FUNCTION_RULE(p):
    'FUNCTION_RULE : FUNCTION_AUX FUNCTION ID LPAREN PARAM RPAREN FUNCTION_BODY'
    pass

def p_FUNCTION_AUX(p):
    '''FUNCTION_AUX : TYPE
    | VOID'''
    pass

def p_MULTIDIMENSIONAL(p):
    '''MULTIDIMENSIONAL : ID LBRACKET CTEI RBRACKET
    | ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET'''
    pass

def p_PARAM(p):
    '''PARAM : TYPE ID PARAM_AUX
    | empty'''
    pass

def p_PARAM_AUX(p):
    '''PARAM_AUX : COMMA PARAM_AUX2
    | empty'''
    pass

def p_PARAM_AUX2(p):
    'PARAM_AUX2 : TYPE ID PARAM_AUX'
    pass

def p_FUNCTION_BODY(p):
    'FUNCTION_BODY : VARS LCURLY STATEMENTS FUNCTION_BODY_AUX RCURLY'
    pass

def p_FUNCTION_BODY_AUX(p):
    '''FUNCTION_BODY_AUX : FUNCTION_RETURN
    | empty'''
    pass

def p_STATEMENTS(p):
    '''STATEMENTS : STATEMENTS_AUX
    | empty'''
    pass

def p_STATEMENTS_AUX(p):
    '''STATEMENTS_AUX : ASSIGNMENT STATEMENTS
    | FUNCTION_CALL STATEMENTS
    | READ_RULE STATEMENTS
    | WRITE STATEMENTS
    | IF_RULE STATEMENTS
    | WHILE_RULE STATEMENTS
    | FOR_RULE STATEMENTS
    '''
    pass

def p_ASSIGNMENT(p):
    'ASSIGNMENT : VAR EQUALS EXPRESSION SEMICOLON'
    pass

def p_FUNCTION_CALL(p):
    'FUNCTION_CALL : ID LPAREN EXPRESSION FUNCTION_CALL_AUX RPAREN SEMICOLON'
    pass

def p_FUNCTION_CALL_AUX(p):
    '''FUNCTION_CALL_AUX : COMMA EXPRESSION FUNCTION_CALL_AUX
    | empty'''
    pass

def p_READ_RULE(p):
    'READ_RULE : READ LPAREN VAR READ_AUX RPAREN SEMICOLON'
    pass

def p_READ_AUX(p):
    '''READ_AUX : COMMA VAR READ_AUX
    | empty'''
    pass

def p_WRITE_RULE(p):
    'WRITE_RULE : WRITE LPAREN WRITE_AUX WRITE_AUX2 RPAREN SEMICOLON'
    pass

def p_WRITE_AUX(p):
    '''WRITE_AUX : CTESTRING
    | EXPRESSION'''
    pass

def p_WRITE_AUX2(p):
    '''WRITE_AUX2 : COMMA WRITE_AUX WRITE_AUX2 
    | empty'''
    pass

def p_VAR(p):
    '''VAR : ID
    | ID LBRACKET EXPRESSION RBRACKET
    | ID LBRACKET EXPRESSION RBRACKET LBRACKET EXPRESSION RBRACKET'''
    pass

def p_FUNCTION_RETURN(p):
    'FUNCTION_RETURN : RETURN EXPRESSION SEMICOLON'
    pass

def p_IF_RULE(p):
    'IF_RULE : IF LPAREN EXPRESSION RPAREN LCURLY STATEMENTS RCURLY ELSE LCURLY STATEMENTS RCURLY'
    pass

def p_WHILE_RULE(p):
    'WHILE_RULE : WHILE LPAREN EXPRESSION RPAREN LCURLY STATEMENTS RCURLY'
    pass

def p_FOR_RULE(p):
    'FOR_RULE : FOR LPAREN VAR EQUALS EXPRESSION TO EXPRESSION RPAREN LCURLY STATEMENTS RCURLY'
    pass

def p_EXPRESSION(p):
    'EXPRESSION : AND_EXPRESSION EXPRESSION_AUX'
    pass

def p_EXPRESSION_AUX(p):
    '''EXPRESSION_AUX : OR EXPRESSION
    | empty'''
    pass

def p_AND_EXPRESSION(p):
    'AND_EXPRESSION : COMPARE_EXPRESSION AND_EXPRESSION_AUX'
    pass

def p_AND_EXPRESSION_AUX(p):
    '''AND_EXPRESSION_AUX : AND AND_EXPRESSION
    | empty'''
    pass

def p_COMPARE_EXPRESSION(p):
    'COMPARE_EXPRESSION : ARITHMETIC_EXPRESSION COMPARE_EXPRESSION_AUX ARITHMETIC_EXPRESSION'
    pass

def p_COMPARE_EXPRESSION_AUX(p):
    'COMPARE_EXPRESSION_AUX : COMPARE_EXPRESSION_AUX2 ARITHMETIC_EXPRESSION'
    pass

def p_COMPARE_EXPRESSION_AUX2(p):
    '''COMPARE_EXPRESSION_AUX2 : LESSTHAN
    | GREATERTHAN
    | DOUBLEEQUALS
    | NOTEQUALS'''
    pass

def p_ARITHMETIC_EXPRESSION(p):
    'ARITHMETIC_EXPRESSION : TERM ARITHMETIC_EXPRESSION_AUX'
    pass

def p_ARITHMETIC_EXPRESSION_AUX(p):
    '''ARITHMETIC_EXPRESSION_AUX : ARITHMETIC_EXPRESSION_AUX2 ARITHMETIC_EXPRESSION
    | empty'''
    pass

def p_ARITHMETIC_EXPRESSION_AUX2(p):
    '''ARITHMETIC_EXPRESSION_AUX2 : PLUS
    | MINUS'''
    pass

def p_TERM(p):
    'TERM : FACTOR TERM_AUX'
    pass

def p_TERM_AUX(p):
    '''TERM_AUX : TERM_AUX2 TERM
    | empty'''
    pass

def p_TERM_AUX2(p):
    '''TERM_AUX2 : MULTIPLY
    | DIVIDE'''
    pass

def p_FACTOR(p):
    '''FACTOR : LPAREN EXPRESSION RPAREN
    | CTEI
    | CTESTRING
    | CTEF
    | VAR
    | FUNCTION_CALL'''
    pass

def p_error(p):
    print("Apropiado")

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

parser = yacc.yacc()


aux = int(input("1.Valido\n2.No valido\n3.Probar de documento 'test.txt'\n"))

data = ""

if (aux == 1):
    data = '''program myprogram;{
    }'''

elif (aux == 2):
    data = '''prog 1'''

elif (aux == 3):
    f = open("test.txt", "r")
    if f.mode == 'r':
        data = f.read()
    else:
        print("File is invalid")

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
parser.parse(data)
