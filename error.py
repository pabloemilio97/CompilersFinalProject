import sys
import shared_vm
import shared


def err(msg, var):
    error_output = 'ERROR: ' + msg + ' => ' + var
    if shared.env == 'dev':
        shared_vm.output.append(f'Whale >> COMPILATION ERROR \n{error_output}')
        raise ValueError('compilation error')
    else:
        print(msg)
        sys.exit()

def gen_err(msg):
    if shared.env == 'dev':
        shared_vm.output.append(f'Whale >> COMPILATION ERROR \n {msg}')
        raise ValueError('compilation error')
    else:
        print(msg)
        sys.exit()


def gen_runtime_err(msg):
    print('RUNTIME ERROR')
    if shared.env == 'dev':
        shared_vm.output.append(f'Whale >> RUNTIME ERROR \n {msg}')
        raise ValueError('compilation error')
    else:
        print(msg)
        sys.exit()
