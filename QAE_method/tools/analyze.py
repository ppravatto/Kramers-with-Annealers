import os
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec
import numpy as np

plt.rc('font', **{'size':22})
plt.rcParams.update({"text.usetex": True, "font.family": "serif"})

if __name__ == "__main__":

    root = "lambda"
    steps = 79
    bins = 100

    REF = None

    LAMBDA, ENERGY, SQNORM = [], [], []
    for idx in range(steps):
        filename = "{}_{}.txt".format(root, idx)
        buffer = [[],[]]
        if os.path.isfile(filename) == True:
            with open(filename, 'r') as file:
                LAMBDA.append(float(file.readline().strip('#')))
                for line in file:
                    sline = line.split()
                    buffer[0].append(float(sline[0]))
                    buffer[1].append(float(sline[1]))
                ENERGY.append(buffer[0])
                SQNORM.append(buffer[1])
        else:
            print("ERROR: file '{}' not found".format(filename))
            exit()
        
    
    MIN_E_STEP, MIN_SQNORM_STEP = [], []
    MaxE, MinE = max(ENERGY[0]), min(ENERGY[0])
    for lenergy, lsqnorm in zip(ENERGY, SQNORM):
        min_lenergy, min_lsqnorm = min(zip(lenergy, lsqnorm), key=lambda x: x[0])
        MIN_E_STEP.append(min_lenergy)
        MIN_SQNORM_STEP.append(min_lsqnorm)
        MaxE = max(MaxE, max(lenergy))
        MinE = min(MinE, min(lenergy))
    
    print("Minimum energy: {}".format(MinE))

    BINS, FREQ = None, []
    for values in ENERGY:
        freq, BINS = np.histogram(values, bins=bins, range=(MinE, MaxE))
        FREQ.append(freq)
    
    dL = LAMBDA[1]-LAMBDA[0]
    I_LAMBDA = [LAMBDA[0] -0.5*dL + n*dL for n in range(len(LAMBDA)+1)]

    TR_FREQ = list(map(list, zip(*FREQ)))

    gs = gridspec.GridSpec(2, 2, height_ratios=[2, 1])

    fig = pl.figure(figsize=(13, 10))

    ax1 = pl.subplot(gs[0, :])
    pcmesh = ax1.pcolormesh(I_LAMBDA, BINS, TR_FREQ, cmap="Blues")
    cbar = plt.colorbar(pcmesh, ax=ax1)
    cbar.set_label("Number of samples", rotation=90)

    ax1.plot(LAMBDA, MIN_E_STEP, c="#bf00bf", label="Minimum")
    
    ax1.set_xlabel(r"$\lambda$", size=24)
    ax1.set_ylabel(r"$\lambda_1$", size=24)
    ax1.legend()

    ax2 = pl.subplot(gs[1, 0])
    ax2.plot(LAMBDA, MIN_E_STEP, c="#bf00bf", label="Minimum")
    ax2.plot([LAMBDA[0], LAMBDA[-1]], [REF, REF], c="red", linestyle="--", label="Theoretical")
    ax2.set_xlabel(r"$\lambda$", size=24)
    ax2.set_ylabel(r"$\lambda_1$", size=24, c="#bf00bf")
    ax2.tick_params(axis='y', labelcolor="#bf00bf")
    ax2.grid(which="major", c="#DDDDDD")
    ax2.grid(which="minor", c="#EEEEEE")

    ax2b = ax2.twinx()
    ax2b.plot(LAMBDA, MIN_SQNORM_STEP, c="green", label="Norm minimum")
    ax2b.tick_params(axis='y', labelcolor="green")
    ax2b.set_ylabel(r"$|| \Psi ||$", size=24, c="green")

    ax3 = pl.subplot(gs[1, 1])
    for Lambda, Energy, Norm in zip(LAMBDA, ENERGY, SQNORM):
        ax3.scatter(Norm, Energy, s=4, c="blue", alpha=0.15, edgecolors=None)
    ax3.set_xscale('log')
    ax3.set_xlabel(r"$|| \Psi ||$", size=24)
    ax3.set_ylabel(r"$\lambda_1$", size=24)
    ax3.grid(which="major", c="#DDDDDD")
    ax3.grid(which="minor", c="#EEEEEE")
    

    plt.tight_layout()
    plt.savefig("QAE_output.png", dpi=1200)
    plt.show()
  