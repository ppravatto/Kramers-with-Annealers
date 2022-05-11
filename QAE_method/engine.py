import sys, os
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from neal import SimulatedAnnealingSampler

from QAE_method import *

plt.rc('font', **{'size':20})


if __name__ == "__main__":

    if "-h" in sys.argv or "--help" in sys.argv :
        print("Kramers with Annealers QAE engine ver. 1.0")
        print("-----------------------------------------------------------------")
        print("Basic syntax:")
        print("   python3 engine.py <hamiltonian> <K> <samples> <lambda-max>")
        print("")
        print("Arguments:")
        print("    <hamiltonian>: text-file containing the hamiltonian matrix")
        print("    <K>: value of K to be used in the QAE mapping")
        print("    <samples>: number of independent simulations to accumulate")
        print("    <lambda-max>: maximum value of lambda")
        print("-----------------------------------------------------------------")
        exit()
    elif len(sys.argv) != 5:
        print("ERROR: 4 arguments expected, {} arguments given".format(len(sys.argv)-1))
        print("""Use '-h' or '--help' for the list of required arguents""")
        exit()
    
    filename = sys.argv[1]
    if os.path.isfile(filename) == False:
        print("ERROR: {} file not found".format(filename))
        exit()
    
    K = int(sys.argv[2])
    N_runs = int(sys.argv[3])
    lam_max = float(sys.argv[4])

    sampler = SimulatedAnnealingSampler()

    scan_data = [[], []]
    for idx, LAM in enumerate(np.linspace(0, lam_max, 101)):

        H = load_hamiltonian_matrix(filename)

        data = Parallel(n_jobs=-1)(delayed(QAE)(H, K, LAM, sampler) for i in range(N_runs))

        QA_energies, QA_solutions = [], []
        for block in data:
            QA_energies.append(block[0])
            QA_solutions.append(block[1])
        
        with open("lambda_{}.txt".format(idx), 'w') as file:
            file.write("#{}\n".format(LAM))
            for QAS in QA_solutions:
                WFNC = get_coefficients(QAS, K)
                energy = compute_energy(H, WFNC)
                file.write("{:.12f}\n".format(energy))

        annealing_energy = min(QA_energies)
        annealing_solution = QA_solutions[QA_energies.index(annealing_energy)]

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
    plt.savefig(filename.split(".")[0]+".png", dpi=600)
    plt.show()