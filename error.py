import sys
import shared_vm


def err(msg, var):
    error_output = 'ERROR: ' + msg + ' => ' + var
    print(error_output)
    shared_vm.output.append(f'Whale >> COMPILATION ERROR \n{error_output}')
    sys.exit()

def gen_err(msg):
    print(msg)
    shared_vm.output.append(f'Whale >> COMPILATION ERROR \n {msg}')
    sys.exit()


def gen_runtime_err(msg):
    print('RUNTIME ERROR')
    print(msg)
    shared_vm.output.append(f'Whale >> RUNTIME ERROR Error \n {msg}') 
    sys.exit()
