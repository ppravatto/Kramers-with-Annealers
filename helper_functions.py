import symengine as se
from openfermion.ops import QubitOperator

'''
Helper functions for Binary mapping script
'''

#Convert Pauli string dictionary to OpenFermion qubit operator
def to_QubitOperator(PauliStrings):
    hamiltonian = 0
    for string, coeff in PauliStrings.items():
        lstring = ""
        for idx, operation in enumerate(string):
            if operation == "I":
                continue
            lstring += "{}{} ".format(operation, idx)
        hamiltonian += coeff * QubitOperator(lstring) if lstring != "" else coeff
    return hamiltonian


'''
Helper functions for XBK method
'''

#Convert dictionary from OpenFermion form to dimod form
def convert_dict(dictionary):
    new_dict = {}
    for key in dictionary:
        var_list = []
        for var in key:
            var_list += ['s'+str(var[0])]
        var_list = tuple(var_list)
        
        new_dict[var_list] = dictionary[key]
    return new_dict



#Convert a dimod dictionary into a function using symengine
def dict_to_func(dictionary):
    expr = 0
    for key in dictionary:
        term = dictionary[key]
        for var in key:
            term *= se.Symbol(var)
        expr += term
    
    if type(expr) == float:
        f = expr
    else:
        var_list = list(expr.free_symbols)
        var_list.sort(key = lambda variable: int(str(variable)[1:]))
        f = se.lambdify(var_list, (expr,))
    return f
