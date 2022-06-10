import os
import matplotlib.pyplot as plt
import numpy as np

plt.rc('font', **{'size':20})

if __name__ == "__main__":

    root = "lambda"
    steps = 50
    bins = 100

    LAMBDA, ENERGY = [], []
    for idx in range(steps):
        filename = "{}_{}.txt".format(root, idx)
        buffer = []
        if os.path.isfile(filename) == True:
            with open(filename, 'r') as file:
                LAMBDA.append(float(file.readline().strip('#')))
                for line in file:
                    buffer.append(float(line.split()[0]))
                ENERGY.append(buffer)
        else:
            print("ERROR: file '{}' not found".format(filename))
            exit()
    
    MINSTEP = []
    MaxE, MinE = max(ENERGY[0]), min(ENERGY[0])
    for values in ENERGY:
        MINSTEP.append(min(values))
        MaxE = max(MaxE, max(values))
        MinE = min(MinE, min(values))
    
    BINS, FREQ = None, []
    for values in ENERGY:
        freq, BINS = np.histogram(values, bins=bins, range=(MinE, MaxE))
        FREQ.append(freq)
    
    dL = LAMBDA[1]-LAMBDA[0]
    I_LAMBDA = [LAMBDA[0] -0.5*dL + n*dL for n in range(len(LAMBDA)+1)]

    TR_FREQ = list(map(list, zip(*FREQ)))

    fig = plt.figure(figsize=(10, 9))

    pcmesh = plt.pcolormesh(I_LAMBDA, BINS, TR_FREQ, cmap="Blues")

    cbar = plt.colorbar(pcmesh)
    cbar.set_label("Number of samples", rotation=90)

    plt.plot(LAMBDA, MINSTEP, c="#bf00bf", label="Mimimum")

    plt.xlabel(r"$\lambda$", size=22)
    plt.ylabel("Energy", size=22)

    plt.legend()

    plt.tight_layout()

    plt.show()


    

        
    

        