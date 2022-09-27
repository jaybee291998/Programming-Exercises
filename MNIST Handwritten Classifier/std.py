import numpy as np 
import matplotlib.pyplot as plt

def std(x):
	mu = np.mean(x)
	n = x.shape
	return np.sqrt(np.sum((x - mu)**2)/n)

def p(x, mu=1, std=1):
	return (1/(np.sqrt(2*numpy.pi)*std))*(np.e**-((x-mu)/(s2*td**2)))

n = 100
a = np.random.rand(n)
mu = np.mean(a)
std_ = std(a)
std = np.std(a)
x = np.arange(0,n,1)
print(f'mu: {mu}')
print(f'std_: {std_}')
print(f'std: {std}')

plt.plot(x, a, 'ro')
plt.ylabel('random number')
plt.show()