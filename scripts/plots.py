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

def plotOptimisation(R,energy_list,iterations,i=''):
	fig, ax = plt.subplots()
	ax.plot([0,iterations],[ex.exactEnergy(R),ex.exactEnergy(R)],'--',color='k',label='Exact')
	ax.plot(energy_list,'o',label='VQE')
	ax.set(xlabel = 'log(iterations)', ylabel = 'log(energy)')
	ax.legend()
	#plt.show()
	fig.savefig(f'../plots/{R}optimizationPlot{i}.png',format='png')

def plotEAgainstR(RArray,exactE,approxESim,approxE_IBM=None):
	fig, ax = plt.subplots()
	ax.plot(RArray,exactE,'k-',label='Exact')
	ax.plot(RArray,approxESim,'bx-',label='VQE_Simulation')
	if approxE_IBM:
		ax.plot(RArray,approxE_IBM,'or-',label='VQE_IBM')

	ax.set_xlabel('R')
	ax.set_ylabel('E')
	ax.legend()
	plt.show()
	fig.savefig('../plots/Eplot.png',format='png')