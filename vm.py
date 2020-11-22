import shared
import shared_vm
from memory import VirtualMemory

class State:
    def __init__(self, scope, return_type, memory):
        self.scope = scope
        self.return_type = return_type
        self.memory = memory


def insert_constants_memory(main_memory, constants):
    for constant, attr in constants.items():
        type = attr["type"]
        main_memory.vm_push_constant(constant, attr["memory_index"], type)

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
    #ARITHEMTIC
    if operation in shared.operators:
        execute_arithmetic(quadruple)
    #ASSIGNMENT
    elif operation == "=":
        execute_assign(quadruple)
    #JUMPS
    elif operation == "goto":
        execute_goto(quadruple)
    elif operation == "gotoF":
        execute_gotoF(quadruple)
    #FUNCTIONS
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
    #ARRAYS
    elif operation == "ver":
        execute_ver(quadruple)
    

def execute_arithmetic(quadruple):
    pass

def execute_assign(quadruple):
    pass

def execute_goto(quadruple):
    pass

def execute_gotoF(quadruple):
    pass

def execute_ERA(quadruple):
    pass

def execute_PARAM(quadruple):
    pass

def execute_GOSUB(quadruple):
    pass

def execute_RETURN(quadruple):
    pass

def execute_ver(quadruple):
    pass