import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random

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

x = np.array([1, 2, 4, 0])
y = np.array([0.5, 1, 2, 0])

params = np.random.rand(2)

lr = 1e-2

for _ in range(100000):
	step(x, y, params, lr)

theta1, theta0 = params
preds = pred(x, params)
print(f'Theta 0: {theta0}')
print(f'Theta 1: {theta1}')
print(f'Cost :{cost(y, preds)}')

x_1 = 1
p = pred(x_1, params)
print(f'h({x_1}) = {p}')