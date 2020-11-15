mu_fname = r"C:\! Convex_Optimization\Coding_tasks\!CAMEX\package\CAMEX\camex\addons\cvx\Portfolio_optimization_2\data\mu_data.csv"
sigma_fname = r"C:\! Convex_Optimization\Coding_tasks\!CAMEX\package\CAMEX\camex\addons\cvx\Portfolio_optimization_2\data\sigma_data.csv"
%matplotlib qt5

# https://colab.research.google.com/github/cvxgrp/cvx_short_course/blob/master/applications/portfolio_optimization.ipynb

import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
import pandas as pd
import os
import scipy.stats as spstats


plt.close('all')

"""
# parameters used for testing -->
# input variable
mu_fname = (os.path.dirname(__file__) + os.path.sep
            + 'data' + os.path.sep + 'mu_data.csv')

# input variable
sigma_fname = (os.path.dirname(__file__) + os.path.sep
            + 'data' + os.path.sep + 'sigma_data.csv')

# <-- parameters used for testing
"""

print('script input parameters:')
print('mu_fname = ', mu_fname)
print('sigma_fname = ', sigma_fname)


df_mu = pd.read_csv(mu_fname)
df_sigma = pd.read_csv(sigma_fname)

mu = df_mu.to_numpy().T
Sigma = df_sigma.to_numpy()

# checks:

assert mu.shape[1] == 1, 'the mean return vector second dimension not equal to 1'
assert mu.shape[0] == Sigma.shape[0], 'the mean return vector and the covariance matrix dimensions did not match'
assert Sigma.shape[0] == Sigma.shape[1], 'covariance matrix should be square'
assert np.allclose(Sigma, Sigma.T), 'covariance matrix should be symmetric'
assert np.all(np.linalg.eigvals(Sigma) >= 0), 'covariance matrix should be positive semidefinite'


n = mu.shape[0]

w = cp.Variable(n)
gamma = cp.Parameter(nonneg=True)
ret = mu.T @ w
risk = cp.quad_form(w, Sigma)
prob = cp.Problem(cp.Maximize(ret - gamma * risk),
                  [cp.sum(w) == 1,
                  w >= 0])

# Portfolio optimization with leverage limit.
Lmax = cp.Parameter()
prob = cp.Problem(cp.Maximize(ret - gamma*risk), 
               [cp.sum(w) == 1, 
                cp.norm(w, 1) <= Lmax])

# Compute trade-off curve for each leverage limit.
L_vals = [1, 2, 4]
SAMPLES = 100
risk_data = np.zeros((len(L_vals), SAMPLES))
ret_data = np.zeros((len(L_vals), SAMPLES))
gamma_vals = np.logspace(-2, 3, num=SAMPLES)
w_vals = []
for k, L_val in enumerate(L_vals):
    for i in range(SAMPLES):
        Lmax.value = L_val
        gamma.value = gamma_vals[i]
        prob.solve(solver=cp.SCS)
        risk_data[k, i] = cp.sqrt(risk).value
        ret_data[k, i] = ret.value
        
# Plot trade-off curves for each leverage limit.
for idx, L_val in enumerate(L_vals):
    plt.plot(risk_data[idx,:], ret_data[idx,:], label=r"$L^{\max}$ = %d" % L_val)
for w_val in w_vals:
    w.value = w_val
    plt.plot(cp.sqrt(risk).value, ret.value, 'bs')
plt.xlabel('Standard deviation')
plt.ylabel('Return')
plt.legend(loc='lower right')
plt.title('Trade - off curves for different leverage limits')
plt.show()        
