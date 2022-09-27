import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random

def generate_training_data(x, params):
	p1, p2 = params
	return p1*x + p2 + np.random.rand(len(x))*random.randint(10,20)

def pred(x, params):
	p1, p2 = params
	return p1*x + p2

def partialP1(x, y, p):
	return (2*(y-p)*x).sum()

def partialP2(y, p):
	return 2*(y-p).sum()

def cost(y, p):
	return ((y - p)**2).sum()/y.shape

def step(x, y, params, lr):
	preds = pred(x, params)
	params[0] += lr * partialP1(x, y, preds)
	params[1] += lr * partialP2(y, preds)
	# c = cost(y, preds)
	# print(f'Cost: {c}')


lr = 1e-7
m = 1000
n = m / 10
correct_params = [random.random() for _ in range(2)]
params = [random.random() for _ in range(2)]
x = np.arange(m) / 10
y = generate_training_data(x, correct_params)

p = pred(x, params)
c = cost(y, p)
print(f'Untrained Loss: {c}')
print(f'Params: {params}')
for i in range(1000):
	step(x,y,params,lr)

preds = pred(x, params)
print(f'partial p1:{partialP1(x,y,preds)}')
print(f'Params: {params}')

print(((preds - y)**2).sum()/m)
print(cost(y, preds))


print(f'Correct Params: {correct_params}')
print(f'Current Params: {params}')

plt.plot(x, y, 'ro', x, pred(x, params))
plt.show()