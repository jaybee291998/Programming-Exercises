import scipy.io 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import multivariate_normal
from sklearn.model_selection import train_test_split
import math

# loa the data from the file
mat = scipy.io.loadmat("cover.mat")

# single variate gaussian distribution
def gaussian_distribution(x, mu, sigma):
	pred = np.exp(-(x - mu)**2/(2*sigma**2)) / (np.sqrt(2*np.pi)*sigma)
	return np.prod(pred, axis=1)
# multivariate gaussian distributiunm
def mult_gaus_dist(x, mu, cov_mat):
	m, n = cov_mat.shape
	det = np.linalg.det(cov_mat)
	inv = np.linalg.inv(cov_mat)
	x_mu = x-mu

	num = np.exp(-0.5*(x_mu @ inv @ np.transpose(x_mu)))
	den = np.power(2*np.pi, n/2) * np.power(det, 0.5)

	return num / den

def norm_pdf_multivariate(x, mu, sigma):
    size = x.shape[0]
    if size == len(mu) and (size, size) == sigma.shape:
        det = np.linalg.det(sigma)
        if det == 0:
            raise NameError("The covariance matrix can't be singular")

        norm_const = 1.0/ ( np.power((2*np.pi),float(size)/2) * np.power(det,1.0/2) )
        x_mu = x - mu
        inv = np.linalg.inv(sigma)        
        result = np.power(math.e, -0.5 * (x_mu @ inv @ np.transpose(x_mu)))
        return norm_const * result
    else:
        raise NameError(f"The dimensions of the input don't match: {size} != {len(x)} or {sigma.shape}")

X = mat['X']
y = mat['y']
m, n = X.shape

# find the inices where the anomalies and nrmal data are
pos_y_ind = np.where(y == 1)[0]
neg_y_ind = np.where(y != 1)[0]

pos_m = pos_y_ind.shape[0]
neg_m = neg_y_ind.shape[0]

# 60% o the normal examples
X_train = X[neg_y_ind[:int(neg_m*0.60)]]
# conctenate 20% of the normal case then 50% of the anomolous case
X_cv = np.concatenate((X[neg_y_ind[int(neg_m*0.60):int(neg_m*0.80)]], X[pos_y_ind[:int(pos_m*0.50)]]), axis=0)
X_test = np.concatenate((X[neg_y_ind[int(neg_m*0.80):]], X[pos_y_ind[int(pos_m*0.50):]]), axis=0)

mu = np.mean(X_train, axis=0)
sigma = np.std(X_train, axis=0)
cov_mat_cal = (np.transpose(X_train - mu)@(X_train-mu)) / m

x = X_cv[0]

mv = multivariate_normal(mu, cov_mat_cal)

# epsilon is comapared with the probability 
epsilon = 1e-1
cv_m, _ = X_cv.shape
cv_anomalous_start_index = int(neg_m*0.80) - int(neg_m*0.60) # the start index of the anomalous examples from the cross validation set
test_anomalous_start_index = neg_m - int(neg_m*0.80)
false_neg = 0 # total number of negative detection that turn out to be positive
false_pos = 0 # total number anomalous detection that turnsout to be negative
true_pos = 0 # total number of positive detection thats actually a positive
true_neg = 0 # total number of negative detection thats actually negative
# calculate the proba;ities until the start of the anomalous examples
# so that every example is non-anomalous
for i in range(cv_anomalous_start_index):
	current_sample = X_cv[i]
	p = mult_gaus_dist(current_sample, mu, cov_mat_cal)
	# it means an anomaly is detected
	# but since all the examples  are non-anomalous this is consired a false positive
	if p < epsilon:
		false_pos += 1
	else: # anomaly is not detected so its a true negative
		true_neg += 1
# all the examples here are anomalous
for i in range(cv_anomalous_start_index, X_cv.shape[0], 1):
	current_sample = X_cv[i]
	p = mult_gaus_dist(current_sample, mu, cov_mat_cal)
	# an anomaly is deteccted, and it is indeed correct
	if p < epsilon:
		true_pos += 1
	else: # no anomaly is detected, but since all the examles are anomalous this ounts as a false neg
		false_neg += 1 

print(f'precision: {true_pos / (true_pos + false_pos)}')
print(f'recall: {true_pos / (true_pos + false_neg)}')
# print(f'total positive example: {pos_m}')
# print(f'cv: {X_cv.shape}')
# print(f'number of positive exmaple in CV: {X_cv.shape[0] - cv_anomalous_start_index}')
# print(f'there shpuld be: {int(pos_m*0.50)}')
# print(f'numbe of positive example in test: {X_test.shape[0] - test_anomalous_start_index}')