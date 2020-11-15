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
np.random.seed(1)

# input variable
marker_1 = 29

# input variable
marker_2 = 40

# <-- parameters used for testing
"""

print('script input parameters:')
print('mu_fname = ', mu_fname)
print('sigma_fname = ', sigma_fname)
print('marker_1 = ', marker_1)
print('marker_2 = ', marker_2)

df_mu = pd.read_csv(mu_fname)
df_sigma = pd.read_csv(sigma_fname)

mu = df_mu.to_numpy().T
Sigma = df_sigma.to_numpy()

# checks:

assert mu.shape[1] == 1, 'the mean return vector seconf dimension not equal to 1'
assert mu.shape[0] == Sigma.shape[0], 'the mean return vector and the covariance matrix dimensions did not match'
assert Sigma.shape[0] == Sigma.shape[1], 'covariance matrix should be square'
assert np.allclose(Sigma, Sigma.T), 'covariance matrix should be symmetric'
assert np.all(np.linalg.eigvals(Sigma) >= 0), 'covariance matrix should be positive semidefinite'


n = mu.shape[0]

# Long only portfolio optimization.

w = cp.Variable(n)
gamma = cp.Parameter(nonneg=True)
ret = mu.T @ w
risk = cp.quad_form(w, Sigma)
prob = cp.Problem(cp.Maximize(ret - gamma * risk),
                  [cp.sum(w) == 1,
                  w >= 0])

# Compute trade-off curve.
print('Compute trade-off curve')
SAMPLES = 100

assert 0 <= marker_1 < SAMPLES, 'first marker should be >= 0 and < ' + str(SAMPLES)
assert 0 <= marker_2 < SAMPLES, 'second marker should be >= 0 and < ' + str(SAMPLES)

risk_data = np.zeros(SAMPLES)
ret_data = np.zeros(SAMPLES)
gamma_vals = np.logspace(-2, 3, num=SAMPLES)
print('minimum gamma value = ', np.min(gamma_vals))
print('maximum gamma value = ', np.max(gamma_vals))
for i in range(SAMPLES):
    gamma.value = gamma_vals[i]
    prob.solve()
    risk_data[i] = cp.sqrt(risk).value
    ret_data[i] = ret.value
  
# Plot long only trade-off curve.

markers_on = [marker_1, marker_2]
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(risk_data, ret_data, 'g-', 
         label='tradeoff curve for portfolio')
for marker in markers_on:
    plt.plot(risk_data[marker], ret_data[marker], 'bs')
    ax.annotate(r"$\gamma = %.2f$" % gamma_vals[marker], 
                xy=(risk_data[marker] + .08, ret_data[marker]-.03))
    
for i in range(n):
    if i == 0:
        plt.plot(cp.sqrt(
            Sigma[i, i]).value, mu[i], 'ro', 
            label = "individual stocks")
    else: 
        plt.plot(cp.sqrt(Sigma[i, i]).value, mu[i], 'ro')
        
plt.title('long only trade-off curve')    
plt.xlabel('Standard deviation')
plt.ylabel('Return')
plt.legend()
plt.show()

# Plot return distributions for two points on the trade-off curve 
# for normal distribution.

plt.figure()
for midx, idx in enumerate(markers_on):
    gamma.value = gamma_vals[idx]
    prob.solve()
    std = np.sqrt(risk.value)
    x = np.linspace(-2, 5, 1000)
    plt.plot(x, spstats.norm.pdf(x, ret.value, std), 
             label=r"PDF for $\gamma = %.2f$" % gamma.value)

    print('marker = ', idx)
    print('gamma value for marker = ', gamma_vals[idx])
    print('expected return for marker = ', ret.value[0])
    print('standard deviation for marker = ', std)
    print('probability of loss for normal distribution for marker = ',
          spstats.norm.cdf(0, ret.value, std)[0])
        

plt.xlabel('Return')
plt.ylabel('Density')
plt.legend(loc='upper right')
plt.title('Probablilty density of portfolio return for normal distribution')
plt.show()
