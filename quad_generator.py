import semantic_cube
import symbol_table
from shared import quadruples, operands_stack, operations_stack, jump_stack, curr_register, jump_operations

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


def quad_pos():
    return str(len(quadruples))

def next_quad_pos():
    return str(len(quadruples) + 1)

def gen_assign_quadruples(expression, assign_to):
    if len(expression) == 1:
        gen_quad('=', expression[0], '', assign_to)
    else:
        gen_arithmetic_quadruples(expression)
        gen_quad('=', quadruples[-1][-1], '', assign_to)


def gen_if_quadruples(expression):
    if len(expression) == 1:
        pass
    else:
        gen_arithmetic_quadruples(expression)
    # here we know that last quad has the result of if expression
    gen_quad('gotoF', quadruples[-1][-1], '', '')

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
    if len(expression) == 1:
        pass
    else:
        gen_arithmetic_quadruples(expression)
        # here we know the last quad is the result of the while expression
    gen_quad('gotoF', '', quadruples[-1][-1], '')

def assign_gotoF_quadruple_pos():
    jump_to = int(jump_stack.pop())
    quadruples[jump_to][4] = next_quad_pos()

def gen_while_goto_quadruple():
    jump_to = jump_stack.pop()
    gen_quad('goto', '', '', jump_to, False)
    
def gen_arithmetic_quadruples(expression):
    global curr_register
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
                    gen_quad(operations_stack.pop(), first_operand, second_operand, f't{curr_register}')
                    operands_stack.append(f't{curr_register}')
                    curr_register += 1
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
    global curr_register
    while top(operations_stack):
        second_operand = operands_stack.pop()
        first_operand = operands_stack.pop()
        gen_quad(operations_stack.pop(), first_operand, second_operand, f't{curr_register}')
        operands_stack.append(f't{curr_register}')
        curr_register += 1


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

