from error import err, gen_err
from memory import memory
import semantic_cube
import shared


# Class used to instantiate while code is being parsed, used for cuadruplos

class Variable:
    def __init__(self, type, value, addr):  
        self.type = type  
        self.value = value
        self.addr = addr
  


# var map inside of function to have it in scope

# there is going to be a func key called global, where the global vars are stored

# func map contains
# 'type': type,
# 'vars': {}
# 'params': {}
# 'quadruple_reg' : '1'
# 'return_value' :

func_map = {
    'constants': {}
}

def find_variable_scope(var_name):
    if var_name in func_map["global"]["vars"]:
        return "global"
    elif var_name in func_map[shared.scope]["vars"]:
        return shared.scope
    gen_err(f"No se encontró variable {var_name} en scope global o local")

def insert_constant(constant):
    if constant not in func_map['constants']:
        constant_type = semantic_cube.check_type(constant)
        constant_map = {
            'memory_index': memory.constant_memory.compile_push(constant_type),
            'type': constant_type,
        }
        func_map['constants'][constant] = constant_map



empty_values = {
    'int': '0',
    'float': '0.0',
    'char': '',
}

def find_variable_attribute(var_name, attribute):
    if var_name in func_map[shared.scope]['vars']:
        return func_map[shared.scope]['vars'][var_name][attribute]
    elif var_name in func_map[shared.scope]['params']:
        return func_map[shared.scope]['params'][var_name][attribute]
    return None
    
def normalize_boolean(value):
    if value is False:
        return 0
    elif value is True:
        return 1
    else:
        return value

def find_register_result(operator, q2, q3):
    q2_memory_index = find_variable_attribute(q2, 'memory_index')
    q3_memory_index = find_variable_attribute(q3, 'memory_index')
    if q2_memory_index is not None:
        q2_value = memory.get_value(q2_memory_index)
    else:
        q2_value = semantic_cube.get_constant_value(q2)
    if q3_memory_index is not None:
        q3_value = memory.get_value(q3_memory_index)
    else:
        q3_value = semantic_cube.get_constant_value(q3)
    res = shared.operators[operator](q2_value, q3_value)
    res = normalize_boolean(res)
    return str(res)

def insert_tmp_value(operator, q2, q3, tmp_var_name):
    type_register = semantic_cube.find_return_type(q2, q3, operator)
    insert_tmp_var(shared.scope, tmp_var_name, type_register)

def insert_tmp_pointer(tmp_var_name):
    _insert_generic_local_var(shared.scope, memory.tmp_pointer_memory, tmp_var_name, "int")

def insert_quadruple_reg(func_name, quadruple_reg):
    if func_name not in func_map:
        gen_err(f'Tratando de agregar # de cuadruplo a funcion que no existe "{func_name}"')
    else:
        func_map[func_name]['quadruple_reg'] = quadruple_reg


def insert_function(func_name, type='void'):
    # check if already exists
    if func_name in func_map.keys():
        err('function was already declared', func_name)
    else:
        # create a function register
        func_map[func_name] = {
            'type': type,
            'vars': {},
            'params': {},
        }

def _insert_var(scope, segment, var_name, type=None, dimensions=None):
    if var_name in func_map[scope]['vars'].keys():
        err(f'variable already declared in {scope} scope', var_name)
    else:
        func_map[scope]['vars'][var_name] = {
            'memory_index' : segment.compile_push(type, dimensions),
            'type': type,
            'dimensions': dimensions,
        }

def _insert_generic_local_var(func_name, segment, var_name, type=None, dimensions=None):
    if var_name in func_map['global']['vars'].keys():
        # var already declared globally
        err('variable ' + var_name + ' already declared globally', func_name)
    _insert_var(func_name, segment, var_name, type, dimensions)

def _insert_local_var(func_name, var_name, type=None, dimensions=None):
    _insert_generic_local_var(func_name, memory.local_memory, var_name, type, dimensions)

def insert_tmp_var(func_name, var_name, type=None):
    _insert_generic_local_var(func_name, memory.tmp_memory, var_name, type)

def _insert_global_var(var_name, type, dimensions=None):
    _insert_var("global", memory.global_memory, var_name, type, dimensions)

def insert_var(scope, var_name, type=None, dimensions=None):
    if scope == "global":
        _insert_global_var(var_name, type, dimensions)
    # Is local
    else:
        _insert_local_var(scope, var_name, type, dimensions)


def insert_param(func_name, param_name, param_type):
    # append param to a function
    func_map[func_name]['params'][param_name] = {
        'memory_index': memory.local_memory.compile_push(param_type),
        'type': param_type,
    }



def print_func_map(map=func_map, indent=0):
   for key, value in map.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         print_func_map(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))



# testing

# insert_function('global', 'void')
# insert_function('main', 'int')

# insert_global_var('x', 'int', '10')
# insert_global_var('y', 'int', '20')
# insert_global_var('z', 'int', '30')


# insert_local_var('main', 'a', 'float', '10')
# insert_local_var('main', 'b', 'float', '20')
# insert_local_var('main', 'c', 'char', 'z')

# insert_param('main', 'numero', 'int')

# print(func_map['main']['params'])

# # memory testing
# print(memory)

