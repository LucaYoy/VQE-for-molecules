import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
from matplotlib import pyplot as plt

def plotCircuit(dev,theta):
	qml.drawer.use_style("black_white")
	circuit = qc.QuantumCircuit(dev)
	qml.draw_mpl(circuit.ansatz)(list(theta)+[0,1])
	fig.savefig('../plots/circuitPlot.png',format='png')

def plotOptimisation(R,energy_list,iterations):
	fig, ax = plt.subplots()
	ax.plot([0,iterations],[ex.exactEnergy(R),ex.exactEnergy(R)],'--',color='k',label='Exact')
	ax.plot(energy_list,'o',label='VQE')
	ax.set(xlabel = 'iterations', ylabel = 'energy')
	ax.legend()
	plt.show()
	fig.savefig('../plots/optimizationPlot.png',format='png')

def plotEAgainstR(dev,theta,c,eta,shots,RRange,minChange):
	parameters = np.loadtxt("HamiltonianParameters.txt")
	RArray = parameters[int(RRange[0]/5-1):int(RRange[1]/5),0]
	exactE = [ex.exactEnergy(R) for R in RArray]
	circuit = qc.QuantumCircuit(dev)
	approxE = [circuit.optimize(R, theta, c, eta, shots, minChange)[0][-1] for R in RArray]

	fig, ax = plt.subplots()
	ax.plot(RArray,exactE,'k-',label='Exact')
	ax.plot(RArray,approxE,'x-',label='VQE')
	ax.set_xlabel('R')
	ax.set_ylabel('E')
	ax.legend()
	plt.show()
	fig.savefig('../plots/Eplot.png',format='png')