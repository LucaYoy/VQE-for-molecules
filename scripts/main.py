import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
import plots

R = 90
theta = 2*np.pi*np.random.rand(8)
c = 0.05*2*np.pi
eta = 0.5
shots = 8192

energy_list, iterations = qc.optimize(R,theta,c,eta,shots,0.01)

# plots
#plots.plotOptimisation(R,energy_list,iterations)
plots.plotEAgainstR(theta, c, eta, shots, 0.01)