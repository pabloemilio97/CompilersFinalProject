from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
import grammar
import shared_vm
import shared
import symbol_table

app = Flask(__name__)
CORS(app)

def clean_all():
    symbol_table.func_map = {
        'constants': {}
    }
    shared.scope = 'global'
    shared.assign_to = ''
    shared.current_declaration_type = ''
    shared.expression_stack = [[]]
    shared.param_nums_stack = []
    shared.function_call_names_stack = []
    shared.quadruples = []
    shared.quadruples_address = []
    shared.operands_stack = []
    shared.operations_stack = []
    shared.jump_stack = []
    shared_vm.instruction_pointer = 0
    shared_vm.call_stack = []
    shared_vm.preparing_state = None
    shared_vm.output = []

def print_all():
    print(shared.scope)
    print(shared.assign_to)
    print(symbol_table.func_map)
    print(shared.current_declaration_type)
    print(shared.expression_stack)
    print(shared.param_nums_stack)
    print(shared.function_call_names_stack)
    print(shared.quadruples)
    print(shared.quadruples_address)
    print(shared.operands_stack)
    print(shared.operations_stack)
    print(shared.jump_stack)
    print(shared_vm.instruction_pointer)
    print(shared_vm.call_stack)
    print(shared_vm.preparing_state)
    print(shared_vm.output)


@app.route("/")
def home():
    print('Entered Home')
    response = "this is response"
    return jsonify(response)


@app.route('/compile', methods=['POST'])
def compile():

    code = request.get_json()


    mobile_code_file = open('mobile_code.ap', 'w')
    mobile_code_file.write(code)
    mobile_code_file.close()

    try:
        grammar.comp_and_run('mobile_code.ap')
    except ValueError as error:
        pass

    output = shared_vm.output
    # clean everything before compiling again
    clean_all()
    return jsonify(output)
