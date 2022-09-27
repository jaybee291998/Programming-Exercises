import numpy as np 
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt 

path = 'train.csv'
df = pd.read_csv(path)
print(df.head())