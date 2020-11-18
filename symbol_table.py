from error import err, gen_err
from memory import memory


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
# 'params': []
# 'quadruple_reg' : '1'

func_map = {}


empty_values = {
    'int': 0,
    'float': 0.0,
    'char': '',
}

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
            'params': [],
        }

def _insert_local_var(func_name, var_name, type=None, value=None):
    # Inserts local variable for a function
    if var_name in func_map[func_name]['vars'].keys(): # already declared in same function
        err('variable ' + var_name + ' already declared', var_name)
    elif var_name in func_map['global']['vars'].keys():
        err('variable ' + var_name + ' already declared globally', func_name) # var already declared globally
    else:
        if (value == None): # empty declaration gives empty value
            value = empty_values[type]
        # insert into vars map
        func_map[func_name]['vars'][var_name] = { 
            'type': type,
            'value': value,
            'memory_index': memory.local_memory.push(type, value),
        }

def _insert_global_var(global_var_name, type, value=None):
    # Insert global variable in function_map
    if global_var_name in func_map['global']['vars'].keys():
        err('variable already declared globally', global_var_name)
    else:
        if (value == None):
            value = empty_values[type]
        func_map['global']['vars'][global_var_name] = {
            'type': type,
            'value': value,
            'memory_index' : memory.global_memory.push(type, value),
        }

def insert_var(scope, var_name, type=None, value=None):
    if scope == "global":
        _insert_global_var(var_name, type, value)
    else:
        _insert_local_var(scope, var_name, type, value)


def insert_param(func_name, param_name, param_type):
    # append param to a function
    func_map[func_name]['params'].append((param_name, param_type))



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

