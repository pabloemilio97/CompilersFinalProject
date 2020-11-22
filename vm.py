import shared

instruction_pointer = 0
def run(quadruples, func_map):
    endprog_register = len(quadruples) - 1
    while instruction_pointer != endprog_register:
        quadruple = quadruples[instruction_pointer]
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