import pennylane as qml
import numpy as np
import ExactSolution as ex

class QuantumCircuit:
    def __init__(self,dev):
        self.dev = dev

    def ansatz(self,dev):
        @qml.qnode(self.dev)
        def helperAnsatz(angles):
            nrAngles = len(angles)-2
            theta = angles[:nrAngles]
            basis = angles[nrAngles:]  # basis has two elements with values 0 or 1

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

            # #CNOT to entangle
            # qml.CZ(wires = [0,1])

            # # third round of rotations
            # qml.RX(theta[8], wires=0)
            # qml.RZ(theta[9], wires=0)
            # qml.RX(theta[10], wires=1)
            # qml.RZ(theta[11], wires=1)

            qml.U3(basis[0]*np.pi/2, 0, basis[0]*np.pi, wires=0)  # apply hadamard gate to qubit 0 iff basis[0]=1
            qml.U3(basis[1]*np.pi/2, 0, basis[1]*np.pi, wires=1)  # apply hadamard gate to qubit 1 iff basis[1]=1

            return qml.probs(wires=[0,1])
        return helperAnsatz

    def get_expectation(self,gate, probabilities):
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

    def energy(self,R,probs_XX, probs_XZ, probs_ZX, probs_ZZ):
        """ 
        counts - dictionary of measured counts, e.g., {'00': 4096, '11': 4096}
        shots - total number of shots for each basis (for convenience. Can be computed from counts)
        """
        # Replace with code to convert counts to expectation values to get energy expectation.

        E_H = ex.Hamiltonian(R, self.get_expectation('XI', probs_XX), self.get_expectation('IX', probs_XX), self.get_expectation('ZI', probs_ZZ), self.get_expectation('IZ', probs_ZZ), self.get_expectation('XX', probs_XX), self.get_expectation('ZZ', probs_ZZ), self.get_expectation('XZ', probs_XZ), self.get_expectation('ZX', probs_ZX), 1)

        return E_H

    def optimize(self,R,theta,c,eta,shots, iterations):
        energy_list = []
        params = len(theta)

        for i in range(iterations):
            angles = [[]]*params
            basis = [[]]*2
            gradient = []

            for j in range(params):
                e = np.zeros(params)
                e[j] = 1
                theta_plus = theta.copy() + c*e
                theta_minus = theta.copy() - c*e

                angles = [angles[k] + [theta_plus[k]]*4 for k in range(params)]
                basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]
                angles = [angles[k] + [theta_minus[k]]*4 for k in range(params)]
                basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]

            angles = [angles[kk] + [theta[kk]]*4 for kk in range(params)]
            basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]
            angles = np.array(angles+basis)
            probs = self.ansatz(self.dev)(angles,shots=shots)

            #optimization proeccess
            for j in range(params):
                E_plus = self.energy(R,probs[8*j], probs[8*j+1], probs[8*j+2], probs[8*j+3])
                E_minus = self.energy(R,probs[8*j+4], probs[8*j+5], probs[8*j+6], probs[8*j+7])
                gradient.append( (E_plus - E_minus)/(2*c) )  # approximate gradient

            energy_list.append(self.energy(R,probs[8*params], probs[8*params+1], probs[8*params+2], probs[8*params+3]))
            theta = theta - eta*np.array(gradient)  # update the angles using gradient descent!

        #final energy
        angles = [[theta[k]]*4 for k in range(params)]
        basis  = [[1,1,0,0],[1,0,1,0]]
        angles = np.array(angles + basis)

        probs = self.ansatz(self.dev)(angles,shots=shots)
        E_final = self.energy(R,probs[0], probs[1], probs[2], probs[3])
        energy_list.append(E_final)

        return energy_list
