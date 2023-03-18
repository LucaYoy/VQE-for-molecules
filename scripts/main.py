import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
import plots
from qiskit import IBMQ

R = 90
theta = 2*np.pi*np.random.rand(8)
c = 0.05*2*np.pi
eta = 0.5
shots = 8192

dev1 = qml.device("default.qubit", wires=2)
dev2 = qml.device('qiskit.ibmq',wires=2,shots=shots,backend='ibmq_quito')

# circuitSimulation = qc.QuantumCircuit(dev1)
# energy_listSim, iterationsSim = circuitSimulation.optimize(R,theta,c,eta,shots,0.001)

circuitReal = qc.QuantumCircuit(dev2)
energy_listRe, iterationsRe = circuitReal.optimize(R,theta,c,eta,shots,0.001)

# plots
plots.plotOptimisation(R,energy_list,iterations)
#plots.plotEAgainstR(theta, c, eta, shots,[50,250] ,0.001)