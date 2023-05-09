import numpy as np
import pennylane as qml

parameters = np.loadtxt("HamiltonianParameters.txt")

def Hamiltonian(R):
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

    H = Jx * (qml.PauliX(0) + qml.PauliX(1))
    H = H + Jz * (qml.PauliZ(0) + qml.PauliZ(1))
    H = H + Jxx * qml.PauliX(0)@qml.PauliX(1)
    H = H + Jzz * qml.PauliZ(0)@qml.PauliZ(1)
    H = H + Jxz * (qml.PauliX(0)@qml.PauliZ(1) + qml.PauliZ(0)@qml.PauliX(1))
    H = H + C*qml.Identity(0)@qml.Identity(1)

    return H*0.5

def exactEnergy(Hmatrix):
    E, V = np.linalg.eigh(Hmatrix)
    return np.min(E)