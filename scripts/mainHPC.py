import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
import pickle
import time
import sys

#sh file array 0-143
which = int(sys.argv[1])
parameters = []
phis = (np.pi/180)*np.array(range(5,185,5))
#rs = 0.1*np.array(range(1,37))
for phi in phis:
	for method in ['FOGD','SOGD','SPSA','PS']:
		parameters.append({'phi':phi,'method':method})
params = parameters[which]

sym = ['H','O','H']
r = 1.9
#phi = 1.75
phi, method = params['phi'],params['method']
coord = np.array([[-r*np.sin(phi/2),r*np.cos(phi/2),0],[0,0,0],[r*np.sin(phi/2),r*np.cos(phi/2),0]])
H,qb = qml.qchem.molecular_hamiltonian(sym,coord,active_electrons=4,active_orbitals=4)
Hmatrix = qml.matrix(H)
#print(Hmatrix)

layers = 8
theta = 2*np.pi*np.random.rand((layers+1)*2*qb)
c = 0.05*2*np.pi
eta = 0.8
shots = 8192
iterations = 40

dev1 = qml.device("default.qubit", wires=qb)
circuitSim = qc.QuantumCircuit(dev1,H)
t1 = time.time()
energy_listSim = circuitSim.optimize(theta, c, eta, shots, iterations, method=method)
t2 = time.time()
print(t2-t1)

with open(f'energy_listSim{method}_phi={phi}_layers={layers}_iteration={iterations}','wb') as f:
	pickle.dump(energy_listSim, f)


