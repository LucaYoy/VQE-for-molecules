import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
import plots
from qiskit import IBMQ

R = 100

c = 0.05*2*np.pi
eta = 1
shots = 8192
iterations = 30
RRange = [50,250]
parameters = np.loadtxt("HamiltonianParameters.txt")
RArray = parameters[int(RRange[0]/5-1):int(RRange[1]/5),0]

exactE = [ex.exactEnergy(R) for R in RArray]

dev1 = qml.device("default.qubit", wires=2)
circuitSim = qc.QuantumCircuit(dev1)
# approxESim = [circuitSim.optimize(R, theta, c, eta, shots, iterations)[-1] for R in RArray]

# dev2 = qml.device('qiskit.ibmq',wires=2,shots=shots,backend='ibmq_quito')
# circuitReal = qc.QuantumCircuit(dev2)
# energy_listRe, iterationsRe = circuitReal.optimize(R,theta,c,eta,shots,0.001)

for i in range(10):
	theta = 2*np.pi*np.random.rand(8)
	energy_listSim = circuitSim.optimize(R,theta,c,eta,shots,iterations)
	plots.plotOptimisation(R,energy_listSim,iterations,i=i)

#plots.plotEAgainstR(RArray,exactE,approxESim)