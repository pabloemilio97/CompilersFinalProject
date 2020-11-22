import operator
from collections import deque

scope = 'global'
assign_to = ''
current_declaration_type = ''
expression_stack = [[]]
param_nums_stack = []
function_call_names_stack = []
quadruples = []
quadruples_address = []
operands_stack = []
operations_stack = []
jump_stack = []
jump_operations = {
    'gotoF', 'goto'
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
