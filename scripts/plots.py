import pennylane as qml
import numpy as np
import QuantumCircuit as qc
import ExactSolution as ex
from matplotlib import pyplot as plt

def plotOptimisation(Hmatrix,energy_listFOGD,energy_listSOGD,energy_listPS,energy_listSPSA,iterations,layers,IBM_dict={'energyArray':[],'method':''},i=''):
	fig, ax = plt.subplots()
	ax.plot([0,iterations],[ex.exactEnergy(Hmatrix),ex.exactEnergy(Hmatrix)],'--',color='k',label='Exact')
	ax.plot(energy_listFOGD,'b.-',label='VQE-FirstOrderGD',markersize=4)
	ax.plot(energy_listSOGD,'r.-',label='VQE-SecondOrderGD',markersize=4)
	ax.plot(energy_listPS,'g.-',label='VQE-ParameterShiftGD',markersize=4)
	ax.plot(energy_listSPSA,'k.-',label='VQE-SPSA',markersize=4)
	ax.plot(IBM_dict['energyArray'],'.-')#,label=f"IBM-VQE-{IBM_dict['method']}",markersize=4)
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
	ax.plot(RArray,approxESim,'bx',label='VQE_Simulation',markersize=5)
	if approxE_IBM:
		ax.plot(approxE_IBM[0],approxE_IBM[1],'rx',label='VQE_IBM',markersize=5)

	ax.set_xlabel('R',fontsize=9)
	ax.set_ylabel('E',fontsize=9)
	ax.tick_params(axis='x', labelsize=9)
	ax.tick_params(axis='y', labelsize=9)
	ax.legend(prop={'size': 5})
	fig.set_size_inches(3.4,2.1)
	plt.subplots_adjust(bottom=0.19,left=0.2)
	plt.show()
	fig.savefig(f'../plots/Eplot_{method}_{layers}Layers.pdf',format='pdf',dpi=100)

def plotEAgainstPhi(PhiArray,exactE,approxESim1,approxESim2,approxESim3,layers,method):
	fig, ax = plt.subplots()
	approxESim1Conv = [approxESim1[i] if np.abs(approxESim1[i]-exactE[i])<=0.1 else None for i in range(len(PhiArray))]
	approxESim1NotConv = [approxESim1[i] if np.abs(approxESim1[i]-exactE[i])>0.1 else None for i in range(len(PhiArray))]
	approxESim2Conv = [approxESim2[i] if np.abs(approxESim2[i]-exactE[i])<=0.1 else None for i in range(len(PhiArray))]
	approxESim2NotConv = [approxESim2[i] if np.abs(approxESim2[i]-exactE[i])>0.1 else None for i in range(len(PhiArray))]
	approxESim3Conv = [approxESim3[i] if np.abs(approxESim3[i]-exactE[i])<=0.1 else None for i in range(len(PhiArray))]
	approxESim3NotConv = [approxESim3[i] if np.abs(approxESim3[i]-exactE[i])>0.1 else None for i in range(len(PhiArray))]

	ax.plot(PhiArray,exactE,'k-',label='Exact')
	ax.plot(PhiArray,approxESim1Conv,'bx',label='1 Layer',markersize=5)
	ax.plot(PhiArray,approxESim1NotConv,'bx',alpha=0.4,markersize=5)
	ax.plot(PhiArray,approxESim2Conv,'gx',label='2 layers',markersize=5)
	ax.plot(PhiArray,approxESim2NotConv,'gx',alpha=0.4,markersize=5)
	ax.plot(PhiArray,approxESim3Conv,'mx',label='3 layers',markersize=5)
	ax.plot(PhiArray,approxESim3NotConv,'mx',alpha=0.4,markersize=5)

	ax.set_xlabel('Phi',fontsize=9)
	ax.set_ylabel('E',fontsize=9)
	ax.tick_params(axis='x', labelsize=9)
	ax.tick_params(axis='y', labelsize=9)
	ax.legend(prop={'size': 5})
	fig.set_size_inches(3.4,2.1)
	plt.subplots_adjust(bottom=0.19,left=0.2)
	plt.show()
	fig.savefig(f'../plots/Eplot_{method}_{layers}Layers.pdf',format='pdf',dpi=100)

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









