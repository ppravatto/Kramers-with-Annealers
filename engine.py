import sys, os
from time import time
from openfermion.utils import count_qubits
from joblib import Parallel, delayed
from neal import SimulatedAnnealingSampler

from helper_functions import *
from binary_mapping import *
from XBK_method import *



def annealing_run(qubit_Hamiltonian, sampler, r):
    
    m = count_qubits(qubit_Hamiltonian)
    qubit_Hs, qubit_Cs = [],[]
    for p in range(int(math.ceil(r/2+1))):
        qubit_Hs += [XBK_transform(qubit_Hamiltonian, r, p)]
        qubit_Cs += [construct_C(m, r, p)]

    XBK_energy, ground_state = XBK(qubit_Hs, qubit_Cs, r, sampler, starting_lam=2, num_samples=1000, strength=1e3, verbose=False)

    return XBK_energy
        



if __name__ == "__main__":

    if "-h" in sys.argv or "--help" in sys.argv :
        print("Kramers with Annealers engine ver. 1.0")
        print("-----------------------------------------------------------------")
        print("Basic syntax:")
        print("   python3 engine.py <hamiltonian> <rvalue> <samples>")
        print("")
        print("Arguments:")
        print("    <hamiltonian>: text-file containing the hamiltonian matrix")
        print("    <rvalue>: value of r to be used in the XBK mapping")
        print("    <samples>: number of independent simulations to accumulate")
        print("-----------------------------------------------------------------")
        exit()
    elif len(sys.argv) != 4:
        print("ERROR: 3 arguments expected, {} arguments given".format(len(sys.argv)-1))
        print("""Use '-h' or '--help' for the list of required arguents""")
        exit()
    
    
    filename = sys.argv[1]
    if os.path.isfile(filename) == False:
        print("ERROR: {} file not found".format(filename))
        exit()

    raw_qubit_H = get_binary_Hamiltonian(filename)
    qubit_H = to_QubitOperator(raw_qubit_H)

    r = int(sys.argv[2])
    N_runs = int(sys.argv[3])
    sampler = SimulatedAnnealingSampler()

    t_start = time()
    data = Parallel(n_jobs=-1)(delayed(annealing_run)(qubit_H, sampler, r) for i in range(N_runs))
    t_end = time()

    with open("stat_r{}.txt".format(r), 'w') as file:
        for value in data:
            file.write("{:.12f}\n".format(value))
    
    print("JOB TERMINATED NORMALLY")
    print("Parallel runtime: {:.2f}s".format(t_end-t_start))

