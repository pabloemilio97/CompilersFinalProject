#Pablo Andrade A01193740
#Andrés Aguirre A01039656

import ply.lex as lex
import ply.yacc as yacc

#pending: add string for declaration?
reserved = {
    'program': 'PROGRAM',
    'function': 'FUNCTION',
    'void': 'VOID',
    'let': 'LET',
    'int': 'INT',
    'float': 'FLOAT',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE'
}

tokens = [
    'ID', 'AND', 'OR', 'COMMENT', 'COLON', 'SEMICOLON', 'LBRACKET', 'RBRACKET', 'LCURLY', 'RCURLY', 'EQUALS', 'GREATERTHAN', 'LESSTHAN', 'LPAREN', 'RPAREN', 'DOT', 'COMMA', 'CTESTRING',
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
t_COMMENT  = r'%%.*%%'

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value, 'ID')# Check for reserved words
  return t

start = 'PROG'

def p_empty(p):
    'empty :'
    pass

def p_PROG(p):
    'PROG : program ID SEMICOLON VARS BODY MAIN'
    pass

def p_BODY(p):
    'BODY : FUNCTION BODY | empty'
    pass

def p_VARS(p):
    'VARS : let TYPE COLON ID_LIST SEMICOLON VARS | empty'
    pass

def p_ID_LIST(p):
    'ID_LIST : ID ID_LIST_AUX | MULTIDIMENSIONAL ID_LIST_AUX'
    pass

def p_ID_LIST_AUX(p):
    'ID_LIST_AUX : COMMA ID_LIST | empty'
    pass 

def p_FUNCTION(p):
    'FUNCTION : FUNCTION_AUX function ID LPAREN PARAM RPAREN FUNCTION_BODY'
    pass

def p_FUNCTION_AUX(p):
    'FUNCTION_AUX : TYPE | void'
    pass

def p_MULTIDIMENSIONAL(p):
    'MULTIDIMENSIONAL : ID LBRACKET CTEI RBRACKET | id LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET'
    pass

def p_PARAM(p):
    'PARAM : TYPE ID PARAM_AUX | empty'
    pass

def p_PARAM_AUX(p):
    'PARAM_AUX : COMMA PARAM_AUX2 | empty'
    pass

def p_PARAM_AUX2(p):
    'PARAM_AUX2 : TYPE ID PARAM_AUX'
    pass

def p_FUNCTION_BODY(p):
    'FUNCTION_BODY : VARS LCURLY STATEMENTS FUNCTION_BODY_AUX RCURLY'
    pass

def p_FUNCTION_BODY_AUX(p):
    'FUNCTION_BODY_AUX : FUNCTION_RETURN | epsilon'
    pass


###From here down, we need to keep modifying

def p_TYPE(p):
    '''TYPE : INT
    | FLOAT'''
    pass

def p_STATEMENT(p):
    '''STATEMENT : ASSIGNMENT
    | CONDICION
    | ESCRITURA'''
    pass

def p_ASSIGNMENT(p):
    'ASSIGNMENT : ID EQUALS EXPRESSION COLON'
    pass

def p_EXPRESSION(p):
    'EXPRESSION : EXP E1'
    pass

def p_E1(p):
    '''E1 : E2 EXP
    | empty'''
    pass

def p_E2(p):
    '''E2 : LESSTHAN
    | GREATERTHAN
    | LESSTHAN GREATERTHAN'''

def p_EXP(p):
    'EXP : TERMINO EX1'
    pass

def p_EX1(p):
    '''EX1 : TERMINO EX2 EX1
    | empty'''
    pass

def p_EX2(p):
    '''EX2 : PLUS
    | MINUS
    '''

def p_TERMINO(p):
    'TERMINO : FACTOR T1'
    pass

def p_T1(p):
    '''T1 : FACTOR T2 T1
    | empty'''
    pass

def p_T2(p):
    '''T2 : MULTIPLY
    | DIVIDE'''

def p_FACTOR(p):
    '''FACTOR : LPAREN EXPRESSION RPAREN
    | F1 VARCTE'''
    pass

def p_F1(p):
    '''F1 : EX2
    | empty
    '''

def p_VARCTE(p):
    '''VARCTE : ID
    | CTEI
    | CTEF'''
    pass

def p_CONDICION(p):
    'CONDICION : IF LPAREN EXPRESSION RPAREN BODY C1 COLON'
    pass

def p_C1(p):
    '''C1 : ELSE BODY
    | empty'''
    pass

def p_ESCRITURA(p):
    'ESCRITURA : PRINT LPAREN ES1 ES2 RPAREN SEMICOLON'
    pass

def p_ES1(p):
    '''ES1 : CTESTRING
    | EXPRESSION DOT ES1
    | empty
    '''
    pass

def p_ES2(p):
    '''ES2 : CTESTRING
    | EXPRESSION
    '''
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
