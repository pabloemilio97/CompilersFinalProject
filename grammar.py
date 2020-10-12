#Pablo Andrade A01193740
#Andrés Aguirre A01039656

import ply.lex as lex
import ply.yacc as yacc

#pending: add string for declaration?
reserved = {
    'program': 'PROGRAM_RESERVED',
    'function': 'FUNCTION_RESERVED',
    'void': 'VOID_RESERVED',
    'let': 'LET_RESERVED',
    'int': 'INT_RESERVED',
    'float': 'FLOAT_RESERVED',
    'print': 'PRINT_RESERVED',
    'if': 'IF_RESERVED',
    'else': 'ELSE_RESERVED',
    'read': 'READ_RESERVED',
    'write': 'WRITE_RESERVED',
    'for': 'FOR_RESERVED',
    'while': 'WHILE_RESERVED',
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
t_DOUBLEEQUALS = r'=='
t_NOTEQUALS = r'!='

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value, 'ID')# Check for reserved words
  return t

start = 'PROGRAM'

def p_empty(p):
    'empty :'
    pass

def p_PROGRAM(p):
    'PROGRAM : program ID SEMICOLON VARS BODY MAIN'
    pass

def p_BODY(p):
    '''BODY : FUNCTION BODY
    | empty'''
    pass

def p_VARS(p):
    '''VARS : let TYPE COLON ID_LIST SEMICOLON VARS
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

def p_FUNCTION(p):
    'FUNCTION : FUNCTION_AUX function ID LPAREN PARAM RPAREN FUNCTION_BODY'
    pass

def p_FUNCTION_AUX(p):
    '''FUNCTION_AUX : TYPE
    | void'''
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
    | READ STATEMENTS
    | WRITE STATEMENTS
    | IF STATEMENTS
    | WHILE STATEMENTS
    | FOR STATEMENTS
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

def p_READ(p):
    'READ : read LPAREN VAR READ_AUX RPAREN SEMICOLON'
    pass

def p_READ_AUX(p):
    '''READ_AUX : COMMA VAR READ_AUX
    | empty'''
    pass

def p_WRITE(p):
    'WRITE : write LPAREN WRITE_AUX WRITE_AUX2 RPAREN SEMICOLON'
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
    'FUNCTION_RETURN : return EXPRESSION SEMICOLON'
    pass

def p_IF(p):
    'IF : if LPAREN EXPRESSION RPAREN LCURLY STATEMENTS RCURLY else LCURLY STATEMENTS RCURLY'
    pass

def p_WHILE(p):
    'WHILE : while LPAREN EXPRESSION RPAREN LCURLY STATEMENTS RCURLY'
    pass

def p_FOR(p):
    'FOR : for LPAREN VAR EQUALS EXPRESSION to EXPRESSION RPAREN LCURLY STATEMENTS RCURLY'
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
    'COMPARE_EXPRESSION : ARITHMETHIC_EXPRESSION COMPARE_EXPRESSION_AUX ARITMETHIC_EXPRESSION'
    pass

def p_COMPARE_EXPRESSION_AUX(p):
    'COMPARE_EXPRESSION_AUX : COMPARE_EXPRESSION_AUX2 ARITHMETHIC_EXPRESSION'
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
