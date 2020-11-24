import sys


def err(msg, var):
    error_output = 'ERROR: ' + msg + ' => ' + var
    print(error_output)


def gen_err(msg):
    print(msg)
    raise Exception
    sys.exit()


def gen_runtime_err(msg):
    print('RUNTIME ERROR')
    print(msg)
    sys.exit()
