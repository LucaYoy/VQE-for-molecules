import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
from matplotlib import pyplot as plt

def plotCircuit():
	qml.drawer.use_style("black_white")
	qml.draw_mpl(qc.ansatz)(list(theta)+[0,1])

def plotOptimisation(R,energy_list,iterations):
	fig, ax = plt.subplots()
	ax.plot([0,iterations],[ex.exactEnergy(R),ex.exactEnergy(R)],'--',color='k',label='Exact')
	ax.plot(energy_list,'o',label='VQE')
	ax.set(xlabel = 'iterations', ylabel = 'energy')
	ax.legend()
	plt.show()

def plotEAgainstR(theta,c,eta,shots,minChange):
	parameters = np.loadtxt("HamiltonianParameters.txt")
	RArray = parameters[10:30,0]
	exactE = [ex.exactEnergy(R) for R in RArray]
	approxE = [qc.optimize(R, theta, c, eta, shots, minChange)[0][-1] for R in RArray]

	fig, ax = plt.subplots()
	ax.plot(RArray,exactE,'k-',label='Exact')
	ax.plot(RArray,approxE,'x-',label='VQE')
	ax.set_xlabel('R')
	ax.set_ylabel('E')
	ax.legend()
	plt.show()