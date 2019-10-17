# Load the data from the .log file
import json
import matplotlib.pyplot as plt
import numpy as np

data=json.load(open("test.log"))

# Extract the relevant information

iters=[]
energy=[]
sf=[]

for iteration in data["Output"]:
    iters.append(iteration["Iteration"])
    energy.append(iteration["Energy"]["Mean"])
    sf.append(iteration["Structure Factor"]["Mean"])
fig, ax1 = plt.subplots()
ax1.plot(iters, energy, color='blue', label='Energy')
ax1.set_ylabel('Energy')
ax1.set_xlabel('Iteration')
ax2 = ax1.twinx()
ax2.plot(iters, np.array(sf), color='green', label='Structure Factor')
ax2.set_ylabel('Structure Factor')
ax1.legend(loc=2)
ax2.legend(loc=1)
plt.show()


print(r"Structure factor = {0:.3f}({1:.3f})".format(np.mean(sf[-50:]),
                                              np.std(np.array(sf[-50:]))/np.sqrt(50)))
print(r"Energy = {0:.3f}({1:.3f})".format(np.mean(energy[-50:]), np.std(energy[-50:])/(np.sqrt(50))))

