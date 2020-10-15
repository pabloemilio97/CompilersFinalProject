class VariableAttributes:  
    def __init__(self, type, scope):  
        self.type = type  
        self.scope = scope  


# It is forbidden to declare a variable with local scope with thscope same name as a variable present in the table
variable_table = {
    
}

def add_variable(name, type, scope):
    if name in variable_table:
        print(f"Variable {name} has already been declared")
    else:
        variable_table[name] = VariableAttributes(type, scope)

def modify_variable(name, new_value):
    if name in variable_table:
        variable_table[name] = new_value
    else:
        print(f"Variable {name} does not exist")

def delete_variable(name):
    if name in variable_table:
        variable_table.pop(name)
    else:
        print(f"Variable {name} does not exist")

def delete_variables_in_scope(scope):
    for key in variable_table:
        if variable_table[key].scope == "scope":
            delete_variable(key)
        
