import numpy as np
import os

from helper_functions import *



def get_bin_list(number, register_length, invert=False):
    string = "{0:b}".format(number)
    buffer = [int(i) for i in string]
    buffer = buffer[::-1]
    while len(buffer)<register_length:
        buffer.append(0)
    if invert == True:
        buffer = buffer[::-1]
    return buffer


def get_pauli_string(row_bin, col_bin, term_bin):
    coeff = complex(1, 0)
    pauli_string = ""
    for i, select in enumerate(term_bin):
        coeff *= 0.5
        if row_bin[i] == col_bin[i]:
            if select == 0:
                pauli_string += "I"
            else:
                pauli_string += "Z"
                coeff *= (-1)**row_bin[i]
        else:
            if select == 0:
                pauli_string += "X"
            else:
                pauli_string += "Y"
                coeff *= complex(0, 1) * (-1)**row_bin[i]
    return pauli_string, coeff


def get_binary_Hamiltonian(filename, threshold=0):
    nqubits = 0
    Hamiltonian = {}
    if os.path.isfile(filename) == True:
        with open(filename, 'r') as myfile:
            for row, line in enumerate(myfile):
                myline = line.split()
                if row==0:
                    nqubits = int(np.ceil(np.log2(len(myline))))
                for col, integral in enumerate(myline):
                    if np.abs(float(integral)) > threshold:
                        row_bin = get_bin_list(row, nqubits)
                        col_bin = get_bin_list(col, nqubits)
                        for term in range(2**nqubits):
                            term_bin = get_bin_list(term, nqubits)
                            pauli_string, coeff = get_pauli_string(row_bin, col_bin, term_bin)
                            if pauli_string not in Hamiltonian:
                                Hamiltonian[pauli_string] = coeff*float(integral)
                            else:
                                Hamiltonian[pauli_string] += coeff*float(integral)
    else:
        print("""ERROR: '{}' file not found\n""".format(filename))
        exit()

    return Hamiltonian
    