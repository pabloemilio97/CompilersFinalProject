from error import err, gen_err
import memory
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

def find_variable_or_param_scope(var_name):
    if var_name in func_map["global"]["vars"]:
        return "global"
    elif var_name in func_map[shared.scope]["vars"] or func_map[shared.scope]["params"]:
        return shared.scope
    gen_err(f"Could not find "{var_name}" in  global or local scope")

def find_variable_scope(var_name):
    if var_name in func_map["global"]["vars"]:
        return "global"
    elif var_name in func_map[shared.scope]["vars"]:
        return shared.scope
    gen_err(f"Could not find "{var_name}" in  global or local scope")

def insert_constant(constant):
    if constant not in func_map['constants']:
        constant_type = semantic_cube.check_type(constant)
        constant_map = {
            'memory_index': memory.compilation_mem.constant_memory.compile_push(constant_type),
            'type': constant_type,
        }
        func_map['constants'][constant] = constant_map


empty_values = {
    'int': '0',
    'float': '0.0',
    'char': '',
}

def var_or_param(scope, var_name):
    if var_name in func_map[scope]['vars']:
        return 'vars'
    elif var_name in func_map[scope]['params']:
        return 'params'

def insert_tmp_value(operator, q2, q3, tmp_var_name):
    type_register = semantic_cube.find_return_type(q2, q3, operator)
    insert_tmp_var(shared.scope, tmp_var_name, type_register)

def insert_tmp_pointer(tmp_var_name, pointed_type):
    _insert_generic_local_var(shared.scope, memory.compilation_mem.tmp_pointer_memory, tmp_var_name, "int", pointed_type=pointed_type)

def insert_quadruple_reg(func_name, quadruple_reg):
    if func_name not in func_map:
        gen_err(f'Trying to add quadruple register to a function that does not exist "{func_name}"')
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

def _insert_var(scope, segment, var_name, type=None, dimensions=None, pointed_type=None):
    if var_name in func_map[scope]['vars'].keys():
        err(f'variable already declared in {scope} scope', var_name)
    else:
        func_map[scope]['vars'][var_name] = {
            'memory_index' : segment.compile_push(type, dimensions),
            'type': type,
            'dimensions': dimensions,
            'pointed_type': pointed_type,
        }

def _insert_generic_local_var(func_name, segment, var_name, type=None, dimensions=None, pointed_type=None):
    if var_name in func_map['global']['vars'].keys():
        # var already declared globally
        err('variable ' + var_name + ' already declared globally', func_name)
    _insert_var(func_name, segment, var_name, type, dimensions, pointed_type)

def _insert_local_var(func_name, var_name, type=None, dimensions=None):
    _insert_generic_local_var(func_name, memory.compilation_mem.local_memory, var_name, type, dimensions)

def insert_tmp_var(func_name, var_name, type=None):
    _insert_generic_local_var(func_name, memory.compilation_mem.tmp_memory, var_name, type)

def _insert_global_var(var_name, type, dimensions=None):
    _insert_var("global", memory.compilation_mem.global_memory, var_name, type, dimensions)

def insert_var(scope, var_name, type=None, dimensions=None):
    if scope == "global":
        _insert_global_var(var_name, type, dimensions)
    # Is local
    else:
        _insert_local_var(scope, var_name, type, dimensions)


def insert_param(func_name, param_name, param_type):
    # append param to a function
    func_map[func_name]['params'][param_name] = {
        'memory_index': memory.compilation_mem.local_memory.compile_push(param_type),
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

