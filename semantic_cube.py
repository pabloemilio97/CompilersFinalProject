import symbol_table
import error
import shared

# Third Level
int_int_operator_map = {
    "+": "int",
    "-": "int",
    "*": "int",
    "/": "float",
    "<": "int",
    ">": "int",
    "<=": "int",
    ">=": "int",
    "==": "int",
    "!=": "int",
    "&": "int",
    "|": "int",
}

int_float_operator_map = {
    "+": "float",
    "-": "float",
    "*": "float",
    "/": "float",
    "<": "int",
    ">": "int",
    "<=": "int",
    ">=": "int",
    "==": "int",
    "!=": "int",
    "&": "int",
    "|": "int",
}

int_char_operator_map = {
    "+": "invalid",
    "-": "invalid",
    "*": "invalid",
    "/": "invalid",
    "<": "invalid",
    ">": "invalid",
    "<=": "invalid",
    ">=": "invalid",
    "==": "invalid",
    "!=": "invalid",
    "&": "invalid",
    "|": "invalid",
}

float_int_operator_map = {
    "+": "float",
    "-": "float",
    "*": "float",
    "/": "float",
    "<": "int",
    ">": "int",
    "<=": "int",
    ">=": "int",
    "==": "int",
    "!=": "int",
    "&": "int",
    "|": "int",
}

float_float_operator_map = {
    "+": "float",
    "-": "float",
    "*": "float",
    "/": "float",
    "<": "int",
    ">": "int",
    "<=": "int",
    ">=": "int",
    "==": "int",
    "!=": "int",
    "&": "int",
    "|": "int",
}

float_char_operator_map = {
    "+": "invalid",
    "-": "invalid",
    "*": "invalid",
    "/": "invalid",
    "<": "invalid",
    ">": "invalid",
    "<=": "invalid",
    ">=": "invalid",
    "==": "invalid",
    "!=": "invalid",
    "&": "invalid",
    "|": "invalid",
}

char_int_operator_map = {
    "+": "invalid",
    "-": "invalid",
    "*": "invalid",
    "/": "invalid",
    "<": "invalid",
    ">": "invalid",
    "<=": "invalid",
    ">=": "invalid",
    "==": "invalid",
    "!=": "invalid",
    "&": "invalid",
    "|": "invalid",
}

char_float_operator_map = {
    "+": "invalid",
    "-": "invalid",
    "*": "invalid",
    "/": "invalid",
    "<": "invalid",
    ">": "invalid",
    "<=": "invalid",
    ">=": "invalid",
    "==": "invalid",
    "!=": "invalid",
    "&": "invalid",
    "|": "invalid",
}

char_char_operator_map = {
    "+": "invalid",
    "-": "invalid",
    "*": "invalid",
    "/": "invalid",
    "<": "invalid",
    ">": "invalid",
    "<=": "invalid",
    ">=": "invalid",
    "==": "invalid",
    "!=": "invalid",
    "&": "invalid",
    "|": "invalid",
}

# Second Level
int_map = {
    "int": int_int_operator_map,
    "float": int_float_operator_map,
    "char": int_char_operator_map,
}

float_map = {
    "int": float_int_operator_map,
    "float": float_float_operator_map,
    "char": float_char_operator_map,
}

char_map = {
    "int": char_int_operator_map,
    "float": char_float_operator_map,
    "char": char_char_operator_map,
}


# First level
cube = {
    "int": int_map,
    "float": float_map,
    "char": char_map,
}

def same_type(input1, input2, raise_error=True):
    type1 = check_type(input1)
    type2 = check_type(input2)
    is_same_type = type1 == type2
    if(raise_error and not is_same_type):
        error.gen_err(f"Tratando de asignar a {input1} un tipo incorrecto: {type2}")
    return is_same_type

def _find_return_type(type1, type2, operator):
    res = cube[type1][type2][operator]
    if (res == 'invalid'):
        error.gen_err(f'No se puede hacer operacion de {type1} con {type2}')
    return res

def find_return_type(input1, input2, operator):
    type1 = check_type(input1)
    type2 = check_type(input2)
    res = _find_return_type(type1, type2, operator)
    return res

def _check_pointer_type(pointer):
    var_name = pointer[1:-1]
    if var_name in symbol_table.func_map['global']['vars']:
        return symbol_table.func_map['global']['vars'][var_name]['pointed_type']
    if var_name in symbol_table.func_map[shared.scope]['vars']:
        return symbol_table.func_map[shared.scope]['vars'][var_name]['pointed_type']
    elif var_name in symbol_table.func_map[shared.scope]['params']:
        return symbol_table.func_map[shared.scope]['params'][var_name]['pointed_type']
    error.gen_err(f'Apuntador "{pointer}" no encontrada')

def check_type(input):
    if len(input) >= 2 and input[0] == '(' and input[-1] == ')':
        return _check_pointer_type(input)
    if  2 <= len(input) <= 3 and input[0] == '"' and input[-1] == '"':
        return "char"
    if input in symbol_table.func_map['global']['vars']:
        return symbol_table.func_map['global']['vars'][input]['type']
    if input in symbol_table.func_map[shared.scope]['vars']:
        return symbol_table.func_map[shared.scope]['vars'][input]['type']
    elif input in symbol_table.func_map[shared.scope]['params']:
        return symbol_table.func_map[shared.scope]['params'][input]['type']
    elif input.isdigit():
        return 'int'
    else:
        try: 
            float(input)
            return 'float'
        except:
            error.gen_err(f'no se puede hacer operaciones con input "{input}"')


def get_constant_value(input):
    input_type = check_type(input)
    if input_type == 'int':
        input_result = int(input)
    elif input_type == 'float':
        input_result = float(input)
    else:
        input_result = input
    return input_result


def get_value(input):
    value = symbol_table.find_variable_attribute(input, 'value')
    if value is not None:
        return value
    else:
        return get_constant_value(input)
        
    
