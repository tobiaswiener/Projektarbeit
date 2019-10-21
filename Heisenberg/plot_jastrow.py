import json
import matplotlib.pyplot as plt



exact_gs_energy = -39.14752260706246



# import the data from log file
data=json.load(open("Jastrow.log"))

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