vlambda = 1500.0
input_file = r"C:\! Convex_Optimization\Coding_tasks\!CAMEX\package\CAMEX\camex\addons\cvx\L1_trend_filtering\data\input_data.csv"
%matplotlib qt5

# code from here:
#  https://www.cvxpy.org/examples/applications/l1_trend_filter.html
#  https://stanford.edu/~boyd/papers/pdf/l1_trend_filter.pdf

import numpy as np
import cvxpy as cp
import scipy as scipy
# import cvxopt as cvxopt
import os
import matplotlib.pyplot as plt
plt.close('all')
"""
# parameters used for testing -->
vlambda = 1500

input_file = (os.path.dirname(__file__) + os.path.sep
              + 'data' + os.path.sep + 'input_data.csv')
print("in .../L1_trend_filtering/execute.py")
# <-- parameters used for testing
"""

print('input parameters:')
print('vlambda =', vlambda)
print('input_file =', input_file)

# Load time series data: S&P 500 price log.
y = np.loadtxt(input_file)
n = y.size

# Form second difference matrix.
e = np.ones((1, n))
D = scipy.sparse.spdiags(np.vstack((e, -2*e, e)), range(3), n-2, n)

# Solve l1 trend filtering problem.
x = cp.Variable(shape=n)
obj = cp.Minimize(0.5 * cp.sum_squares(y - x)
                  + vlambda * cp.norm(D@x, 1))
prob = cp.Problem(obj)

# ECOS and SCS solvers fail to converge before
# the iteration limit. Use CVXOPT instead.
prob.solve(solver=cp.CVXOPT, verbose=True)
print('Solver status: {}'.format(prob.status))

# Check for error.
if prob.status != cp.OPTIMAL:
    raise Exception("Solver did not converge!")

print("optimal objective value: {}".format(obj.value))

print('x.size = ', x.size)

# Plot estimated trend with original signal.
plt.figure(figsize=(6, 6))
plt.plot(np.arange(1, n+1), y, 'k:', linewidth=2.0, label='input data')
plt.plot(np.arange(1, n+1), np.array(x.value), 'b-',
         linewidth=1.0, label='piecewise linear estimations')
plt.xlabel('date')
plt.ylabel('price')
plt.legend()
plt.title('$L_1$ trend filtering, $\lambda = $' + str(vlambda))
plt.show()
