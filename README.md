# VQE-For-Molecules
Exploring VQE approximations for ground states of chemical molecules; specifically the He-H+ and H2O molecules. I carry out different variants of gradient descent and compare their performance on convergence. I then look into how well VQE can approximate the energy curve as a function of the molecules geometry.
## Procedure 
* Find the exact ground state through exact diagonalization on the molecular hamiltonian
* Set up the quantum circuit approximation which contains multiple layers, made up of rotation gates, seperated by cointrol Z gates.
* Carry out optimization on the energy of the output state of the circuit in order to find the minimum energy
* Test different gradient descent methods
* Run the algorithm both as a simulation and on IBM quantum computers
* change the geometry of the molecule and find the minimum energy for different geometries
* Plot the results and analyze them
## Tech stack
* Vanilla Python
* Numpy
* Matplotlib
* Pennylane
* Google Collab
* IBM Quantum 
* Linux scripting
* Augusta HPC
