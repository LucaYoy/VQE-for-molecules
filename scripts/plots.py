import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
from matplotlib import pyplot as plt

def plotOptimisation(R,energy_listFOGD,energy_listSOGD,energy_listPS,energy_listSPSA,iterations,layers,i=''):
	fig, ax = plt.subplots()
	ax.plot([0,iterations],[ex.exactEnergy(R),ex.exactEnergy(R)],'--',color='k',label='Exact')
	ax.plot(energy_listFOGD,'bo-',label='VQE-FirstOrderGD')
	ax.plot(energy_listSOGD,'ro-',label='VQE-SecondOrderGD')
	ax.plot(energy_listPS,'go-',label='VQE-ParameterShiftGD')
	ax.plot(energy_listSPSA,'ko-',label='VQE-SPSA')
	ax.set(xlabel = 'iterations', ylabel = 'energy')
	ax.legend()
	plt.show()
	fig.set_size_inches(16,12)
	fig.savefig(f'../plots/{R}optimizationPlotWith{layers}Layers{i}.png',format='png',dpi=100)

def plotEAgainstR(RArray,exactE,approxESim,layers,method,approxE_IBM=None):
	fig, ax = plt.subplots()
	ax.plot(RArray,exactE,'k-',label='Exact')
	ax.plot(RArray,approxESim,'bx-',label='VQE_Simulation')
	if approxE_IBM:
		ax.plot(RArray,approxE_IBM,'rx-',label='VQE_IBM')

	ax.set_xlabel('R')
	ax.set_ylabel('E')
	ax.legend()
	plt.show()
	fig.set_size_inches(16,12)
	fig.savefig(f'../plots/Eplot_{method}_{layers}Layers.png',format='png',dpi=100)

def plotDeltaE_layers(R,approxEArray,exactE,method):
	fig, ax = plt.subplots()
	ax.plot(range(1,len(approxEArray)+1),np.abs(approxEArray - exactE),'xb')
	ax.set_xlabel('Layers')
	ax.set_ylabel('|deltaE|')

	plt.show()
	fig.set_size_inches(16,12)
	fig.savefig(f'../plots/deltaE_layers_{R}_{method}.png',format='png',dpi=100)









