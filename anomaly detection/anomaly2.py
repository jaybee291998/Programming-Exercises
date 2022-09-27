import scipy.io 
from sklearn.model_selection import train_test_split
import numpy as np
from utils import estimate_gaussian, multivariate_gaussian, estimate_gaussian_mult, select_threshold
from dataloader import get_dataset

# path of the file
path = 'datasets/shuttle.mat'
# load data from the file
data = scipy.io.loadmat(path)


X_train, y_train, X_cv, y_cv, X_test, y_test = get_dataset(path)
# mu, sigma2 = estimate_gaussian(X_train)
# p = multivariate_gaussian(X_train, mu, sigma2)
# pval = multivariate_gaussian(X_cv, mu, sigma2)
# ptest = multivariate_gaussian(X_test, mu, sigma2)

mu, cov_mat = estimate_gaussian_mult(X_train)
p = multivariate_gaussian(X_train, mu, cov_mat)
pval = multivariate_gaussian(X_cv, mu, cov_mat)
ptest = multivariate_gaussian(X_test, mu, cov_mat)

epsilon, f1 = select_threshold(pval, y_cv)
print(f'epsilon: {epsilon}')
print(f'f1: {f1}')

outliers = np.sum((ptest < epsilon).astype(int))

print(f'found {outliers} outliers in the test set.')


# print(f'X_train: {X_train.shape}')
# print(f'y_train: {y_train.shape}')

# print(f'X_cv: {X_cv.shape}')
# print(f'y_cv: {y_cv.shape}')

# print(f'X_test: {X_test.shape}')
# print(f't_test: {y_test.shape}')

# print(f'y test sum: {np.sum(y_test)}')
# print(np.sum(y_test[-int(np.sum(y_test)):]))
