import sys

def err(msg, var):
    error_output = 'ERROR: ' + msg + ' => ' + var
    print(error_output)

def gen_err(msg):
    print(msg)
    sys.exit()
    