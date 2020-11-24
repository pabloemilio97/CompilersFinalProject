import shared_vm

def print_func(value):
    # for now this will only print in terminal, but it should add it somewhere and return request with it
    print("Wrote: ", value)
    shared_vm.output.append(f'Compilords >> {value}')
