import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
import plots
from qiskit import IBMQ
import pickle
import time

R = 90
layers = 1
theta = 2*np.pi*np.random.rand((layers+1)*4)
c = 0.05*2*np.pi
eta = 0.8
shots = 8192
iterations = 20
RRange = [50,250]
parameters = np.loadtxt("HamiltonianParameters.txt")
RArray = parameters[int(RRange[0]/5-1):int(RRange[1]/5),0]
H = ex.Hamiltonian(R)
Hmatrix = qml.matrix(H)

dev1 = qml.device("default.qubit", wires=2)
circuitSim = qc.QuantumCircuit(dev1,H)

# dev2 = qml.device('qiskit.ibmq',wires=2,shots=shots,backend='ibmq_quito')
# circuitReal = qc.QuantumCircuit(dev2)
# s = time.time()
# energy_listRe105 = circuitReal.optimize(R, theta, c, eta, shots, iterations, method='SOGD')
# e = time.time()
# with open('energy_listRe105.pkl','wb') as f:
# 	pickle.dump(energy_listRe105,f)
# print(f'took {e-s}s')

#circuitSim.plotCircuit(theta)
# energy_listSimFOGD = circuitSim.optimize(theta,c,eta,shots,iterations,method='FOGD')
# energy_listSimSOGD = circuitSim.optimize(theta,c,eta,shots,iterations,method='SOGD')
# energy_listSimPS = circuitSim.optimize(theta,c,eta,shots,iterations,method='PS')
# energy_listSimSPSA = circuitSim.optimize(theta,0.2,eta,shots,iterations,method='SPSA')
# plots.plotOptimisation(Hmatrix,energy_listSimFOGD,energy_listSimSOGD,energy_listSimPS,energy_listSimSPSA,iterations,layers,i='Eta0.8_Sim')
# #plots.plotOptimisation(Hmatrix,[],[],[],[],iterations,layers,i='Eta0.8_Sim')

with open('energy_listRe75.pkl','rb') as f:
	energy_listRe75 = pickle.load(f)

with open('energy_listRe90.pkl','rb') as f:
	energy_listRe90 = pickle.load(f)

with open('energy_listRe105.pkl','rb') as f:
	energy_listRe105 = pickle.load(f)

IBM75 = {'energyArray':energy_listRe75,'method':'SOGD'}
IBM90 = {'energyArray':energy_listRe90,'method':'SOGD'}
IBM105 = {'energyArray':energy_listRe105,'method':'SOGD'}
# plots.plotOptimisation(75,[],[],[],[],iterations,layers,IBM75,i='Eta0.8')
#plots.plotOptimisation(Hmatrix,[],[],[],[],iterations,layers,IBM90,i='Eta0.8')
# plots.plotOptimisation(105,[],[],[],[],iterations,layers,IBM105,i='Eta0.8')

exactEArray = [ex.exactEnergy(qml.matrix(ex.Hamiltonian(R))) for R in RArray]
approxESim = [qc.QuantumCircuit(dev1,ex.Hamiltonian(R)).optimize(theta, c, eta, shots, iterations,method='SOGD')[-1] for R in RArray]
approxERe = [(75,90,105),(energy_listRe75[-1],energy_listRe90[-1],energy_listRe105[-1])]
plots.plotEAgainstR(RArray,exactEArray,approxESim,layers,method='SOGD',approxE_IBM=approxERe)

# maxLayers = 5
# nrOfparamList = range(8,(maxLayers+1)*4+1,4)
# exactE = ex.exactEnergy(Hmatrix)
# approxEArray = [circuitSim.optimize(2*np.pi*np.random.rand(i), c, eta, shots, iterations,method='PS')[-1] for i in nrOfparamList]
# plots.plotDeltaE_layers(R, approxEArray, exactE,method='PS')
