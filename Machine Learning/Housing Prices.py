# Shift + Alt + A

import sys

# used for manipulating directory paths
import os

import matplotlib.pyplot as plt

# Plotting library
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D  # needed to plot 3-D surfaces

# Scientific and vector computation for python
import numpy as np

pathdata = 'ex1data1.txt'
path = os.path.join('/Users/mackt/Python/Machine Learning/Data', pathdata)

print(path)

data = np.loadtxt(path, delimiter=',')
X, y = data[:, 0], data[:, 1]

m = y.size

print(m)

def plotData(x, y):
    fig = plt.figure()
    plt.plot(x, y, 'go', ms=7, mec='k')
    plt.ylabel('Profit in $10,000')
    plt.xlabel('Population of City in 10,000s')
plotData(X, y)

plt.show()

X = np.stack([np.ones(m), X], axis=1)

#Computing J for given theta
def computeCost(X, y, theta):
    J = 0
    h = np.dot(X, theta)
    J = (1/(2 * m)) * np.sum(np.square(np.dot(X, theta) - y))
    return J

J = computeCost(X, y, theta=np.array([0.0, 0.0]))
J1 = J
print('With theta = [0, 0] \nCost computed = %.2f' % J)
print('Expected cost value (approximately) 32.07\n')

J = computeCost(X, y, theta=np.array([-1, 2]))
J2 = J
print('With theta = [-1, 2]\nCost computed = %.2f' % J)
print('Expected cost value (approximately) 54.24\n')

if J1 < J2:
    print('J1 is closer than J2 to minimizing J.\n')
elif J1 > J2:
    print('J2 is closer than J1 to minimizing J.\n')
else:
    print('J1 and J2 are equally close to minimizing J.\n')

def gradientDescent(X, y, theta, alpha, num_iters):
    theta = theta.copy()
    J_history = [] # Use a python list to save cost in every iteration

    for i in range(num_iters):
        theta = theta - (alpha / m) * (np.dot(X, theta) - y).dot(X)
        # save the cost J in every iteration
        J_history.append(computeCost(X, y, theta))
    return theta, J_history

# initialize fitting parameters
theta = np.zeros(2)

# some gradient descent settings
iterations = 1500
alpha = 0.01

theta, J_history = gradientDescent(X ,y, theta, alpha, iterations)
print('Theta found by gradient descent: {:.4f}, {:.4f}'.format(*theta))
print('Expected theta values (approximately): [-3.6303, 1.1664]')

# plot the linear fit
plotData(X[:, 1], y)
pyplot.plot(X[:, 1], np.dot(X, theta), '-')
pyplot.legend(['Training data', 'Linear regression']);
plt.show()

# Predict values for population sizes of 35,000 and 70,000
predict1 = np.dot([1, 3.5], theta)
print('For population = 35,000, we predict a profit of {:.2f}\n'.format(predict1*10000))
predict2 = np.dot([1, 7], theta)
print('For population = 70,000, we predict a profit of {:.2f}\n'.format(predict2*10000))

# grid over which we will calculate J
theta0_vals = np.linspace(-10, 10, 100)
theta1_vals = np.linspace(-1, 4, 100)

# initialize J_vals to a matrix of 0's
J_vals = np.zeros((theta0_vals.shape[0], theta1_vals.shape[0]))

# Fill out J_vals
for i, theta0 in enumerate(theta0_vals):
    for j, theta1 in enumerate(theta1_vals):
        J_vals[i, j] = computeCost(X, y, [theta0, theta1])
# Because of the way meshgrids work in the surf command, we need to
# transpose J_vals before calling surf, or else the axes will be flipped
J_vals = J_vals.T

# surface plot
fig = pyplot.figure(figsize=(12, 5))
ax = fig.add_subplot(121, projection='3d')
ax.plot_surface(theta0_vals, theta1_vals, J_vals, cmap='viridis')
pyplot.xlabel('theta0')
pyplot.ylabel('theta1')
pyplot.title('Surface')

# contour plot
# Plot J_vals as 15 contours spaced logarithmically between 0.01 and 100
ax = pyplot.subplot(122)
pyplot.contour(theta0_vals, theta1_vals, J_vals, linewidths=2, cmap='viridis', levels=np.logspace(-2, 3, 20))
pyplot.xlabel('theta0')
pyplot.ylabel('theta1')
pyplot.plot(theta[0], theta[1], 'go', ms=10, lw=2)
pyplot.title('Contour, showing minimum')
pass

plt.show()

pathdata = 'ex1data2.txt'
path = os.path.join('/Users/mackt/Python/Machine Learning/Data', pathdata)

data = np.loadtxt(path, delimiter=',')
X = data[:, :2]
y = data[:, 2]
m = y.size

# print out some data points
print('{:>8s}{:>8s}{:>10s}'.format('X[:,0]', 'X[:, 1]', 'y'))
print('-'*26)
for i in range(10):
    print('{:8.0f}{:8.0f}{:10.0f}'.format(X[i, 0], X[i, 1], y[i]))

def  featureNormalize(X):
    X_norm = X.copy()
    mu = np.zeros(X.shape[1])
    sigma = np.zeros(X.shape[1])

    mu = np.mean(X, axis = 0)
    sigma = np.std(X, axis = 0)
    X_norm = (X - mu) / sigma

    return X_norm, mu, sigma

X_norm, mu, sigma = featureNormalize(X)

print('Computed mean:', mu)
print('Computed standard deviation:', sigma)

def computeCostMulti(X, y, theta):
    m = y.shape[0]
    J = 0

    h = np.dot(X, theta)
    J = (1/(2 * m)) * np.sum(np.square(np.dot(X, theta) - y))
    return J

def gradientDescentMulti(X, y, theta, alpha, num_iters):
    m = y.shape[0]
    theta = theta.copy()
    J_history = []

    for i in range(num_iters):
        subt = 0
        subt = (np.dot(X, theta) - y)
        print(X)
        print(subt)
        subt = subt.dot(np.transpose(X))
        subt = subt*(alpha / m)
        theta = theta - subt
        # theta = theta - (alpha / m) * (np.dot(X, theta) - y).dot(np.transpose(X))
        J_history.append(computeCostMulti(X, y, theta))
    return theta, J_history

alpha = 0.1
num_iters = 400

theta = np.zeros(3)
print(theta)
print(X)
theta, J_history = gradientDescentMulti(X, y, theta, alpha, num_iters)

pyplot.plot(np.arange(len(J_history)), J_history, lw=2)
pyplot.xlabel('Number of iterations')
pyplot.ylabel('Cost J')

print('theta computed from gradient descent: {:s}'.format(str(theta)))

X_array = [1, 1650, 3]
X_array[1:3] = (X_array[1:3] - mu) / sigma
price = np.dot(X_array, theta)

print('Predicted price of a 1650 sq-ft, 3 br house (using gradient descent): ${:.0f}'.format(price))

X_array = [1, 1650, 3]
X_array[1:3] = (X_array[1:3] - mu) / sigma
print(X_array[1:3])