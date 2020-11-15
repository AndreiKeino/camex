# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 12:52:08 2020

@author: Andrei
"""


import numpy as np
import pandas as pd
import os


np.random.seed(1)
n = 10

columns = ['asset_' + str(i + 1) for i in range(n)]
mu = np.abs(np.random.randn(n, 1))
Sigma = np.random.randn(n, n)
Sigma = Sigma.T.dot(Sigma)

df_mu = pd.DataFrame(data = mu.T, index = [0], columns = columns)
print(df_mu)

filename = (os.path.dirname(__file__) + os.path.sep
            + 'data' + os.path.sep + 'mu_data.csv')

df_mu.to_csv(filename, index = False)

df_sigma = pd.DataFrame(data = Sigma, index = range(n), columns = columns)
print(df_sigma)
filename = (os.path.dirname(__file__) + os.path.sep
            + 'data' + os.path.sep + 'sigma_data.csv')
df_sigma.to_csv(filename, index = False)



