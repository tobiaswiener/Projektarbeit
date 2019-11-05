# Import netket library
import netket as nk
# Import Json, this will be needed to examine log files
import json
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import time


data=json.load(open("06_FFNN5_ExactSampler1000_AdaMax_7000_Gd.log"))
exact_gs_energy = -34.46969272725688

# Extract the relevant information
iters_Jastrow=[]
energy_Jastrow=[]

for iteration in data["Output"]:
    iters_Jastrow.append(iteration["Iteration"])
    energy_Jastrow.append(iteration["Energy"]["Mean"])

fig, ax1 = plt.subplots()
ax1.plot(iters_Jastrow, energy_Jastrow, color='C8', label='Energy (Jastrow)')
ax1.set_ylabel('Energy')
ax1.set_xlabel('Iteration')
plt.axis([0,iters_Jastrow[-1],exact_gs_energy-0.1,exact_gs_energy+0.4])
plt.axhline(y=exact_gs_energy, xmin=0,
                xmax=iters_Jastrow[-1], linewidth=2, color='k', label='Exact')
ax1.legend()
plt.show()