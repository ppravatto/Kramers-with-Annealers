import sys, os
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font', **{'size':20})

if __name__ == "__main__":

    if "-h" in sys.argv or "--help" in sys.argv :
        print("Kramers with Annealers multi-analysis script ver. 1.0")
        print("-----------------------------------------------------------------------")
        print("Syntax:")
        print("   python3 multianalyze.py <root> <bins> <reference>")
        print("")
        print("Required arguments:")
        print("       <root>: root of the files obtained from the engine.py script")
        print("                 each file must be named <root><r>.txt with <r> integer")
        print("       <bins>: number of bins to use for the plot")
        print("  <reference>: eigenvalue list obtained from the")
        print("                 Smoluchowski-Rotor-Chain software")
        print("-----------------------------------------------------------------------")
    elif len(sys.argv) !=4 :
        print("ERROR: 3 arguments expected, {} arguments given".format(len(sys.argv)-1))
        print("""Use '-h' or '--help' for the list of arguents""")
        exit()

    root = sys.argv[1]
    nbins = int(sys.argv[2])
    eiglist = sys.argv[3]

    data = [[], []]

    for filename in os.listdir(os.getcwd()):
        if filename.startswith(root):
            
            values = []    
            with open(filename, 'r') as file:
                for line in file:
                    values.append(float(line))
            
            data[0].append(int(filename.split("r")[-1].strip(".txt")))
            data[1].append(values)

    rsorted = np.sort(data[0])
    
    with open(eiglist, 'r') as file:
            lines = file.readlines()
            reference = float(lines[1].split()[-1])
    
    top, bottom = reference, reference
    for list in data[1]:
        maxval, minval = max(list), min(list)
        top, bottom = max(maxval, top), min(minval, bottom)

    deltax = (top-bottom)/nbins
    
    fig, axs = plt.subplots(figsize=(16, 10), ncols=len(data[0]))
    for i, ax in enumerate(axs):
        
        idx = data[0].index(rsorted[i])

        bins, _, _ = ax.hist(data[1][idx], bins=np.linspace(bottom, top, nbins+1), orientation='horizontal') 
        maxh = ax.get_xlim()[-1]
        ax.hlines(reference, 0, maxh, colors='red', linestyles='--')
        ax.set_xlim((0, maxh))
        if i!=0:
            ax.axes.yaxis.set_ticklabels([])
        ax.set_title("r = {}".format(rsorted[i]))


    plt.tight_layout()
    plt.savefig("scan_{}.png".format(root.split("_")[0]), dpi=600)
    plt.show()



    