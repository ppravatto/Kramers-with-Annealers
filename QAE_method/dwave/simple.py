import sys, os, dimod
import numpy as np
import matplotlib.pyplot as plt

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

from QAE_method import *


# Set here your D-Wave credentials
ENDPOINT = ""
TOKEN = ""
DEVICE = ""


#Define a custom QAE function to run a QAE iteration with a defined lambda value (lam) returning the full sampling set
def dwave_QAE(Hamiltonian, K, lam, sampler, sampler_params):

    bqm = get_QAE_bqm(Hamiltonian, K, lam)
    response = sampler.sample(bqm, **sampler_params)
    solutions = pd.DataFrame(response.data())

    return solutions['energy'], solutions['sample']



if __name__ == "__main__":

    K = 5
    shots = 10000
    lambda_max = 3

    qpu = DWaveSampler(endpoint=ENDPOINT, token=TOKEN, solver=DEVICE)
    sampler = EmbeddingComposite(qpu)
    params = {'num_reads': shots}

    scan_data = [[], []]
    for idx, LAM in enumerate(np.linspace(0, lambda_max, 101)):

        H = load_hamiltonian_matrix("hamiltonian.txt")
        
        
        QA_energies, QA_solutions = dwave_QAE(H, K, LAM, sampler, sampler_params=params)

        with open("lambda_{}.txt".format(idx), 'w') as file:
            file.write("#{}\n".format(LAM))
            for QAS in QA_solutions:
                WFNC = get_coefficients(QAS, K)
                energy = compute_energy(H, WFNC)
                file.write("{:.12f}\n".format(energy))

        index = int(QA_energies.idxmin())
        annealing_energy = QA_energies[index]
        annealing_solution = QA_solutions[index]

        wfn_coeff = get_coefficients(annealing_solution, K)
        energy = compute_energy(H, wfn_coeff)

        scan_data[0].append(LAM)
        scan_data[1].append(energy)
        print(" Lambda: {:.3f}, functional: {:.5f}, sq_norm: {:.3e}, energy: {:.10f}".format(LAM, annealing_energy, sq_norm(wfn_coeff), energy))

    min_energy = min(scan_data[1])
    print("--------------------------------------------------------------------------------")
    print(" Minumum energy {:.15f}".format(min_energy))

    fig = plt.figure(figsize=(10, 8))

    plt.plot(scan_data[0], scan_data[1])
    plt.xlabel(r"$\lambda$", size=24)
    plt.ylabel("Energy", size=24)

    plt.tight_layout()
    plt.savefig("scan_K{}_s{}.png".format(K, shots), dpi=600)
    plt.show()
            
