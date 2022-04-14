# Kramers with Annealers

This repository contains code to calculate the first non-vanishing eigenvalue of the Fokker-Planck-Smoluchowski operator, associated with a symmetric bistable system, using a quantum annealer.

The software employs a binary mapping to encode the basis-set. Once the Pauli decomposition of the operator has been obtained the XBK method ([R. Xia et al, J. Phys. Chem. B, (2018), 122, 13, 3384–3395](https://doi.org/10.1021/acs.jpcb.7b10371)) is used to map the problem onto the quantum annealer.

The code employed is largely adapted from the original implementation "[Quantum-Chemistry-with-Annealers](https://github.com/jcopenh/Quantum-Chemistry-with-Annealers)" by J.Copenhaver, associated with the paper [J. Copenhaver et al, J. Chem. Phys., 154, 034105 (2021)](https://doi.org/10.1063/5.0030397).

The relation existing between the Fokker-Planck-Smoluchowski operator and the quantum Hamiltonian is discussed, concerning its quantum computational applications, in the paper [Pierpaolo Pravatto et al, New J. Phys., (2021), 23 123045](https://doi.org/10.1088/1367-2630/ac3ff9).


### Requirements

* [numpy](https://github.com/numpy/numpy )
* [symengine](https://github.com/symengine/symengine.py)
* [openfermion 0.11.0](https://github.com/quantumlib/OpenFermion/tree/02a0088347c31ad3b6b73db18bc598ef6ddb923a)
* [dwave-ocean-sdk](https://github.com/dwavesystems/dwave-ocean-sdk)
* [joblib](https://github.com/joblib/joblib) (only required by the `engine.py` script)

We strongly advise the user to install all the required dependencies and run the scripts using a virtual environment like [anaconda3](https://www.anaconda.com/).

### Running a calculation

The `engine.py` script allows the user to run multiple annealing simulations. The basic syntax is:
```
python3 engine.py <hamiltonian> <rvalue> <samples>
```
where `<hamiltonian>` is the text file containing the "hamiltonian" matrix, `<rvalue>` represents the value of `r` to be used in the XBK method, while `<samples>` represents the number of independent simulations to accumulate. The program will output a `stat_r<rvalue>.txt` containing the eigenvalues computed by the independent annealing runs.

An updated list of commands accepted by the `engine.py` can be printed using the `-h` or `--help` flags.
