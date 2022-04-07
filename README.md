# Kramers with Annealers

This repository contains code to calculate the first non-vanishing eigenvalue of the Fokker-Planck-Smoluchowski operator, associated to a symmetric bistable system, using a quantum annealer.

The software employ a binary mapping to encode the basis-set. Once the Pauli decomposition of the operator has been obtained the XBK method ([R. Xia et al, J. Phys. Chem. B, (2018), 122, 13, 3384–3395](https://doi.org/10.1021/acs.jpcb.7b10371)) is used to map the problem onto the quantum annealer.

The code employed is largely adapted from the original implementation "[Quantum-Chemistry-with-Annealers](https://github.com/jcopenh/Quantum-Chemistry-with-Annealers)" by J.Copenhaver, associated with the paper [J. Copenhaver et al, J. Chem. Phys., 154, 034105 (2021)](https://doi.org/10.1063/5.0030397)


### Requirements
* [numpy](https://github.com/numpy/numpy )
* [symengine](https://github.com/symengine/symengine.py)
* [openfermion 0.11.0](https://github.com/quantumlib/OpenFermion/tree/02a0088347c31ad3b6b73db18bc598ef6ddb923a)
* [dwave-ocean-sdk](https://github.com/dwavesystems/dwave-ocean-sdk)

