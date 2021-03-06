# Pablo Andrade A01193740
# Andrés Aguirre A01039656

import ply.lex as lex
import ply.yacc as yacc
import quad_generator
import shared
import symbol_table
import error
import quad_generator
import pprint
import semantic_cube
import vm
import shared_vm
import os
import sys

if len(sys.argv) == 2:
    if sys.argv[1] == 'local':
        shared.env = sys.argv[1]

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
    'PLUS', 'MINUS', 'MULTIPLY', 'FLOORDIVIDE', 'DIVIDE', 'CTEI', 'CTEF', 'GREATERTHANOREQUAL', 'LESSTHANOREQUAL',
] + list(reserved.values())

t_SEMICOLON = r';'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_DOUBLEEQUALS = r'=='
t_NOTEQUALS = r'!='
t_EQUALS = r'='
t_GREATERTHAN = r'>'
t_GREATERTHANOREQUAL = r'>='
t_LESSTHAN = r'<'
t_LESSTHANOREQUAL = r'<='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r'\,'
t_CTECHAR = r'"[a-zA-Z0-9]?"'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_FLOORDIVIDE = r'/.'
t_DIVIDE = r'/'
t_CTEI = r'[0-9]+'
t_CTEF = r'[0-9]+\.[0-9]*'
t_AND = r'\&'
t_OR = r'\|'


def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


start = 'PROGRAM_RULE'


def p_empty(p):
    'empty :'


def p_PROGRAM_RULE(p):
    'PROGRAM_RULE : PROGRAM_RULE_AUX ID SEMICOLON VARS BODY MAIN_RULE'


def p_PROGRAM_RULE_AUX(p):
    'PROGRAM_RULE_AUX : PROGRAM'
    symbol_table.insert_function('global')
    shared.jump_stack.append('0')
    # this one will contain the main register to know where to start
    quad_generator.gen_quad('goto', 'main', '', '')


def p_MAIN_RULE(p):
    'MAIN_RULE : MAIN_AUX LPAREN RPAREN LCURLY STATEMENTS RCURLY'


def p_MAIN_AUX(p):
    'MAIN_AUX : MAIN'
    main_pos = int(shared.jump_stack.pop())
    quad_generator.update_quadruples(main_pos)
    function_name = p[1]  # function name is main here
    # Inserting function into symbol table
    symbol_table.insert_function(function_name)
    shared.scope = function_name


def p_BODY(p):
    '''BODY : BODY_AUX BODY
    | empty'''


def p_BODY_AUX(p):
    '''BODY_AUX : FUNCTION_RULE
    | PROCEDURE'''


def p_PROCEDURE(p):
    'PROCEDURE : VOID FUNCTION FUNCTION_ID_AUX  LPAREN PARAM RPAREN PROCEDURE_BODY'


def p_PROCEDURE_BODY(p):
    '''PROCEDURE_BODY : VARS LCURLY STATEMENTS RCURLY'''
    quad_generator.gen_endfunc_quadruple()


def p_FUNCTION_RULE(p):
    'FUNCTION_RULE : FUNCTION_SIGNATURE_AUX FUNCTION_BODY'


def p_FUNCTION_SIGNATURE_AUX(p):
    'FUNCTION_SIGNATURE_AUX : TYPE FUNCTION FUNCTION_ID_AUX LPAREN PARAM RPAREN'
    func_type = p[1]
    symbol_table.func_map[shared.scope]['type'] = func_type


def p_PARAM(p):
    '''PARAM : PARAM_TYPE_ID_AUX PARAM_AUX
    | empty'''
    symbol_table.insert_quadruple_reg(shared.scope, quad_generator.quad_pos())


def p_PARAM_TYPE_ID_AUX(p):
    'PARAM_TYPE_ID_AUX : TYPE ID'
    param_type = p[1]
    param_name = p[2]
    if param_name in symbol_table.func_map['global']['vars']:
        error.gen_err(f'param name already declared globally "{param_name}"')
    symbol_table.insert_param(shared.scope, param_name, param_type)


def p_PARAM_AUX(p):
    '''PARAM_AUX : COMMA PARAM_AUX2
    | empty'''


def p_PARAM_AUX2(p):
    'PARAM_AUX2 : PARAM_TYPE_ID_AUX PARAM_AUX'


def p_FUNCTION_ID_AUX(p):
    'FUNCTION_ID_AUX : ID'
    function_name = p[1]
    # Inserting function into symbol table
    symbol_table.insert_function(function_name)
    shared.scope = function_name


def p_FUNCTION_BODY(p):
    '''FUNCTION_BODY : VARS LCURLY STATEMENTS FUNCTION_BODY_AUX RCURLY'''
    quad_generator.gen_endfunc_quadruple()


def p_FUNCTION_BODY_AUX(p):
    '''FUNCTION_BODY_AUX : FUNCTION_RETURN'''


def p_TYPE(p):
    '''TYPE : INT
    | FLOAT
    | CHAR'''
    type = p[1]
    p[0] = type


def p_VARS(p):
    '''VARS : LET TYPE_DECLARATION_AUX ID_LIST SEMICOLON VARS
    | empty'''


def p_TYPE_DECLARATION_AUX(p):
    'TYPE_DECLARATION_AUX : TYPE'
    shared.current_declaration_type = p[1]


def p_ID_LIST(p):
    '''ID_LIST : ID_AUX ID_LIST_AUX
    | MULTIDIMENSIONAL ID_LIST_AUX'''


def p_ID_AUX(p):
    '''ID_AUX : ID'''
    var_name = p[1]
    symbol_table.insert_var(shared.scope, var_name,
                            shared.current_declaration_type)


def p_ID_LIST_AUX(p):
    '''ID_LIST_AUX : COMMA ID_LIST
    | empty'''


def p_MULTIDIMENSIONAL(p):
    '''MULTIDIMENSIONAL : ARRAY
    | MATRIX'''


def p_ARRAY(p):
    '''ARRAY : ID LBRACKET CTEI_AUX RBRACKET'''
    name = p[1]
    dimension = p[3]
    symbol_table.insert_var(
        shared.scope, name, shared.current_declaration_type, [dimension])


def p_MATRIX(p):
    '''MATRIX : ID LBRACKET CTEI_AUX RBRACKET LBRACKET CTEI_AUX RBRACKET'''
    name = p[1]
    dimension_1 = p[3]
    dimension_2 = p[6]
    symbol_table.insert_var(shared.scope, name, shared.current_declaration_type, [
                            dimension_1, dimension_2])


def p_CTEI_AUX(p):
    '''CTEI_AUX : CTEI'''
    constant = p[1]
    symbol_table.insert_constant(constant)
    p[0] = constant


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
    'ASSIGNMENT : VAR_ASSIGNMENT EQUALS EXPRESSION'
    assign_to = shared.assign_to
    expression = p[3]
    quad_generator.gen_assign_quadruples(expression, assign_to)


def p_FUNCTION_CALL(p):
    'FUNCTION_CALL : FUNCTION_CALL_ID_AUX LPAREN FUNCTION_CALL_AUX RPAREN'
    function_name = p[1]
    quad_generator.gen_quad('GOSUB', '', '', function_name)
    p[0] = function_name
    shared.expression_stack.pop()
    shared.param_nums_stack.pop()
    shared.function_call_names_stack.pop()


def p_FUNCTION_CALL_ID_AUX(p):
    'FUNCTION_CALL_ID_AUX : ID'
    function_name = p[1]
    shared.expression_stack.append([])
    shared.param_nums_stack.append(1)
    shared.function_call_names_stack.append(function_name)
    if function_name not in symbol_table.func_map:
        error.gen_err(
            f'Trying to call function that does not exist "{function_name}"')
    else:
        # quadruple ERA with func name, this symbol table should contain the memory needed for the func
        quad_generator.gen_quad('ERA', '', '', function_name)
    # pass the func name to previous rule
    p[0] = function_name


def p_FUNCTION_CALL_AUX(p):
    '''FUNCTION_CALL_AUX : PARAM_EXPRESSION FUNCTION_CALL_AUX2
    | empty'''
    shared.param_nums_stack[-1] = 1


def p_PARAM_EXPRESSION(p):
    'PARAM_EXPRESSION : EXPRESSION'
    expression = p[1]
    quad_generator.gen_param_quadruples(expression)


def p_FUNCTION_CALL_AUX2(p):
    '''FUNCTION_CALL_AUX2 : COMMA PARAM_EXPRESSION FUNCTION_CALL_AUX2
    | empty'''


def p_READ_RULE(p):
    'READ_RULE : READ LPAREN VAR_ASSIGNMENT READ_AUX RPAREN'


def p_READ_AUX(p):
    '''READ_AUX : COMMA VAR_ASSIGNMENT READ_AUX
    | empty'''


def p_WRITE_RULE(p):
    'WRITE_RULE : WRITE LPAREN WRITE_EXPRESSION_AUX WRITE_AUX RPAREN'


def p_WRITE_AUX(p):
    '''WRITE_AUX : COMMA WRITE_EXPRESSION_AUX WRITE_AUX 
    | empty'''


def p_WRITE_EXPRESSION_AUX(p):
    'WRITE_EXPRESSION_AUX : EXPRESSION'
    expression = p[1]
    quad_generator.gen_write_quadruples(expression)


def p_VAR_ASSIGNMENT(p):
    '''VAR_ASSIGNMENT : ID_ASSIGNMENT
    | ARRAY_ASSIGNMENT
    | MATRIX_ASSIGNMENT'''


def p_ID_ASSIGNMENT(p):
    'ID_ASSIGNMENT : ID'
    shared.assign_to = ''
    var_name = p[1]
    if var_name not in symbol_table.func_map[shared.scope]['vars'] and var_name not in symbol_table.func_map['global']['vars']:
        error.gen_err(f'Trying to assign value to variable "{var_name}" that does not exist')
    shared.assign_to = var_name


def p_ARRAY_ASSIGNMENT(p):
    'ARRAY_ASSIGNMENT : ARRAY_ACCESS'
    pointer = p[1]
    shared.assign_to = pointer


def p_MATRIX_ASSIGNMENT(p):
    'MATRIX_ASSIGNMENT : MATRIX_ACCESS'
    pointer = p[1]
    shared.assign_to = pointer


def p_FUNCTION_RETURN(p):
    'FUNCTION_RETURN : RETURN EXPRESSION SEMICOLON'
    expression = p[2]
    quad_generator.gen_return_quadruples(expression)


def p_IF_RULE(p):
    'IF_RULE : IF LPAREN EXPRESSION_AUX_IF RPAREN LCURLY STATEMENTS RCURLY IF_AUX'


def p_EXPRESSION_AUX_IF(p):
    'EXPRESSION_AUX_IF : EXPRESSION'
    expression = p[1]
    quad_generator.gen_if_quadruples(expression)


def p_IF_AUX(p):
    '''IF_AUX : ELSE_AUX LCURLY STATEMENTS RCURLY_AUX_ELSE
    | empty'''
    if len(p) < 5:
        quad_generator.gen_endif_quadruples()


def p_ELSE_AUX(p):
    'ELSE_AUX : ELSE'
    quad_generator.gen_else_quadruples()


def p_RCURLY_AUX_ELSE(p):
    'RCURLY_AUX_ELSE : RCURLY'
    quad_generator.gen_endelse_quadruples()


def p_WHILE_RULE(p):
    'WHILE_RULE : WHILE_WORD_AUX LPAREN WHILE_EXPRESSION_AUX RPAREN LCURLY STATEMENTS RCURLY_WHILE_AUX'


def p_WHILE_WORD_AUX(p):
    'WHILE_WORD_AUX : WHILE'
    shared.jump_stack.append(quad_generator.quad_pos())


def p_WHILE_EXPRESSION_AUX(p):
    'WHILE_EXPRESSION_AUX : EXPRESSION'
    expression = p[1]
    quad_generator.gen_while_quadruples(expression)


def p_RCURLY_WHILE_AUX(p):
    'RCURLY_WHILE_AUX : RCURLY'
    quad_generator.gen_endwhile_quadruples()


def p_FOR_RULE(p):
    'FOR_RULE : FOR LPAREN ASSIGNMENT TO_WORD_AUX END_FOR_AUX'


def p_END_FOR_AUX(p):
    'END_FOR_AUX : FOR_EXPRESSION_AUX RPAREN LCURLY STATEMENTS RCURLY'
    """
    This works because all rules present are executed before the following code.
    Since the last rule that will be executed is RCURLY, it is OK to generate the
    quadruples belonging to the end of the for loop.
    """
    variable = p[1]
    quad_generator.gen_endfor_quadruples(variable)


def p_FOR_EXPRESSION_AUX(p):
    'FOR_EXPRESSION_AUX : EXPRESSION'
    # The last quadruple that has been generated is the assignment
    variable = shared.quadruples[-1][-1]
    expression = p[1]
    quad_generator.gen_for_quadruples(variable, expression)
    # To know which variable corresponds to the for loop scope
    p[0] = variable


def p_TO_WORD_AUX(p):
    'TO_WORD_AUX : TO'
    shared.jump_stack.append(quad_generator.quad_pos())


def p_EXPRESSION(p):
    'EXPRESSION : OR_EXPRESSION EXPRESSION_AUX'
    value = shared.expression_stack[-1]
    p[0] = value[:]
    shared.expression_stack[-1].clear()

def p_EXPRESSION_NO_CLEAR(p):
    'EXPRESSION_NO_CLEAR : OR_EXPRESSION EXPRESSION_AUX'
    value = shared.expression_stack[-1]
    p[0] = value[:]

def p_EXPRESSION_AUX(p):
    '''EXPRESSION_AUX : EXPRESSION
    | empty'''

def p_OR_EXPRESSION(p):
    'OR_EXPRESSION : AND_EXPRESSION OR_EXPRESSION_AUX'

def p_OR_EXPRESSION_AUX(p):
    '''OR_EXPRESSION_AUX : OR_EXPRESSION_AUX2 OR_EXPRESSION
    | empty'''

def p_OR_EXPRESSION_AUX2(p):
    'OR_EXPRESSION_AUX2 : OR'
    operation = p[1]
    shared.expression_stack[-1].append(operation)

def p_AND_EXPRESSION(p):
    'AND_EXPRESSION : COMPARE_EXPRESSION AND_EXPRESSION_AUX'


def p_AND_EXPRESSION_AUX(p):
    '''AND_EXPRESSION_AUX : AND_EXPRESSION_AUX2 AND_EXPRESSION
    | empty'''

def p_AND_EXPRESSION_AUX2(p):
    'AND_EXPRESSION_AUX2 : AND'
    operation = p[1]
    shared.expression_stack[-1].append(operation)


def p_COMPARE_EXPRESSION(p):
    'COMPARE_EXPRESSION : ARITHMETIC_EXPRESSION COMPARE_EXPRESSION_AUX'


def p_COMPARE_EXPRESSION_AUX(p):
    '''COMPARE_EXPRESSION_AUX : COMPARE_EXPRESSION_AUX2 ARITHMETIC_EXPRESSION
    | empty'''


def p_COMPARE_EXPRESSION_AUX2(p):
    '''COMPARE_EXPRESSION_AUX2 : LESSTHAN
    | GREATERTHAN
    | DOUBLEEQUALS
    | NOTEQUALS
    | LESSTHANOREQUAL
    | GREATERTHANOREQUAL'''
    operation = p[1]
    shared.expression_stack[-1].append(operation)


def p_ARITHMETIC_EXPRESSION(p):
    'ARITHMETIC_EXPRESSION : TERM ARITHMETIC_EXPRESSION_AUX'


def p_ARITHMETIC_EXPRESSION_AUX(p):
    '''ARITHMETIC_EXPRESSION_AUX : ARITHMETIC_EXPRESSION_AUX2 ARITHMETIC_EXPRESSION
    | empty'''


def p_ARITHMETIC_EXPRESSION_AUX2(p):
    '''ARITHMETIC_EXPRESSION_AUX2 : PLUS
    | MINUS'''
    operation = p[1]
    shared.expression_stack[-1].append(operation)


def p_TERM(p):
    'TERM : FACTOR TERM_AUX'


def p_TERM_AUX(p):
    '''TERM_AUX : TERM_AUX2 TERM
    | empty'''


def p_TERM_AUX2(p):
    '''TERM_AUX2 : MULTIPLY
    | FLOORDIVIDE
    | DIVIDE'''
    operation = p[1]
    shared.expression_stack[-1].append(operation)


def p_FACTOR(p):
    '''FACTOR : LPAREN_AUX EXPRESSION_NO_CLEAR RPAREN_AUX
    | FACTOR_CONSTANTS
    | VAR_ACCESS
    | ARRAY_ACCESS
    | MATRIX_ACCESS
    | FUNCTION_CALL_EXPRESSION'''
    if len(p) != 4:
        factor = p[1]
        shared.expression_stack[-1].append(factor)


def p_FACTOR_CONSTANTS(p):
    '''FACTOR_CONSTANTS : CTEI
    | CTECHAR
    | CTEF'''
    constant = p[1]
    symbol_table.insert_constant(constant)
    p[0] = constant


def p_FUNCTION_CALL_EXPRESSION(p):
    '''FUNCTION_CALL_EXPRESSION : FUNCTION_CALL'''
    function_name = p[1]
    if symbol_table.func_map[function_name]["type"] == "void":
        error.gen_err(f"Function {function_name} does not have a return value")
    new_tmp = quad_generator.gen_function_call_quads(function_name)
    p[0] = new_tmp


def p_LPAREN_AUX(p):
    'LPAREN_AUX : LPAREN'
    shared.expression_stack[-1].append(p[1])


def p_RPAREN_AUX(p):
    'RPAREN_AUX : RPAREN'
    shared.expression_stack[-1].append(p[1])


def p_VAR_ACCESS(p):
    'VAR_ACCESS : ID'
    current_func_map_vars = symbol_table.func_map[shared.scope]['vars']
    var_name = p[1]
    if var_name not in current_func_map_vars and var_name not in symbol_table.func_map[shared.scope]['params'] and var_name not in symbol_table.func_map['global']['vars']:
        error.gen_err(
            f'Trying to access variable "{var_name}" that does not exist')
    else:
        p[0] = var_name


def p_ARRAY_ACCESS(p):
    'ARRAY_ACCESS : ARRAY_ACCESS_ID_AUX LBRACKET EXPRESSION RBRACKET'
    array_name = p[1]
    expression = p[3]
    pointer = quad_generator.gen_array_assignment_quads(array_name, expression)
    shared.expression_stack.pop()
    p[0] = pointer


def p_ARRAY_ACCESS_ID_AUX(p):
    'ARRAY_ACCESS_ID_AUX : ID'
    shared.expression_stack.append([])
    p[0] = p[1]

def p_MATRIX_ACCESS(p):
    'MATRIX_ACCESS : ARRAY_ACCESS_ID_AUX LBRACKET EXPRESSION RBRACKET LBRACKET EXPRESSION RBRACKET'
    matrix_name = p[1]
    expression1 = p[3]
    expression2 = p[6]
    pointer = quad_generator.gen_matrix_assignment_quads(
        matrix_name, expression1, expression2)
    shared.expression_stack.pop()
    p[0] = pointer


def p_error(p):
    error.gen_err(f'Syntax error! "{p}"')


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    error.gen_err("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

parser = yacc.yacc(debug=False, write_tables=False)


if shared.env == 'local':
    test_files = os.listdir('./tests')

    print('Choose a file to test dog')

    for i, test_file in enumerate(test_files):
        print(i + 1, test_file)

    data = ""
    aux = int(input())
    file_chosen = test_files[aux - 1]
    f = open(f'./tests/{file_chosen}', "r")
    if f.mode == 'r':
        data = f.read()
    else:
        error.gen_err("Pusiste el numero del archivo mal perro")
    lexer.input(data)


    while True:
        tok = lexer.token()
        if not tok:
            break

    # use debug=True for debugging
    parser.parse(data)
    # Add last quadruple
    quad_generator.gen_quad('ENDPROG', '', '', '')

    print("Compilado correctamente")
    for i in range(len(shared.quadruples)):
        print(shared.quadruples[i], "\t\t", shared.quadruples_address[i])

    vm.run(shared.quadruples_address, symbol_table.func_map)





def comp_and_run(file_name):
    f = open(file_name, 'r')
    data = f.read()
    parser.parse(data)
    quad_generator.gen_quad('ENDPROG', '', '', '')
    shared_vm.output.append('Whale >> Compiled Succesfully')
    vm.run(shared.quadruples_address, symbol_table.func_map)
    output_file = open('output.txt', 'w')
    for item in shared_vm.output:
        output_file.write(item + '\n')
    

        


# pprint = pprint.PrettyPrinter(indent=4)
# pprint.pprint(symbol_table.func_map)
# print(compilation_mem)

# symbol_table.print_func_map()
