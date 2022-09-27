import numpy as np

def estimate_gaussian(X):
	m, n = X.shape
	mu = np.mean(X, axis=0)
	x_mu = X - mu
	sigma_square = np.std(X, axis=0) ** 2
	return mu, sigma_square

def estimate_gaussian_mult(X):
	m, n = X.shape
	mu = np.mean(X, axis=0)
	x_mu = X - mu
	cov_mat = (np.transpose(x_mu) @ x_mu) / m
	return mu, cov_mat

def multivariate_gaussian(X, mu, sigma2):
	m, n = X.shape
	# if sigma2 is a row or column vector, convert into a covariance matrix
	if len(sigma2.shape) == 1:
		sigma2 = np.diag(sigma2)

	# perform mean normalization to the dataset
	X = X - mu

	sigma2_det = np.linalg.det(sigma2)
	sigma2_inv = np.linalg.inv(sigma2)
	constant = ((2*np.pi)**(n/2))*(sigma2_det**(0.5))
	result = np.exp(-0.5 * np.sum(X@sigma2_inv*X, axis=1)).reshape((m,1))
	return result/constant

def select_threshold(pval, yval):
	best_epsilon = 0
	best_f1 = 0
	min_ep = np.min(pval)
	max_ep = np.max(pval)
	stepsize = (max_ep - min_ep) / 10000 
	for epsilon in np.arange(min_ep, max_ep, stepsize):
		prediction = pval < epsilon # boolean array
		true_pos = np.sum(np.logical_and(prediction, yval.astype(bool)).astype(int))
		false_pos = np.sum(np.logical_and(np.invert(yval.astype(bool)), prediction).astype(int))
		false_neg = np.sum(np.logical_and(np.invert(prediction), yval.astype(bool)).astype(int))
		precision = true_pos / (true_pos + false_pos)
		recall = true_pos / (true_pos + false_neg)

		f1 = 2 * precision * recall / (precision + recall)
		if f1 > best_f1:
			best_f1 = f1 
			best_epsilon = epsilon

	return best_epsilon, best_f1