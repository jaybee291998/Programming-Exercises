import numpy as np
import matplotlib.pyplot as plt
import random

step_size = 50
base_lr = 0
max_lr = 10
m = 1000

epochs = np.array(list(range(m)))

cycles = np.floor(1 + epochs / (2*step_size))

x = np.absolute(epochs/step_size - 2 * cycles + 1)

learning_rates = base_lr + (max_lr - base_lr) * np.maximum(0, (1-x))
# epoch_divide_stepsize = epochs / step_size
# two_times_cycle = 2 * cycles


# plt.plot(epochs, epoch_divide_stepsize, epochs, two_times_cycle)
plt.plot(epochs, learning_rates)
plt.show()