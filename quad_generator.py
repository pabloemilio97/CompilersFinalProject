import semantic_cube
import symbol_table

cube = semantic_cube.cube
func_map = symbol_table.func_map

quadruples = []

jump_stack = []
operand_stack = []
operator_stack = []

def quad_pos():
    return len(quadruples + 1)

def gen_quad(q1, q2, q3, q4):
    quad = [quad_pos, q1, q2, q3, q4]
    quadruples.append(quad)
