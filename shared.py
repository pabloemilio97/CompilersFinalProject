import operator

scope = 'global'
assign_to = ''
expression_stack = [[]]
param_nums_stack = []
quadruples = []
quadruples_mem = []
operands_stack = []
operations_stack = []
jump_stack = []
jump_operations = {
    'gotoF', 'gotoT', 'goto'
}
numerics = {
    "curr_register": 0,
}
operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '&': operator.and_,
    '|': operator.or_,
}
