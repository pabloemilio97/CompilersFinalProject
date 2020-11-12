import semantic_cube
import symbol_table

cube = semantic_cube.cube
func_map = symbol_table.func_map

quadruples = []


operations = {
    '>': 0,
    '<': 0,
    '+': 1,
    '-': 1,
    '/': 2,
    '*': 2,
}

def quad_pos():
    return len(quadruples) + 1

def gen_arithmetic_quadruples(expression):
    curr_register = 1
    operands_stack = []
    operations_stack = []
    for value in expression:
        if value in operations: # if its and operation
            if len(operations_stack) == 0:
                operations_stack.append(value)
            elif operations[top(operations_stack)] >= operations[value]: # if previous operation is more important than current one then create quadruple
                while len(operations_stack) != 0 and operations[top(operations_stack)] >= operations[value]: # keep checking current operation with previous elements in stack
                    second_operand = operands_stack.pop()
                    first_operand = operands_stack.pop()
                    gen_quad(operations_stack.pop(), first_operand, second_operand, f't{curr_register}')
                    operands_stack.append(f't{curr_register}')
                    curr_register += 1
                operations_stack.append(value)
            else: # previous operation is less important than current one
                operations_stack.append(value)
        else: # its an operand
            operands_stack.append(value)
    # add remaining quads
    while len(operations_stack) != 0:
        second_operand = operands_stack.pop()
        first_operand = operands_stack.pop()
        gen_quad(operations_stack.pop(), first_operand, second_operand, f't{curr_register}')
        operands_stack.append(f't{curr_register}')
        curr_register += 1


def top(stack):
    return stack[len(stack) - 1]

def gen_quad(q1, q2, q3, q4):
    quad = [quad_pos(), q1, q2, q3, q4]
    quadruples.append(quad)
    print(quad)