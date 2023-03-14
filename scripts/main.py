import pennylane as qml
import numpy as np
import UsefulGates as g
from matplotlib import pyplot as plt

dev = qml.device("default.qubit", wires=2)

parameters = np.loadtxt("HamiltonianParameters.txt")

R = 90
H_param = parameters[parameters[:,0]==R,1:].flatten()

C = H_param[0]
Jx = H_param[1]
Jz = H_param[2]
#Jx = H_param[3]
Jxx = H_param[4]
Jxz = H_param[5]
#Jz = H_param[6]
#Jzx = H_param[7]
Jzz = H_param[8]

#print(f"Jx={Jx}, Jz={Jz}, Jxx={Jxx}, Jzz={Jzz}, Jxz={Jxz}, C={C}")

def Hamiltonian():
    H = Jx * (np.kron(g.X,g.Id) + np.kron(g.Id,g.X))
    H = H + Jz * (np.kron(g.Z,g.Id) + np.kron(g.Id,g.Z))
    H = H + Jxx * np.kron(g.X,g.X)
    H = H + Jzz * np.kron(g.Z,g.Z)
    H = H + Jxz * (np.kron(g.X,g.Z) + np.kron(g.Z,g.X))
    H = H + C * np.kron(g.Id,g.Id)

    return H/2

def exactEnergy():
    H = Hamiltonian()

    E, V = np.linalg.eigh(H)
    return np.min(E)

#print(f"Exact ground state energy is E = {exactEnergy()}")

@qml.qnode(dev)
def ansatz(angles):
    theta = angles[:12]
    basis = angles[12:]  # basis has two elements with values 0 or 1

    # inital rotations
    qml.RX(theta[0], wires=0)
    qml.RZ(theta[1], wires=0)
    qml.RX(theta[2], wires=1)
    qml.RZ(theta[3], wires=1)

    # CNOT to entangle
    qml.CZ(wires=[0,1])

    # second round of rotations
    qml.RX(theta[4], wires=0)
    qml.RZ(theta[5], wires=0)
    qml.RX(theta[6], wires=1)
    qml.RZ(theta[7], wires=1)

    #CNOT to entangle
    qml.CZ(wires = [0,1])

    # third round of rotations
    qml.RX(theta[8], wires=0)
    qml.RZ(theta[9], wires=0)
    qml.RX(theta[10], wires=1)
    qml.RZ(theta[11], wires=1)

    qml.U3(basis[0]*np.pi/2, 0, basis[0]*np.pi, wires=0)  # apply hadamard gate to qubit 0 iff basis[0]=1
    qml.U3(basis[1]*np.pi/2, 0, basis[1]*np.pi, wires=1)  # apply hadamard gate to qubit 1 iff basis[1]=1

    return qml.probs(wires=[0,1])

def get_expectation(gate, probabilities):
    II = np.array([1,1,1,1])
    IZ = np.array([1,-1,1,-1])
    ZI = np.array([1,1,-1,-1])
    ZZ = np.array([1,-1,-1,1])
    
    probabilities = np.array(probabilities)

    if gate == 'II':
        return np.dot(II, probabilities)
    if gate == 'IZ' or gate == 'IX':
        return np.dot(IZ, probabilities)
    if gate == 'ZI' or gate == 'XI':
        return np.dot(ZI, probabilities)
    if gate == 'ZZ' or gate == 'XX' or gate == 'XZ' or gate == 'ZX':
        return np.dot(ZZ, probabilities)

    return 'Unidentified Gate'

def energy(probs_XX, probs_XZ, probs_ZX, probs_ZZ):
    """ 
    counts - dictionary of measured counts, e.g., {'00': 4096, '11': 4096}
    shots - total number of shots for each basis (for convenience. Can be computed from counts)
    """
    # Replace with code to convert counts to expectation values to get energy expectation.

    E_H = 0
    E_H += Jx*(get_expectation('XI', probs_XX) + get_expectation('IX', probs_XX))
    E_H += Jz*(get_expectation('ZI', probs_ZZ) + get_expectation('IZ', probs_ZZ))
    E_H += Jxx*get_expectation('XX', probs_XX) 
    E_H += Jzz*get_expectation('ZZ', probs_ZZ) 
    E_H += Jxz*(get_expectation('XZ', probs_XZ) + get_expectation('ZX', probs_ZX))
    E_H += C
    E_H *= 0.5

    return E_H

def optimize(theta,c,eta,shots, iterations):
	energy_list = []
	params = len(theta)

	for jj in range(iterations):

	    angles = [[]]*params
	    basis = [[]]*2
	    gradient = []
	    for ii in range(params):
	        e = np.zeros(params)
	        e[ii] = 1
	        theta_plus = theta.copy() + c*e
	        theta_minus = theta.copy() - c*e

	        angles = [angles[kk] + [theta_plus[kk]]*4 for kk in range(params)]
	        basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]
	        angles = [angles[kk] + [theta_minus[kk]]*4 for kk in range(params)]
	        basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]

	    angles = [angles[kk] + [theta[kk]]*4 for kk in range(params)]
	    basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]
	    angles = np.array(angles + basis)
	    probs = ansatz(angles, shots=shots)

	    for ii in range(params):
	        E_plus = energy(probs[8*ii], probs[8*ii+1], probs[8*ii+2], probs[8*ii+3])
	        E_minus = energy(probs[8*ii+4], probs[8*ii+5], probs[8*ii+6], probs[8*ii+7])
	        gradient.append( (E_plus - E_minus)/(2*c) )  # approximate gradient

	    energy_list.append(energy(probs[8*params], probs[8*params+1], probs[8*params+2], probs[8*params+3]))
	    theta = theta - eta*np.array(gradient)  # update the angles using gradient descent!
	    #print(f"Energy at iteration {jj}: {energy_list[-1]}")

	angles = [[theta[kk]]*4 for kk in range(params)]
	basis  = [[1,1,0,0],[1,0,1,0]]
	angles = np.array(angles + basis)

	probs = ansatz(angles, shots=shots)
	E_final = energy(probs[0], probs[1], probs[2], probs[3])
	energy_list.append( E_final )  # final energy!

	#print(f"Final energy: {energy_list[-1]}")
	return energy_list




theta = 2*np.pi*np.random.rand(12)
c = 0.05*2*np.pi
eta = 0.5
shots = 8192
iterations = 25
energy_list = optimize(theta,c,eta,shots,iterations)

# plots
qml.drawer.use_style("black_white")
qml.draw_mpl(ansatz)(list(theta)+[0,1])

fig, ax = plt.subplots()
ax.plot([0,iterations],[exactEnergy(),exactEnergy()],'--',color='k')
ax.plot(energy_list,'o')
ax.set(xlabel = 'iterations', ylabel = 'energy')
plt.show()






