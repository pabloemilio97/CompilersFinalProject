import semantic_cube
import symbol_table
import shared
import error
from shared import quadruples, quadruples_address, operands_stack, operations_stack, jump_stack, jump_operations, numerics, param_nums_stack
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

def create_tmp_pointer(base_dir):
    """
    Create tmp pointer for array access in memory.
    """
    pointed_type = memory.get_address_type(base_dir)
    old_value = int(numerics["curr_register"])
    symbol_table.insert_tmp_pointer(f't{old_value}', pointed_type)
    numerics["curr_register"] = str(old_value + 1)
    return f"t{old_value}"

def get_expression_result(expression):
    """
    Generate arithemtic quadruples and return result.
    """
    if len(expression) == 1:
        expression_result = expression[0]
    else:
        gen_arithmetic_quadruples(expression)
        expression_result = quadruples[-1][-1]
    return expression_result

def quad_pos():
    return len(quadruples)

def gen_assign_quadruples(expression, assign_to):
    expression_result = get_expression_result(expression)
    semantic_cube.same_type(assign_to, expression_result)
    gen_quad('=', expression_result, '', assign_to)


def _gen_condition_quadruples(expression):
    expression_result = get_expression_result(expression)
    gen_quad('gotoF', expression_result, '', '')

def gen_if_quadruples(expression):
    _gen_condition_quadruples(expression)

def gen_else_quadruples():
    # The quadruple number to which the if's gotoF will go to
    if_jump_to = int(jump_stack.pop())
    gen_quad('goto', '', '', '')
    update_quadruples(if_jump_to)

def _gen_endcondition_quadruples():
    jump_to = int(jump_stack.pop())
    update_quadruples(jump_to)

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
    update_quadruples(jump_to_gotoF)

def gen_endwhile_quadruples():
    _gen_endloop_quadruples()
    
def gen_endfor_quadruples(variable):
    symbol_table.insert_constant('1')
    curr_register = create_tmp_from_operation('+', variable, '1')
    gen_quad('+', variable, '1', curr_register)
    gen_quad('=', curr_register, '', variable)
    _gen_endloop_quadruples()

def gen_for_quadruples(variable, expression):
    """
    variable -> variable to compare to
    expression -> when variable reaches this value, cycle ends
    """
    expression_result = get_expression_result(expression)
    
    gen_quad('<', variable, expression_result, create_tmp_from_operation('<', variable, expression_result))
    comparison_result = quadruples[-1][-1]
    gen_quad('gotoF', comparison_result, '', '')


def gen_endfunc_quadruple():
    gen_quad('ENDFUNC', '', '', '')
    memory.local_memory.flush()
    memory.tmp_memory.flush()

def _gen_generic_quadruples(operation, expression):
    expression_result = get_expression_result(expression)
    gen_quad(operation, '', '', expression_result)

def gen_return_quadruples(expression):
    _gen_generic_quadruples('RETURN', expression)

def gen_write_quadruples(expression):
    _gen_generic_quadruples('WRITE', expression)

def gen_param_quadruples(expression):
    def is_correct_type(expression_result, param_num):
        function_name = shared.function_call_names_stack[-1]
        params = list(func_map[function_name]['params'].values())
        param_type = params[param_num-1]["type"]
        expression_type = semantic_cube.check_type(expression_result)
        if not param_type == expression_type:
            params = list(func_map[function_name]['params'].keys())
            param_name = params[param_num-1]
            error.gen_err(f'Type not valid for param "{param_name}" in function call "{function_name}".')
    
    param_num = param_nums_stack[-1]
    str_param_num = f'param{str(param_num)}'
    expression_result = get_expression_result(expression)
    is_correct_type(expression_result, param_num)
    gen_quad('PARAM', expression_result, '', str_param_num)
    param_nums_stack[-1] += 1

def gen_function_call_quads(function_name):
    function_type = symbol_table.func_map[function_name]['type']
    old_value = int(numerics["curr_register"])
    new_tmp = f't{old_value}'
    symbol_table.insert_tmp_var(shared.scope, new_tmp, function_type)
    gen_quad('=', function_name, '', new_tmp)
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

def _gen_array_tmp_pointer(expression_result, base_dir):
    """
    Final step when accessing array.
    Create pointer and quad to assign a value to it.
    """
    pointer = create_tmp_pointer(base_dir)
    gen_quad('+', expression_result, str(base_dir), pointer)
    return pointer

def _gen_ver_quads(expression_result, upper_bound):
    upper_bound = str(int(upper_bound) - 1)
    symbol_table.insert_constant('0')
    symbol_table.insert_constant(upper_bound)
    gen_quad('ver', expression_result, '0', upper_bound)

def gen_array_assignment_quads(array_name, expression):
    scope = symbol_table.find_variable_scope(array_name)
    array_info = symbol_table.func_map[scope]['vars'][array_name]
    upper_bound = array_info['dimensions'][0]
    array_start_address = array_info['memory_index']
    symbol_table.insert_constant(str(array_start_address))
    expression_result = get_expression_result(expression)

    _gen_ver_quads(expression_result, upper_bound)
    pointer = _gen_array_tmp_pointer(expression_result, array_start_address)
    return f"({pointer})"

def gen_matrix_assignment_quads(matrix_name, expression1, expression2):
    # get matrix start address, upper bound1 and 2
    scope = symbol_table.find_variable_scope(matrix_name)
    matrix_info = symbol_table.func_map[scope]['vars'][matrix_name]
    upper_bound1 = matrix_info['dimensions'][0]
    upper_bound2 = matrix_info['dimensions'][1]
    matrix_start_address = matrix_info['memory_index']
    symbol_table.insert_constant(str(matrix_start_address))

    # generate quadruples for firt dim expression
    expression_result1 = get_expression_result(expression1)

    # generate first verify
    _gen_ver_quads(expression_result1, upper_bound1)

    # generate tmp quad for getting right address if mat is mat[10][10] (mat[4][6]) (we need 4 * 10 + 6 to get that address)
    tmp_register = create_tmp_from_operation('*', expression_result1, upper_bound2)
    gen_quad('*', expression_result1, upper_bound2, tmp_register)

    # generate second dim expression quadruples
    expression_result2 = get_expression_result(expression2)

    # generate second verify
    _gen_ver_quads(expression_result2, upper_bound2)
    
    # tmp_register + second expression result
    tmp_register2 = create_tmp_from_operation('+', tmp_register, expression_result2)
    gen_quad('+', tmp_register, expression_result2, tmp_register2)

    # pointer + 
    pointer = _gen_array_tmp_pointer(tmp_register2, matrix_start_address)
    return f"({pointer})"

def top(stack):
    if not stack or stack[-1] == '(': 
        return ''
    else:
        return stack[-1]

def gen_address_quad(q1, q2, q3, q4):
    
    def transform_to_address(element):
        # Check if it is a function
        if element in symbol_table.func_map or element == '':
            return element
        elif element in symbol_table.func_map['constants']:
            return symbol_table.func_map['constants'][element]['memory_index']
        elif len(element) >= 2 and element[0] == '(' and element[-1] == ')':
            element = element[1:-1]
            scope = symbol_table.find_variable_or_param_scope(element)
            memory_address = symbol_table.func_map[scope]['vars'][element]['memory_index']
            return f'({memory_address})'

        scope = symbol_table.find_variable_or_param_scope(element)
        var_or_param = symbol_table.var_or_param(scope, element)
        memory_address = symbol_table.func_map[scope][var_or_param][element]['memory_index']
        return memory_address
    address_values = [q2, q3, q4]
    if q1 == "goto":
        pass
    elif q1 == "gotoF" or q1 == "PARAM":
        address_values[0] = transform_to_address(address_values[0])
    else:
        for i in range(3):
            address_values[i] = transform_to_address(address_values[i])
        
    quad = [quad_pos(), q1, address_values[0], address_values[1], address_values[2]]
    quadruples_address.append(quad)

def update_quadruples(pos):
    quadruples[pos][-1] = quad_pos()
    quadruples_address[pos][-1] = quad_pos()

def gen_quad(q1, q2, q3, q4, shouldAppendToJump=True):
    gen_address_quad(q1,q2,q3,q4)
    quad = [quad_pos(), q1, q2, q3, q4]
    if q1 in jump_operations and shouldAppendToJump:
        jump_stack.append(quad_pos())
    quadruples.append(quad)

