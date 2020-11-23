import shared
import shared_vm
import semantic_cube
import print_file
import error
from memory import VirtualMemory


class State:
    def __init__(self, scope, return_type, memory):
        self.scope = scope
        self.return_type = return_type
        self.memory = memory


def insert_constants_memory(main_memory, constants):
    for constant, attr in constants.items():
        type = attr["type"]
        value = semantic_cube.get_constant_value(constant, type)
        main_memory.assign_value(attr["memory_index"], value)


def run(quadruples, func_map):
    # Insert constants into memory
    main_memory = VirtualMemory()
    insert_constants_memory(main_memory, func_map["constants"])
    main_state = State("main", "void", main_memory)
    shared_vm.call_stack = [main_state]

    endprog_register = len(quadruples) - 1
    while shared_vm.instruction_pointer != endprog_register:
        quadruple = quadruples[shared_vm.instruction_pointer]
        execute(quadruple)


def execute(quadruple):
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
        execute_ERA(quadruple)
    elif operation == "PARAM":
        execute_PARAM(quadruple)
    elif operation == "GOSUB":
        execute_GOSUB(quadruple)
    elif operation == "RETURN":
        execute_RETURN(quadruple)
    elif operation == "RETURN":
        execute_RETURN(quadruple)
    # ARRAYS
    elif operation == "ver":
        execute_ver(quadruple)
    # WRITE
    elif operation == "WRITE":
        execute_write(quadruple)

    shared_vm.instruction_pointer += 1


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


def execute_gotoF(quadruple):
    memory = shared_vm.call_stack[-1].memory
    if_expression_result = memory.get_value(quadruple[2])
    if if_expression_result == 0:
        execute_goto(quadruple)


def execute_ERA(quadruple):
    pass


def execute_PARAM(quadruple):
    pass


def execute_GOSUB(quadruple):
    pass


def execute_RETURN(quadruple):
    pass


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
