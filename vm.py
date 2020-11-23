import shared
import shared_vm
import semantic_cube
import print_file
import error
import copy
from memory import VirtualMemory


class State:
    def __init__(self, scope, return_type, memory, instruction_pointer):
        self.scope = scope
        self.return_type = return_type
        self.memory = memory
        self.instruction_pointer = instruction_pointer


def insert_constants_memory(main_memory, constants):
    for constant, attr in constants.items():
        type = attr["type"]
        value = semantic_cube.get_constant_value(constant, type)
        main_memory.assign_value(attr["memory_index"], value)


def run(quadruples, func_map):
    # Insert constants into memory
    main_memory = VirtualMemory()
    insert_constants_memory(main_memory, func_map["constants"])
    main_state = State("main", "void", main_memory,
                       shared_vm.instruction_pointer)
    shared_vm.call_stack = [main_state]

    endprog_register = len(quadruples) - 1
    while shared_vm.instruction_pointer != endprog_register:
        quadruple = quadruples[shared_vm.instruction_pointer]
        execute(quadruple, func_map, quadruples)


def execute(quadruple, func_map, quadruples):
    operation = quadruple[1]
    # ARITHEMTIC
    if operation in shared.operators:
        execute_arithmetic(quadruple)
    # ASSIGNMENT
    elif operation == "=":
        execute_assign(quadruple)
    # JUMPS
    elif operation == "goto":
        execute_goto(quadruple)
    elif operation == "gotoF":
        execute_gotoF(quadruple)
    # FUNCTIONS
    elif operation == "ERA":
        execute_ERA(quadruple, func_map)
    elif operation == "PARAM":
        execute_PARAM(quadruple, func_map)
    elif operation == "GOSUB":
        execute_GOSUB(quadruple, func_map)
    elif operation == "RETURN":
        execute_RETURN(quadruple, quadruples)
    elif operation == "ENDFUNC":
        execute_ENDFUNC(quadruple)
    # ARRAYS
    elif operation == "ver":
        execute_ver(quadruple)
    # WRITE
    elif operation == "WRITE":
        execute_write(quadruple)

    shared_vm.instruction_pointer += 1
    shared_vm.call_stack[-1].instruction_pointer = shared_vm.instruction_pointer


def execute_arithmetic(quadruple):
    # Get operator
    operator = shared.operators[quadruple[1]]
    # Get operand values
    memory = shared_vm.call_stack[-1].memory
    left_operand = memory.get_value(quadruple[2])
    right_operand = memory.get_value(quadruple[3])
    # Do the operation
    result = operator(left_operand, right_operand)
    if result is True:
        result = 1
    elif result is False:
        result = 0
    # Store the operation
    store_address = quadruple[4]
    memory.assign_value(store_address, result)


def execute_assign(quadruple):
    memory = shared_vm.call_stack[-1].memory
    result = memory.get_value(quadruple[2])  # right part of =
    assign_to_address = quadruple[4]
    memory.assign_value(assign_to_address, result)


def execute_goto(quadruple):
    shared_vm.instruction_pointer = quadruple[4]
    shared_vm.instruction_pointer -= 1
    shared_vm.call_stack[-1].instruction_pointer = shared_vm.instruction_pointer


def execute_gotoF(quadruple):
    memory = shared_vm.call_stack[-1].memory
    if_expression_result = memory.get_value(quadruple[2])
    if if_expression_result == 0:
        execute_goto(quadruple)


def execute_ERA(quadruple, func_map):
    func_name = quadruple[4]
    start_func_reg = func_map[func_name]['quadruple_reg']
    func_return_type = func_map[func_name]['type']
    func_memory = VirtualMemory()
    func_state = State(func_name, func_return_type,
                       func_memory, start_func_reg)
    shared_vm.preparing_state = func_state


def execute_PARAM(quadruple, func_map):
    param_value = shared_vm.call_stack[-1].memory.get_value(quadruple[2])
    scope = shared_vm.preparing_state.scope
    memory = shared_vm.preparing_state.memory
    param_index = int(quadruple[4][-1]) - 1
    param_memory_index = list(func_map[scope]['params'].values())[
        param_index]['memory_index']
    memory.assign_value(param_memory_index, param_value)


def execute_GOSUB(quadruple, func_map):
    func_name = quadruple[4]
    func_instruction_pointer = func_map[func_name]['quadruple_reg']
    # Add one to current scope
    shared_vm.call_stack[-1].instruction_pointer += 1
    shared_vm.instruction_pointer = func_instruction_pointer
    # Append copy of preparing state
    shared_vm.call_stack.append(shared_vm.preparing_state)
    shared_vm.preparing_state = None
    # Compensate always adding one
    shared_vm.instruction_pointer -= 1
    # Make top of call stack pointer = to global pointer
    shared_vm.call_stack[-1].instruction_pointer = shared_vm.instruction_pointer


def execute_RETURN(quadruple, quadruples):
    memory = shared_vm.call_stack[-1].memory
    return_value = memory.get_value(quadruple[4])
    # return global pointer
    prev_memory = shared_vm.call_stack[-2]
    prev_pointer = prev_memory.instruction_pointer
    assign_quad = quadruples[prev_pointer]
    # check if prev state expects a return value
    if assign_quad[2] == shared_vm.call_stack[-1].scope:
        address_to_assign = assign_quad[4]
        # assign return value to address to assign
        prev_memory.memory.assign_value(
            address_to_assign, return_value)
    else:
        # If we didnt execute = quadruple, execute current quadruple of past state
        shared_vm.call_stack[-2].instruction_pointer -= 1

def execute_ENDFUNC(quadruple):
    shared_vm.call_stack.pop()
    shared_vm.instruction_pointer = shared_vm.call_stack[-1].instruction_pointer



def execute_ver(quadruple):
    memory = shared_vm.call_stack[-1].memory
    access_index = memory.get_value(quadruple[2])
    lower_bound = memory.get_value(quadruple[3])
    upper_bound = memory.get_value(quadruple[4])
    if access_index < lower_bound or access_index > upper_bound:
        error.gen_runtime_err(
            'Tratando de accesar o asignar a un elemento fuera de limites')


def execute_write(quadruple):
    memory = shared_vm.call_stack[-1].memory
    value = memory.get_value(quadruple[4])
    print_file.print_func(value)
