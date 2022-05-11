import os, dimod
import numpy as np
import pandas as pd

#Define a default value for the sampler parameters
SP_DEFAULT = {'num_reads': 10000}


#Define a function to make sure that the key is not already present in the dictionary [DEBUG ONLY]
def dict_sanity_check(dict, key):
    if key in dict.keys():
        print("ERROR: overwriting dictionary entry")
        exit()


#Define a function to load the hamiltonian matrix of the problem
def load_hamiltonian_matrix(filename):
    if os.path.isfile(filename) == False:
        print("""ERROR: '{}' file not found\n""".format(filename))
        exit()

    H = np.loadtxt(filename, dtype=float)
    return H


#Define a function to generate the bqm expression for a QAE iteration with a defined lambda value (lam)
def get_QAE_bqm(Hamiltonian, K, lam):
    
    linear, quadratic = {}, {}
    for r, line in enumerate(Hamiltonian):
        for c, h in enumerate(line):
            F = h-lam if r==c else h
            for i in range(1, K+1):
                c_i = -1 if i==K else 2**(i-K)
                q_i = K*r + i
                for j in range(i, K+1):
                    c_j = -1 if j==K else 2**(j-K)
                    q_j = K*c + j
                    if q_i == q_j:
                        dict_sanity_check(linear, q_i)              #For debug only
                        linear[q_i] = F*c_i*c_j
                    else:
                        dict_sanity_check(quadratic, (q_i, q_j))    #For debug only
                        quadratic[(q_i, q_j)] = 2*F*c_i*c_j   

    bqm = dimod.BinaryQuadraticModel(linear, quadratic, dimod.BINARY)

    return bqm


#Define a function to run a QAE iteration with a defined lambda value (lam)
def QAE(Hamiltonian, K, lam, sampler, sampler_params=SP_DEFAULT):

    bqm = get_QAE_bqm(Hamiltonian, K, lam)
    
    response = sampler.sample(bqm, **sampler_params)
    solutions = pd.DataFrame(response.data())

    index = int(solutions[['energy']].idxmin())
    min_energy = solutions['energy'][index]
    full_solution = solutions['sample'][index]

    return min_energy, full_solution


#Define a function to obtain the solution coefficients from a given annealing solution
def get_coefficients(solution, K):
    coeff = []
    N = int(len(solution)/K)

    for n in range(N):
        C = 0
        for k in range(1, K+1):
            c_k = -1 if k==K else 2**(k-K)
            q_k = K*n + k
            C += c_k*solution[q_k]
        coeff.append(C)
    
    return coeff


#Define a function to compute the squard norm of a coefficient set
def sq_norm(coefficients):
    norm = 0
    for c in coefficients:
        norm += np.abs(c)**2
    return norm


#Define a function to normalize the coefficients obtained form the quantum annealing
def sq_normalize(coefficients):
    norm = sq_norm(coefficients) 
    return [c/np.sqrt(norm) for c in coefficients]


#Define a function to compute the energy correspondent to a given coefficient set
def compute_energy(Hamiltonian, coefficients, normalize=True):
    energy = 0

    coeff = coefficients if normalize==False else sq_normalize(coefficients)

    for r, line in enumerate(Hamiltonian):
        for c, h in enumerate(line):
            energy += h*coeff[r]*coeff[c]
    
    return energy
    
    