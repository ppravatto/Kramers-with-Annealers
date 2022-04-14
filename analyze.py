import sys, os
import matplotlib.pyplot as plt

plt.rc('font', **{'size':20})

if __name__ == "__main__":

    if "-h" in sys.argv or "--help" in sys.argv :
        print("Kramers with Annealers analysis script ver. 1.0")
        print("-----------------------------------------------------------------")
        print("Syntax:")
        print("   python3 analyze.py <data> [... arguments ...]")
        print("")
        print("Required arguments:")
        print("    <data>: output obtained from running the engine.py script")
        print("")
        print("Optional arguments:")
        print("    <reference>: eigenvalue list obtained from the")
        print("                 Smoluchowski-Rotor-Chain software")
        print("-----------------------------------------------------------------")
    elif len(sys.argv) == 1 or len(sys.argv) > 3:
        print("ERROR: 1 or 2 arguments expected, {} arguments given".format(len(sys.argv)-1))
        print("""Use '-h' or '--help' for the list of arguents""")
        exit()

    filename = sys.argv[1]

    if os.path.isfile(filename) == False:
        print("ERROR: '{}' file not found")
        exit()

    data = []    
    with open(filename, 'r') as file:
        for line in file:
            data.append(float(line))
    
    fig = plt.figure(figsize=(10, 10))

    bins, _, _ = plt.hist(data, bins=100, orientation='horizontal')
    plt.xlabel("Number of runs", size=24)
    plt.ylabel("Eigenvalue estimate", size=24)

    if len(sys.argv) > 2:

        if os.path.isfile(sys.argv[2]) == False:
            print("ERROR: '{}' file not found")
            exit()

        with open(sys.argv[2], 'r') as file:
            lines = file.readlines()
            reference = float(lines[1].split()[-1])
        
        plt.hlines(reference, 0, max(bins), colors='black', linestyles='--')

    plt.tight_layout()
    plt.show()



    