import scipy.io
import numpy as np

def get_dataset(path):
# loa the data from the file
	mat = scipy.io.loadmat(path)

	X = mat['X']
	y = mat['y']
	m, n = X.shape

	# find the inices where the anomalies and nrmal data are
	pos_y_ind = np.where(y == 1)[0]
	neg_y_ind = np.where(y == 0)[0]

	pos_m = pos_y_ind.shape[0]
	neg_m = neg_y_ind.shape[0]

	# 60% o the normal examples
	X_train = X[neg_y_ind[:int(neg_m*0.60)]]
	# conctenate 20% of the normal case then 50% of the anomolous case
	X_cv = np.concatenate((X[neg_y_ind[int(neg_m*0.60):int(neg_m*0.80)]], X[pos_y_ind[:int(pos_m*0.50)]]), axis=0)
	X_test = np.concatenate((X[neg_y_ind[int(neg_m*0.80):]], X[pos_y_ind[int(pos_m*0.50):]]), axis=0)

	y_train = np.zeros((int(neg_m*0.60), 1))
	cv_zero = np.zeros((int(neg_m*0.80) - int(neg_m*0.60), 1))
	cv_ones = np.ones((int(pos_m*0.50), 1))
	y_cv = np.concatenate((cv_zero, cv_ones), axis=0)
	test_zero = np.zeros((neg_m - int(neg_m*0.80), 1))
	test_ones = np.ones((int(pos_m*0.50), 1))
	y_test = np.concatenate((test_zero, test_ones), axis=0)

	return X_train, y_train, X_cv, y_cv, X_test, y_test
