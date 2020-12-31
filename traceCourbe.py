import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt("/home/moufdi/GitHubProjects/Projet_mutlithreading/Propagation666.txt")
#print(type(data))
#print(data)
print(np.shape(data))
#print(data[:,1])
#print(data[:,2])

plt.plot(data[0:99,1], data[0:99:,2])
plt.plot(data[100:199,1], data[100:199:,2])

plt.show()


