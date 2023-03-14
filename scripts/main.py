import numpy as np
import QuantumCircuit as qc
from matplotlib import pyplot as plt

R = 90
theta = 2*np.pi*np.random.rand(12)
c = 0.05*2*np.pi
eta = 0.5
shots = 8192
iterations = 25

energy_list = qc.optimize(R,theta,c,eta,shots,iterations)

# plots
qml.drawer.use_style("black_white")
qml.draw_mpl(ansatz)(list(theta)+[0,1])

fig, ax = plt.subplots()
ax.plot([0,iterations],[exactEnergy(),exactEnergy()],'--',color='k')
ax.plot(energy_list,'o')
ax.set(xlabel = 'iterations', ylabel = 'energy')
plt.show()