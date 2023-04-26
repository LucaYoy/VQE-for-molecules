import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
import plots
from qiskit import IBMQ
import pickle
import time

sym = ['H','O','H']
r = 0.96
phi = 104.5
coord = np.array([[-r*np.sin(phi/2),r*np.cos(phi/2),0],[0,0,0],[r*np.sin(phi/2),r*np.cos(phi/2),0]])
H,qb = qml.qchem.molecular_hamiltonian(sym,coord,active_electrons=4,active_orbitals=4)
print(qb,H)
Hmatrix = qml.matrix(H)
#print(Hmatrix)

layers = 5
theta = 2*np.pi*np.random.rand((layers+1)*2*qb)
c = 0.05*2*np.pi
eta = 0.8
shots = 8192
iterations = 20

dev1 = qml.device("default.qubit", wires=qb)
circuitSim = qc.QuantumCircuit(dev1,H)
energy_listSimSOGD = circuitSim.optimize(theta, c, eta, shots, iterations, method='SOGD')
plots.plotOptimisation(Hmatrix, [], energy_listSimSOGD, [], [], iterations, layers,i='HOH_phi=104.5')
