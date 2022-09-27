import gzip
import numpy as np
import matplotlib.pyplot as plt

# f = gzip.open('datasets/train-images-idx3-ubyte.gz', 'rb')

# buf = f.read()
# data = np.frombuffer(buf, dtype=np.uint8)
# data = data[15:-1].reshape(-1, 784)
# print(data.shape)

# plt.imshow(data[0].reshape(28,28))
# plt.show()

class NN:
	def __init__(self, layers_config=None):
		self.num_layers = len(layers_config)
		self.weights = self.init_weights(layers_config)
		self.bias = self.init_bias(layers_config)
		self.init_epsilon = 1e-2

	def feedforward(self, x):
		act = self.sigmoid(np.transpose(x))
		for w, b in zip(self.weights, self.bias):
			z = w@act + b
			act = self.sigmoid(z)
		return act

	def forward(self, x):
		acts = [self.sigmoid(np.transpose(x))]
		for l in range(1,self.num_layers,1):
			z = self.weights[l-1]@acts[l-1] + self.bias[l-1]
			acts.append(self.sigmoid(z))
		return acts

	def backprop(self, x, y):
		m, n = y.shape
		acts = self.forward(x)
		delta = [0 for _ in range(self.num_layers)]
		delta[-1] = acts[-1]-np.transpose(y)
		for l in range(self.num_layers-2, 0, -1):
			delta[l] = (np.transpose(self.weights[l])@delta[l+1])*(acts[l]*(1-acts[l]))
		nabla_weight = []
		for l in range(self.num_layers-1):
			nab = delta[l+1]@np.transpose(acts[l])
			nabla_weight.append(nab/m)

		return nabla_weight, [np.mean(delta[l], axis=1, keepdims=True) for l in range(1, self.num_layers, 1)]

	def check_grad(self, x, y):
		analytic_grad_weight, analytic_grad_bias = self.backprop(x,y)
		numerical_grad_weight = []
		numerical_grad_bias = []
		for l in range(self.num_layers-1):
			row, col = self.weights[l].shape
			weight_grad = np.zeros((row, col))
			for r in range(row):
				for c in range(col):
					# add the epsilon to the current weight
					self.weights[l][r, c] += self.init_epsilon
					plus_epsilon = self.cost(x, y)

					self.weights[l][r, c] -= 2 * self.init_epsilon
					minus_epsilon = self.cost(x, y)

					g = (plus_epsilon - minus_epsilon) / 2 * self.init_epsilon
					# return the weight into default value
					self.weights[l][r, c] += self.init_epsilon
					weight_grad[r, c] = g 
			numerical_grad_weight.append(weight_grad)

			bias_grad = np.zeros((row, 1))
			for r in range(row):
				self.bias[l][r, 0] += self.init_epsilon
				plus_epsilon = self.cost(x, y)

				self.bias[l][r, 0] -= 2 * self.init_epsilon
				minus_epsilon = self.cost(x, y)

				b = (plus_epsilon - minus_epsilon) / 2 * self.init_epsilon

				self.bias[l][r, 0] += self.init_epsilon
				bias_grad[r, 0] = b
			numerical_grad_bias.append(bias_grad)

		dif = 0
		for l in range(self.num_layers-1):
			current_weight_grad = analytic_grad_weight[l]
			current_bias_grad = analytic_grad_bias[l]
			num_weight_grad = numerical_grad_weight[l]
			num_bias_grad = numerical_grad_bias[l]
			dif += ((np.mean(current_weight_grad - num_weight_grad) + np.mean(current_bias_grad - num_bias_grad)) / 2)
		print(f'dif: {dif/self.num_layers}')
		return numerical_grad_weight, numerical_grad_bias


	def cost(self, x, y):
		acts = np.transpose(self.feedforward(x))
		return np.mean(-y*np.log(acts)-(1-y)*np.log(1-acts))

	@staticmethod
	def sigmoid(x):
		return 1 / (1 + np.exp(-x))

	@staticmethod
	def sigmoid_prime(x):
		a = self.sigmoid(x)
		return a*(1-a)

	@staticmethod
	def init_weights(layers_config):
		weights = []
		for s in range(len(layers_config)-1):
			weights.append(np.random.rand(layers_config[s+1], layers_config[s]))
		return weights
	@staticmethod
	def init_bias(layers_config):
		bias = []
		for s in range(len(layers_config)-1):
			bias.append(np.random.rand(layers_config[s+1], 1))
		return bias

w = np.random.rand(5,10)
x = np.random.rand(100, 10)
y = np.random.rand(100, 3)
n = NN([10, 5, 5, 3])
# acts = n.feedforward(x)
# acts2 = n.forward(x)[-1]

# grad_weight, grad_bias = n.backprop(x,y)
# num_grad_weight, num_grad_bias = n.check_grad(x, y)
# for g in num_grad_bias:
# 	print(g.shape)

# print('numeric')
# print(num_grad_weight[2])
# print('---------------')
# print('analytic')
# print(grad_weight[2])

l = 0
i = 0
j = 0

grad_weight, grad_bias = n.backprop(x,y)

original_cost = n.cost(x, y)
epsilon = 1e-9
original_weight = n.weights[l][i, j]
n.weights[l][i, j] += epsilon
plus_epsilon = n.cost(x, y)

n.weights[l][i, j] -= 2*epsilon
minus_epsilon = n.cost(x, y)

n.weights[l][i, j] += epsilon
after_weight = n.weights[l][i, j]

dif = (plus_epsilon - minus_epsilon) / (2 * epsilon)

after_cost = n.cost(x, y)

# print(f'original cost: {original_cost}')
# print(f'orginal weight[{l}][{i}, {j}]: {original_weight}')
# print(f'plus epsilon: {plus_epsilon}')
# print(f'minus epsilon: {minus_epsilon}')
# print(f'after weight: {after_weight}')
# print(f'after cost: {after_cost}')
# print(f'parteial: {dif}')
# print(f'analytic: {grad_weight[l][i, j]}')
# print(f'p: {dif}')

print(n.sigmoid(3) - 2)
# print(grad_bias)