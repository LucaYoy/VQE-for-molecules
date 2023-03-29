import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
import plots
from qiskit import IBMQ

R = 90
layers = 1
theta = 2*np.pi*np.random.rand((layers+1)*4)
c = 0.05*2*np.pi
eta = 0.8
shots = 8192
iterations = 50
RRange = [50,250]
parameters = np.loadtxt("HamiltonianParameters.txt")
RArray = parameters[int(RRange[0]/5-1):int(RRange[1]/5),0]

exactEArray = [ex.exactEnergy(R) for R in RArray]

dev1 = qml.device("default.qubit", wires=2)
circuitSim = qc.QuantumCircuit(dev1)

# dev2 = qml.device('qiskit.ibmq',wires=2,shots=shots,backend='ibmq_quito')
# circuitReal = qc.QuantumCircuit(dev2)
# energy_listRe, iterationsRe = circuitReal.optimize(R,theta,c,eta,shots,0.001)

# circuitSim.plotCircuit(theta)
energy_listSimFOGD = circuitSim.optimize(R,theta,c,eta,shots,iterations,method='FOGD')
energy_listSimSOGD = circuitSim.optimize(R,theta,c,eta,shots,iterations,method='SOGD')
energy_listSimPS = circuitSim.optimize(R,theta,c,eta,shots,iterations,method='PS')
energy_listSimSPSA = circuitSim.optimize(R,theta,0.2,eta,shots,iterations,method='SPSA')
plots.plotOptimisation(R,energy_listSimFOGD,energy_listSimSOGD,energy_listSimPS,energy_listSimSPSA,iterations,layers,i='Eta0.8')

#approxESim = [circuitSim.optimize(R, theta, c, eta, shots, iterations,method='PS')[-1] for R in RArray]
#plots.plotEAgainstR(RArray,exactEArray,approxESim,layers,method='PS')

'''maxLayers = 5
nrOfparamList = range(8,(maxLayers+1)*4+1,4)
exactE = ex.exactEnergy(R)
approxEArray = [circuitSim.optimize(R, 2*np.pi*np.random.rand(i), c, eta, shots, iterations,method='SOGD')[-1] for i in nrOfparamList]
plots.plotDeltaE_layers(R, approxEArray, exactE,method='SPSA')
'''