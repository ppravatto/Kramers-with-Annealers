import sys, os
import numpy as np
from time import time
from openfermion.utils import count_qubits
from joblib import Parallel, delayed

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

from helper_functions import *
from binary_mapping import *
from XBK_method import *

# Set here your D-Wave credentials
ENDPOINT = ""
TOKEN = ""
DEVICE = ""


def annealing_run(qubit_Hamiltonian, sampler, r, sampler_params=SP_DEFAULT):
    
    m = count_qubits(qubit_Hamiltonian)
    qubit_Hs, qubit_Cs = [],[]
    for p in range(int(math.ceil(r/2+1))):
        qubit_Hs += [XBK_transform(qubit_Hamiltonian, r, p)]
        qubit_Cs += [construct_C(m, r, p)]

    XBK_energy, ground_state = XBK(qubit_Hs, qubit_Cs, r, sampler, sampler_params=sampler_params, starting_lam=2, strength=1e3, verbose=False)

    return XBK_energy
        



if __name__ == "__main__":

    raw_qubit_H = get_binary_Hamiltonian("hamiltonian.txt")
    qubit_H = to_QubitOperator(raw_qubit_H)

    r = 8
    at_steps = 20

    number_of_sets = 20
    run_per_set = 500

    qpu = DWaveSampler(endpoint=ENDPOINT, token=TOKEN, solver=DEVICE)
    sampler = EmbeddingComposite(qpu)

    at_range = qpu.properties["annealing_time_range"]

    with open("annealing_time_scan_{}.txt".format(r), 'w') as file:
        for at in np.linspace(at_range[0], at_range[1], at_steps):
            print("Annealing time: {}us".format(at))
            value = None
            params = {'num_reads': run_per_set, 'annealing_time': at}
            for set in range(0, number_of_sets):
                minval = annealing_run(qubit_H, sampler, r, sampler_params=params)
                print(" --> Set {}: {:.10f}".format(set, minval))
                value = minval if value==None else min(value, minval)

            print("Minumum value: {:.12f}\n".format(value))
            file.write("{:.12f}\t{:.12f}\n".format(at, value))
            

