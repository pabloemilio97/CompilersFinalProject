import semantic_cube
import symbol_table
import shared
from shared import quadruples, operands_stack, operations_stack, jump_stack, jump_operations, numerics, param_nums_stack
from memory import memory

cube = semantic_cube.cube
func_map = symbol_table.func_map

operations = {
    '>': 0,
    '<': 0,
    '==': 0,
    '!=': 0,
    '>=': 0,
    '<=': 0,
    '+': 1,
    '-': 1,
    '/': 2,
    '*': 2,
}

def create_tmp_from_operation(operator, q2, q3):
    """
    Return curr_register and add 1 to it.
    We usually have to add 1 each time we consult curr_register.
    """
    old_value = int(numerics["curr_register"])
    symbol_table.insert_tmp_value(operator, q2, q3, f't{old_value}')
    numerics["curr_register"] = str(old_value + 1)
    return f"t{old_value}"

def create_tmp_pointer():
    """
    Create tmp pointer for array access in memory.
    """
    old_value = int(numerics["curr_pointer_register"])
    symbol_table.insert_tmp_pointer(f'(t{old_value})')
    numerics["curr_pointer_register"] = str(old_value + 1)
    return f"(t{old_value})"

def quad_pos():
    return str(len(quadruples))

def gen_assign_quadruples(expression, assign_to):
    if len(expression) == 1:
        semantic_cube.same_type(assign_to, expression[0])
        gen_quad('=', expression[0], '', assign_to)
    else:
        gen_arithmetic_quadruples(expression)
        semantic_cube.same_type(assign_to, quadruples[-1][-1],)
        gen_quad('=', quadruples[-1][-1], '', assign_to)


def _gen_condition_quadruples(expression):
    if len(expression) == 1:
        gen_quad('gotoF', expression[0], '', '')
    else:
        gen_arithmetic_quadruples(expression)
        # here we know that last quad has the result of if expression
        gen_quad('gotoF', quadruples[-1][-1], '', '')

def gen_if_quadruples(expression):
    _gen_condition_quadruples(expression)

def gen_else_quadruples():
    # The quadruple number to which the if's gotoF will go to
    if_jump_to = int(jump_stack.pop())
    gen_quad('goto', '', '', '')
    quadruples[if_jump_to][4] = quad_pos()

def _gen_endcondition_quadruples():
    jump_to = int(jump_stack.pop())
    quadruples[jump_to][4] = quad_pos()

def gen_endelse_quadruples():
    _gen_endcondition_quadruples()

def gen_endif_quadruples():
    _gen_endcondition_quadruples()


def gen_while_quadruples(expression):
    _gen_condition_quadruples(expression)


def _gen_endloop_quadruples():
    jump_to_gotoF = int(jump_stack.pop())
    jump_to_goto = jump_stack.pop()
    gen_quad('goto', '', '', jump_to_goto, False)
    quadruples[jump_to_gotoF][4] = quad_pos()

def gen_endwhile_quadruples():
    _gen_endloop_quadruples()
    
def gen_endfor_quadruples(variable):
    curr_register = create_tmp_from_operation('+', variable, '1')
    gen_quad('+', variable, '1', curr_register)
    gen_quad('=', curr_register, '', variable)
    _gen_endloop_quadruples()

def gen_for_quadruples(variable, expression):
    """
    variable -> variable to compare to
    expression -> when variable reaches this value, cycle ends
    """
    if len(expression) == 1:
        expression_result = expression[0]
    else:
        gen_arithmetic_quadruples(expression)
        expression_result = quadruples[-1][-1]
    
    gen_quad('<', variable, expression_result, create_tmp_from_operation('<', variable, expression_result))
    comparison_result = quadruples[-1][-1]
    gen_quad('gotoF', comparison_result, '', '')


def gen_endfunc_quadruple():
    gen_quad('ENDFUNC', '', '', '')
    memory.local_memory.flush()
    memory.tmp_memory.flush()

def _gen_generic_quadruples(operation, expression):
    if len(expression) == 1:
        gen_quad(operation, '', '', expression[0])
    else:
        gen_arithmetic_quadruples(expression)
        expression_result = quadruples[-1][-1]
        gen_quad(operation, '', '', expression_result)

def gen_return_quadruples(expression):
    _gen_generic_quadruples('RETURN', expression)

def gen_write_quadruples(expression):
    _gen_generic_quadruples('WRITE', expression)

def gen_param_quadruples(expression):
    str_param_num = f'param{str(param_nums_stack[-1])}'
    if len(expression) == 1:
        gen_quad('PARAM', expression[0], '', str_param_num)
    else:
        gen_arithmetic_quadruples(expression)
        # here we have to validate that what ends up in the last tmp value register, is the same type as the parameter
        param_result = quadruples[-1][-1]
        gen_quad('PARAM', param_result, '', str_param_num)
    param_nums_stack[-1] += 1

def gen_function_call_quads(function_name):
    function_type = symbol_table.func_map[function_name]['type']
    old_value = int(numerics["curr_register"])
    new_tmp = f't{old_value}'
    gen_quad('=', function_name, '', new_tmp)
    symbol_table.insert_tmp_var(shared.scope, new_tmp, function_type)
    numerics["curr_register"] = str(old_value + 1)
    return new_tmp
    
def gen_arithmetic_quadruples(expression):
    for value in expression:
        # print(value)
        # print('operations stack: ', operations_stack)
        # print('operands stack: ', operands_stack)
        # print('\n')
        if value == ')':
            flush_remaining(operations_stack, operands_stack)
            operations_stack.pop()
        elif value in operations: # if its and operation
            if not top(operations_stack):
                operations_stack.append(value)
            elif operations[top(operations_stack)] >= operations[value]: # if previous operation is more important than current one then create quadruple
                while top(operations_stack) and operations[top(operations_stack)] >= operations[value]: # keep checking current operation with previous elements in stack
                    second_operand = operands_stack.pop()
                    first_operand = operands_stack.pop()
                    operation = operations_stack.pop()
                    curr_register = create_tmp_from_operation(operation, first_operand, second_operand)
                    gen_quad(operation, first_operand, second_operand, curr_register)
                    operands_stack.append(curr_register)
                operations_stack.append(value)
            else: # previous operation is less important than current one
                operations_stack.append(value)
        else: # its an operand
            if value == '(':
                operations_stack.append(value)
            else:
                operands_stack.append(value)
    # add remaining quads
    flush_remaining(operations_stack, operands_stack)

def flush_remaining(operations_stack, operands_stack):
    while top(operations_stack):
        second_operand = operands_stack.pop()
        first_operand = operands_stack.pop()
        operator = operations_stack.pop()
        curr_register = create_tmp_from_operation(operator, first_operand, second_operand)
        gen_quad(operator, first_operand, second_operand, curr_register)
        operands_stack.append(curr_register)

def gen_array_assignment_quads(array_name, expression):
    if len(expression) == 1:
        expression_result = expression[0]
    else:
        gen_arithmetic_quadruples(expression)
        expression_result = quadruples[-1][-1]

    scope = symbol_table.find_variable_scope(array_name)
    array_info = symbol_table.func_map[scope]['vars'][array_name]
    upper_bound = array_info['dimensions'][0]
    array_start_address = str(array_info['memory_index'])

    gen_quad('ver', expression_result, '0', upper_bound)
    pointer = create_tmp_pointer()
    gen_quad('+', expression_result, array_start_address, pointer)
    shared.assign_to = pointer

def gen_matrix_assignment_quads(matrix_name, expression1, expression2):
    # generate quadruples for firt dim expression
    if len(expression1) == 1:
        expression_result1 = expression1[0]
    else:
        gen_arithmetic_quadruples(expression1)
        expression_result1 = quadruples[-1][-1]

    # get matrix start address, upper bound1 and 2
    scope = symbol_table.find_variable_scope(matrix_name)
    matrix_info = symbol_table.func_map[scope]['vars'][matrix_name]
    upper_bound1 = matrix_info['dimensions'][0]
    upper_bound2 = matrix_info['dimensions'][1]
    matrix_start_address = str(matrix_info['memory_index'])

    # generate first verify
    gen_quad('ver', expression_result1, '0', upper_bound1)

    # generate tmp quad for getting right address if mat is mat[10][10] (mat[4][6]) (we need 4 * 10 + 6 to get that address)
    tmp_register = create_tmp_from_operation('*', expression_result1, upper_bound2)
    gen_quad('*', expression_result1, upper_bound2, tmp_register)

    # generate second dim expression quadruples
    if len(expression2) == 1:
        expression_result2 = expression2[0]
    else:
        gen_arithmetic_quadruples(expression2)
        expression_result2 = quadruples[-1][-1]

    # generate second verify
    gen_quad('ver', expression_result2, '0', upper_bound2)
    
    # tmp_register + second expression result
    tmp_register2 = create_tmp_from_operation('+', tmp_register, expression_result2)
    gen_quad('+', tmp_register, expression_result2, tmp_register2)

    # pointer + 
    pointer = create_tmp_pointer()
    gen_quad('+', tmp_register2, matrix_start_address, pointer)
    shared.assign_to = pointer

def top(stack):
    if not stack or stack[-1] == '(': 
        return ''
    else:
        return stack[-1]

def gen_quad(q1, q2, q3, q4, shouldAppendToJump=True):
    quad = [quad_pos(), q1, q2, q3, q4]
    if q1 in jump_operations and shouldAppendToJump:
        jump_stack.append(quad_pos())
    quadruples.append(quad)

