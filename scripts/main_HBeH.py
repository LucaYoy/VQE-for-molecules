import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
import plots
from qiskit import IBMQ
import pickle
import time

sym = ['H','Be','H']
r = 1.7
phi = np.pi
phis = (np.pi/180)*np.array(range(10,370,10))
rs = 0.1*np.array(range(1,37))
# phi = phis[20]
# r = rs[9]
coord = np.array([[-r*np.sin(phi/2),r*np.cos(phi/2),0],[0,0,0],[r*np.sin(phi/2),r*np.cos(phi/2),0]])
H,qb = qml.qchem.molecular_hamiltonian(sym,coord,active_orbitals=4)
#print(qb,H)
Hmatrix = qml.matrix(H)
# print(Hmatrix)
with open(f'../pklFiles/exactEArray_HBeH_r','rb') as f:
	exactEArrayr = pickle.load(f)

layers = 5
theta = 2*np.pi*np.random.rand((layers+1)*2*qb)
c = 0.05*2*np.pi
eta = 0.8
shots = 8192
iterations = 40

# exactEArrayr = []
# for r in rs:
# 	coord = np.array([[-r*np.sin(phi/2),r*np.cos(phi/2),0],[0,0,0],[r*np.sin(phi/2),r*np.cos(phi/2),0]])
# 	H = qml.qchem.molecular_hamiltonian(sym,coord,active_orbitals=4)[0]
# 	Hmatrix = qml.matrix(H)
# 	exactEArrayr.append(ex.exactEnergy(Hmatrix))
# with open(f'../pklFiles/exactEArray_HBeH_r','wb') as f:
# 	pickle.dump(exactEArrayr, f)
# print('done')

# exactEArrayphi = []
# for phi in phis:
# 	coord = np.array([[-r*np.sin(phi/2),r*np.cos(phi/2),0],[0,0,0],[r*np.sin(phi/2),r*np.cos(phi/2),0]])
# 	H = qml.qchem.molecular_hamiltonian(sym,coord,active_orbitals=4)[0]
# 	Hmatrix = qml.matrix(H)
# 	exactEArrayphi.append(ex.exactEnergy(Hmatrix))
# with open(f'../pklFiles/exactEArray_HBeH_phi','wb') as f:
# 	pickle.dump(exactEArrayphi, f)
# print('done')

plots.plotEAgainstR(rs, exactEArrayr, [], layers, 'test')