#Pablo Andrade A01193740
#Andrés Aguirre A01039656

import ply.lex as lex
import ply.yacc as yacc
import quad_generator
import shared
import symbol_table

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
    'ID', 'AND', 'OR', 'COMMENT', 'SEMICOLON', 'LBRACKET', 'RBRACKET', 'LCURLY', 'RCURLY', 'EQUALS', 'DOUBLEEQUALS', 'NOTEQUALS', 'GREATERTHAN', 'LESSTHAN', 'LPAREN', 'RPAREN', 'COMMA', 'CTECHAR',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'CTEI', 'CTEF',
] + list(reserved.values())

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
t_COMMA     = r'\,'
t_CTECHAR = r'"[a-zA-Z0-9]"'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_MULTIPLY  = r'\*'
t_DIVIDE    = r'/'
t_CTEI      = r'[0-9]+'
t_CTEF      = r'[0-9]+\.[0-9]*'
t_AND       = r'\&'
t_OR       = r'\|'


def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value, 'ID')# Check for reserved words
  return t

start = 'PROGRAM_RULE'

def p_empty(p):
    'empty :'

def p_PROGRAM_RULE(p):
    'PROGRAM_RULE : PROGRAM_RULE_AUX ID SEMICOLON VARS BODY MAIN_RULE'

def p_PROGRAM_RULE_AUX(p):
    'PROGRAM_RULE_AUX : PROGRAM'
    symbol_table.insert_function('global')

def p_MAIN_RULE(p):
    'MAIN_RULE : MAIN LPAREN RPAREN LCURLY STATEMENTS RCURLY'

def p_BODY(p):
    '''BODY : FUNCTION_RULE BODY
    | empty'''

def p_TYPE(p):
    '''TYPE : INT
    | FLOAT
    | CHAR'''
    type = p[1]
    p[0] = type

def p_VARS(p):
    '''VARS : LET TYPE ID_LIST SEMICOLON VARS
    | empty'''
    if len(p) == 6: # if it's declaring a variable
        var_name = p[3]
        var_type = p[2]
        print(shared.context, var_name, var_type)


def p_ID_LIST(p):
    '''ID_LIST : ID ID_LIST_AUX
    | MULTIDIMENSIONAL ID_LIST_AUX'''
    var_name = p[1]
    if len(p) == 3: # if it's declaring a variable pass it to VARS
        p[0] = var_name

def p_ID_LIST_AUX(p):
    '''ID_LIST_AUX : COMMA ID_LIST
    | empty'''
     

def p_FUNCTION_RULE(p):
    'FUNCTION_RULE : FUNCTION_AUX FUNCTION ID LPAREN PARAM RPAREN FUNCTION_BODY'
    func_name = p[3]
    shared.context = func_name
    print(shared.context)
    symbol_table.insert_function(func_name)

def p_FUNCTION_AUX(p):
    '''FUNCTION_AUX : TYPE
    | VOID'''
    func_type = p[1]
    symbol_table.func_map[shared.context]['type'] = func_type
    

def p_MULTIDIMENSIONAL(p):
    '''MULTIDIMENSIONAL : ID LBRACKET CTEI RBRACKET
    | ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET'''
    

def p_PARAM(p):
    '''PARAM : TYPE ID PARAM_AUX
    | empty'''
    

def p_PARAM_AUX(p):
    '''PARAM_AUX : COMMA PARAM_AUX2
    | empty'''
    

def p_PARAM_AUX2(p):
    'PARAM_AUX2 : TYPE ID PARAM_AUX'
    

def p_FUNCTION_BODY(p):
    'FUNCTION_BODY : VARS LCURLY STATEMENTS FUNCTION_BODY_AUX RCURLY'
    

def p_FUNCTION_BODY_AUX(p):
    '''FUNCTION_BODY_AUX : FUNCTION_RETURN
    | empty'''
    

def p_STATEMENTS(p):
    '''STATEMENTS : STATEMENTS_AUX STATEMENTS
    | empty'''
    

def p_STATEMENTS_AUX(p):
    '''STATEMENTS_AUX : STATEMENTS_AUX2 SEMICOLON
    | STATEMENTS_AUX3'''

def p_STATEMENTS_AUX2(p):
    '''STATEMENTS_AUX2 : ASSIGNMENT
    | FUNCTION_CALL
    | READ_RULE
    | WRITE_RULE
    '''

def p_STATEMENTS_AUX3(p):
    '''STATEMENTS_AUX3 : IF_RULE
    | WHILE_RULE
    | FOR_RULE
    '''

def p_ASSIGNMENT(p):
    'ASSIGNMENT : VAR EQUALS EXPRESSION'
    

def p_FUNCTION_CALL(p):
    'FUNCTION_CALL : ID LPAREN FUNCTION_CALL_AUX RPAREN'


def p_FUNCTION_CALL_AUX(p):
    '''FUNCTION_CALL_AUX : EXPRESSION FUNCTION_CALL_AUX2
    | empty'''
    

def p_FUNCTION_CALL_AUX2(p):
    '''FUNCTION_CALL_AUX2 : COMMA EXPRESSION FUNCTION_CALL_AUX2
    | empty'''
    

def p_READ_RULE(p):
    'READ_RULE : READ LPAREN VAR READ_AUX RPAREN'
    

def p_READ_AUX(p):
    '''READ_AUX : COMMA VAR READ_AUX
    | empty'''
    

def p_WRITE_RULE(p):
    'WRITE_RULE : WRITE LPAREN EXPRESSION WRITE_AUX RPAREN'
    

def p_WRITE_AUX(p):
    '''WRITE_AUX : COMMA EXPRESSION WRITE_AUX 
    | empty'''
    

def p_VAR(p):
    '''VAR : ID
    | ID LBRACKET EXPRESSION RBRACKET
    | ID LBRACKET EXPRESSION RBRACKET LBRACKET EXPRESSION RBRACKET'''
    

def p_FUNCTION_RETURN(p):
    'FUNCTION_RETURN : RETURN EXPRESSION SEMICOLON'
    

def p_IF_RULE(p):
    'IF_RULE : IF LPAREN EXPRESSION RPAREN LCURLY STATEMENTS RCURLY IF_AUX'

def p_IF_AUX(p):
    '''IF_AUX : ELSE LCURLY STATEMENTS RCURLY
    | empty'''

def p_WHILE_RULE(p):
    'WHILE_RULE : WHILE LPAREN EXPRESSION RPAREN LCURLY STATEMENTS RCURLY'
    

def p_FOR_RULE(p):
    'FOR_RULE : FOR LPAREN VAR EQUALS EXPRESSION TO EXPRESSION RPAREN LCURLY STATEMENTS RCURLY'
    

def p_EXPRESSION(p):
    'EXPRESSION : AND_EXPRESSION EXPRESSION_AUX'
    

def p_EXPRESSION_AUX(p):
    '''EXPRESSION_AUX : OR EXPRESSION
    | empty'''
    

def p_AND_EXPRESSION(p):
    'AND_EXPRESSION : COMPARE_EXPRESSION AND_EXPRESSION_AUX'
    

def p_AND_EXPRESSION_AUX(p):
    '''AND_EXPRESSION_AUX : AND AND_EXPRESSION
    | empty'''
    

def p_COMPARE_EXPRESSION(p):
    'COMPARE_EXPRESSION : ARITHMETIC_EXPRESSION COMPARE_EXPRESSION_AUX'
    

def p_COMPARE_EXPRESSION_AUX(p):
    '''COMPARE_EXPRESSION_AUX : COMPARE_EXPRESSION_AUX2 ARITHMETIC_EXPRESSION
    | empty'''
    

def p_COMPARE_EXPRESSION_AUX2(p):
    '''COMPARE_EXPRESSION_AUX2 : LESSTHAN
    | GREATERTHAN
    | DOUBLEEQUALS
    | NOTEQUALS'''
    

def p_ARITHMETIC_EXPRESSION(p):
    'ARITHMETIC_EXPRESSION : TERM ARITHMETIC_EXPRESSION_AUX'
    

def p_ARITHMETIC_EXPRESSION_AUX(p):
    '''ARITHMETIC_EXPRESSION_AUX : ARITHMETIC_EXPRESSION_AUX2 ARITHMETIC_EXPRESSION
    | empty'''
    

def p_ARITHMETIC_EXPRESSION_AUX2(p):
    '''ARITHMETIC_EXPRESSION_AUX2 : PLUS
    | MINUS'''
    

def p_TERM(p):
    'TERM : FACTOR TERM_AUX'
    

def p_TERM_AUX(p):
    '''TERM_AUX : TERM_AUX2 TERM
    | empty'''
    

def p_TERM_AUX2(p):
    '''TERM_AUX2 : MULTIPLY
    | DIVIDE'''
    

def p_FACTOR(p):
    '''FACTOR : LPAREN EXPRESSION RPAREN
    | CTEI
    | CTECHAR
    | CTEF
    | VAR
    | FUNCTION_CALL'''
    

def p_error(p):
    print('Syntax error!', p)

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
    f = open("testQuad.txt", "r")
    if f.mode == 'r':
        data = f.read()
    else:
        print("File is invalid")

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break

# use debug=True for debugging
parser.parse(data)


# symbol_table.print_func_map()