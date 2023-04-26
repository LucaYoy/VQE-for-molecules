import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
from matplotlib import pyplot as plt

def plotOptimisation(Hmatrix,energy_listFOGD,energy_listSOGD,energy_listPS,energy_listSPSA,iterations,layers,IBM_dict={'energyArray':[],'method':''},i=''):
	fig, ax = plt.subplots()
	ax.plot([0,iterations],[ex.exactEnergy(Hmatrix),ex.exactEnergy(Hmatrix)],'--',color='k',label='Exact')
	ax.plot(energy_listFOGD,'bo-',label='VQE-FirstOrderGD')
	ax.plot(energy_listSOGD,'ro-',label='VQE-SecondOrderGD')
	ax.plot(energy_listPS,'go-',label='VQE-ParameterShiftGD')
	ax.plot(energy_listSPSA,'ko-',label='VQE-SPSA')
	ax.plot(IBM_dict['energyArray'],'o-',label=f"IBM-VQE-{IBM_dict['method']}")
	ax.set_xlabel('iterations',fontsize=9)
	ax.set_ylabel('E',fontsize=9)
	ax.tick_params(axis='x', labelsize=9)
	ax.tick_params(axis='y', labelsize=9)
	ax.legend(prop={'size': 5})
	fig.set_size_inches(3.4,2.1)
	plt.subplots_adjust(bottom=0.19,left=0.2)
	fig.savefig(f'../plots/optimizationPlotWith{layers}Layers{i}.pdf',format='pdf',dpi=100)
	plt.show()

def plotEAgainstR(RArray,exactE,approxESim,layers,method,approxE_IBM=None):
	fig, ax = plt.subplots()
	ax.plot(RArray,exactE,'k-',label='Exact')
	ax.plot(RArray,approxESim,'bx-',label='VQE_Simulation')
	if approxE_IBM:
		ax.plot(approxE_IBM[0],approxE_IBM[1],'rx',label='VQE_IBM')

	ax.set_xlabel('R',fontsize=9)
	ax.set_ylabel('E',fontsize=9)
	ax.tick_params(axis='x', labelsize=9)
	ax.tick_params(axis='y', labelsize=9)
	ax.legend(prop={'size': 5})
	fig.set_size_inches(3.4,2.1)
	plt.subplots_adjust(bottom=0.19,left=0.2)
	fig.savefig(f'../plots/Eplot_{method}_{layers}Layers.pdf',format='pdf',dpi=100)
	plt.show()

def plotDeltaE_layers(R,approxEArray,exactE,method):
	fig, ax = plt.subplots()
	ax.plot(range(1,len(approxEArray)+1),np.abs(approxEArray - exactE),'xb')
	ax.set_xlabel('Layers',fontsize=9)
	ax.set_ylabel('|deltaE|',fontsize=9)

	ax.tick_params(axis='x', labelsize=9)
	ax.tick_params(axis='y', labelsize=9)
	ax.legend(prop={'size': 5})
	fig.set_size_inches(3.4,2.1)
	plt.subplots_adjust(bottom=0.19,left=0.2)
	fig.savefig(f'../plots/deltaE_layers_{R}_{method}.pdf',format='pdf',dpi=100)
	plt.show()









