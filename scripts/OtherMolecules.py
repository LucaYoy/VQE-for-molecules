import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
import plots
from qiskit import IBMQ
import pickle
import time

sym = ['He','H']
coord = np.array([[0,0,-0.85],[0,0,0.85]])

H,qb = qml.qchem.molecular_hamiltonian(sym,coord,active_orbitals=2,active_electrons=2)

print(qb,H)
print(qml.matrix(H))
