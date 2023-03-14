import numpy as np
import UsefulGates as g

parameters = np.loadtxt("HamiltonianParameters.txt")

def Hamiltonian(R,XI,IX,ZI,IZ,XX,ZZ,XZ,ZX,II):
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

    H = Jx * (XI + IX)
    H = H + Jz * (ZI + IZ)
    H = H + Jxx * XX
    H = H + Jzz * ZZ
    H = H + Jxz * (XZ + ZX)
    H = H + C * II

    return H/2

def exactEnergy(R):
    H = Hamiltonian(R,np.kron(g.X,g.Id),np.kron(g.Id,g.X),np.kron(g.Z,g.Id),np.kron(g.Id,g.Z),np.kron(g.X,g.X),np.kron(g.Z,g.Z),np.kron(g.X,g.Z),np.kron(g.Z,g.X),np.kron(g.Id,g.Id))

    E, V = np.linalg.eigh(H)
    return np.min(E)