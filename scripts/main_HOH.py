import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
import plots
from qiskit import IBMQ
import pickle
import time

with open(f'../pklFiles/H2O/optimalParams_HOH','rb') as f:
	optimal = pickle.load(f)


sym = ['H','O','H']
r, phi = optimal
phis = (np.pi/180)*np.array(range(5,185,5))
rs = 0.1*np.array(range(1,37))
coord = np.array([[-r*np.sin(phi/2),r*np.cos(phi/2),0],[0,0,0],[r*np.sin(phi/2),r*np.cos(phi/2),0]])
H,qb = qml.qchem.molecular_hamiltonian(sym,coord,active_electrons=4,active_orbitals=4)
#print(qb,H)
Hmatrix = qml.matrix(H)
# print(Hmatrix)

layers = 1
theta = 2*np.pi*np.random.rand((layers+1)*2*qb)
c = 0.05*2*np.pi
eta = 0.8
shots = 8192
iterations = 100
with open(f'../pklFiles/H2O/exactEArray_HOH_phi','rb') as f:
	exactEArray = pickle.load(f)

with open(f'../pklFiles/H2O/energy_listSimFOGD_phi={phi}_layers={layers}_iteration={iterations}','rb') as f:
	energy_listSimFOGD = pickle.load(f)
with open(f'../pklFiles/H2O/energy_listSimSOGD_phi={phi}_layers={layers}_iteration={iterations}','rb') as f:
	energy_listSimSOGD = pickle.load(f)
with open(f'../pklFiles/H2O/energy_listSimSPSA_phi={phi}_layers={layers}_iteration={iterations}','rb') as f:
	energy_listSimSPSA = pickle.load(f)
with open(f'../pklFiles/H2O/energy_listSimPS_phi={phi}_layers={layers}_iteration={iterations}','rb') as f:
	energy_listSimPS = pickle.load(f)

plots.plotOptimisation(Hmatrix, energy_listSimFOGD, energy_listSimSOGD, energy_listSimPS, energy_listSimSPSA, iterations, layers,i='_HOH_phi=1.75')

approxESim = []
for phi in phis:
	with open(f'../pklFiles/H2O/energy_listSimPS_phi={phi}_layers={layers}_iteration={iterations}','rb') as f:
		energy_listSim = pickle.load(f)
	approxESim.append(energy_listSim[-1])
  
plots.plotEAgainstR(phis, exactEArray, approxESim, layers, 'PS')