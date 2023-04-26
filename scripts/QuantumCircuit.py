import pennylane as qml
import numpy as np
import ExactSolution as ex

class QuantumCircuit:
    def __init__(self,dev,H):
        self.dev = dev
        self.qubits = len(dev.wires.toarray())
        self.H = H

    def ansatz(self):
        @qml.qnode(self.dev)
        def helperAnsatz(angles):
            nrAngles = len(angles)
            theta = angles

            # inital rotations
            for qb in range(self.qubits):
                qml.RX(theta[2*qb], wires=qb)
                qml.RZ(theta[2*qb+1], wires=qb)

            for i in range(2*self.qubits,nrAngles,2*self.qubits):
                # CNOT to entangle
                for j in range(0,self.qubits-1,2):
                    qml.CZ(wires=[j,j+1])

                for j in range(1,self.qubits-1,2):
                    qml.CZ(wires=[j,j+1])

                # second round of rotations
                for qb in range(self.qubits):
                    qml.RX(theta[i+2*qb], wires=qb)
                    qml.RZ(theta[i+2*qb+1], wires=qb)
                
                # qml.RX(theta[i], wires=0)
                # qml.RZ(theta[i+1], wires=0)
                # qml.RX(theta[i+2], wires=1)
                # qml.RZ(theta[i+3], wires=1)

            # qml.U3(basis[0]*np.pi/2, 0, basis[0]*np.pi, wires=0)  # apply hadamard gate to qubit 0 iff basis[0]=1
            # qml.U3(basis[1]*np.pi/2, 0, basis[1]*np.pi, wires=1)  # apply hadamard gate to qubit 1 iff basis[1]=1

            return qml.expval(self.H)
        return helperAnsatz

    def plotCircuit(self,theta):
        qml.drawer.use_style("black_white")
        fig = qml.draw_mpl(self.ansatz())(list(theta))[0]
        fig.savefig(f'../plots/circuitPlot_{int(len(theta))/(2*self.qubits)-1}Layers_{self.qubits}qubits.pdf',format='pdf')

    # def get_expectation(self,gate, probabilities):
    #     II = np.array([1,1,1,1])
    #     IZ = np.array([1,-1,1,-1])
    #     ZI = np.array([1,1,-1,-1])
    #     ZZ = np.array([1,-1,-1,1])
        
    #     probabilities = np.array(probabilities)

    #     if gate == 'II':
    #         return np.dot(II, probabilities)
    #     if gate == 'IZ' or gate == 'IX':
    #         return np.dot(IZ, probabilities)
    #     if gate == 'ZI' or gate == 'XI':
    #         return np.dot(ZI, probabilities)
    #     if gate == 'ZZ' or gate == 'XX' or gate == 'XZ' or gate == 'ZX':
    #         return np.dot(ZZ, probabilities)

    #     return 'Unidentified Gate'

    # def energy(self,R,probs_XX, probs_XZ, probs_ZX, probs_ZZ):
    #     """ 
    #     counts - dictionary of measured counts, e.g., {'00': 4096, '11': 4096}
    #     shots - total number of shots for each basis (for convenience. Can be computed from counts)
    #     """
    #     # Replace with code to convert counts to expectation values to get energy expectation.

    #     E_H = ex.Hamiltonian(R, self.get_expectation('XI', probs_XX), self.get_expectation('IX', probs_XX), self.get_expectation('ZI', probs_ZZ), self.get_expectation('IZ', probs_ZZ), self.get_expectation('XX', probs_XX), self.get_expectation('ZZ', probs_ZZ), self.get_expectation('XZ', probs_XZ), self.get_expectation('ZX', probs_ZX), 1)

    #     return E_H

    def optimize(self,theta,c,eta,shots, iterations,method,aSPSA=2):
        energy_list = []
        params = len(theta)

        for i in range(iterations):
            # angles = [[]]*params
            # basis = [[]]*2
            thetas = []
            #gradient = []

            if method=='SOGD' or method=='FOGD' or method=='PS':
                for j in range(params):
                    e = np.zeros(params)
                    e[j] = 1
                    if method=='PS':
                        theta_plus = theta.copy() + (np.pi/2)*e
                        theta_minus = theta.copy() - (np.pi/2)*e
                    else:
                        theta_plus = theta.copy() + c*e
                        theta_minus = theta.copy() - c*e

                    thetas.append(theta_plus)
                    thetas.append(theta_minus) 
                    # angles = [angles[k] + [theta_plus[k]]*4 for k in range(params)]
                    # basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]
                    # angles = [angles[k] + [theta_minus[k]]*4 for k in range(params)]
                    # basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]

                # angles = [angles[kk] + [theta[kk]]*4 for kk in range(params)]
                # basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]
                # angles = np.array(angles+basis)
                #probs = self.ansatz()(angles,shots=shots)
                #energy_list.append(self.energy(R,probs[8*params], probs[8*params+1], probs[8*params+2], probs[8*params+3]))
                energy_list.append(self.ansatz()(theta,shots=shots))


                #optimization proeccess
                # for j in range(params):
                #     E_plus = self.energy(R,probs[8*j], probs[8*j+1], probs[8*j+2], probs[8*j+3])
                #     E_minus = self.energy(R,probs[8*j+4], probs[8*j+5], probs[8*j+6], probs[8*j+7])

                #     if method=='FOGD':
                #         gradient.append((E_plus-energy_list[-1])/c) #FOGD
                #     elif method=='SOGD':
                #         gradient.append( (E_plus - E_minus)/(2*c) )  # approximate gradient SOGD
                #     else:
                #         gradient.append( (E_plus - E_minus)/2 ) #PS
                E_plus = np.array([self.ansatz()(theta_plus,shots=shots) for theta_plus in thetas[::2]])
                E_minus = np.array([self.ansatz()(theta_minus,shots=shots) for theta_minus in thetas[1::2]])

                if method=='FOGD':
                    gradient = (E_plus-energy_list[-1])/c #FOGD
                elif method=='SOGD':
                    gradient = (E_plus - E_minus)/(2*c)  # approximate gradient SOGD
                else:
                    gradient = (E_plus - E_minus)/2 #PS

            else:
                a_i = aSPSA / (i+1)
                c_i = c / ((i+1)**(1/3))

                e = 2*np.random.randint(2,size=(params,))-1
                theta_plus = theta.copy() + c_i*e
                theta_minus = theta.copy() - c_i*e

                # angles = [angles[k] + [theta_plus[k]]*4 for k in range(params)]
                # basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]
                # angles = [angles[k] + [theta_minus[k]]*4 for k in range(params)]
                # basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]

                # angles = [angles[k] + [theta[k]]*4 for k in range(params)]
                # basis  = [basis[0] + [1,1,0,0], basis[1] + [1,0,1,0]]
                # angles = np.array(angles + basis)
                # probs = self.ansatz()(angles, shots=shots)
                # energy_list.append(self.energy(R,probs[8], probs[9], probs[10], probs[11]))
                energy_list.append(self.ansatz()(theta,shots=shots))

                # E_plus = self.energy(R,probs[0], probs[1], probs[2], probs[3])
                # E_minus = self.energy(R,probs[4], probs[5], probs[6], probs[7])
                E_plus = self.ansatz()(theta_plus,shots=shots)
                E_minus = self.ansatz()(theta_minus,shots=shots)

                gradient = (E_plus - E_minus)/(2*c_i*e)  # approximate gradient

            if method=='SPSA':
                theta = theta - a_i*np.array(gradient)
            else:
                theta = theta - eta*np.array(gradient)  # update the angles using gradient descent!

        #final energy
        # angles = [[theta[k]]*4 for k in range(params)]
        # basis  = [[1,1,0,0],[1,0,1,0]]
        # angles = np.array(angles + basis)

        # probs = self.ansatz()(angles,shots=shots)
        #E_final = self.energy(R,probs[0], probs[1], probs[2], probs[3])
        E_final = self.ansatz()(theta,shots=shots)
        energy_list.append(E_final)

        return np.array(energy_list)
