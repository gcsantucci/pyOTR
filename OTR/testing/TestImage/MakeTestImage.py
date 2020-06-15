import numpy as np
import matplotlib.pyplot as plt
from Figures import Rectangle, RotatedRectangle, Circle

R1 = Rectangle(-3, -1, 0, 4)
R2 = Rectangle(1, 5, -3, -1)
R3 = RotatedRectangle(0, 4, 0, 2, alpha=45., x0=1., y0=1.)

C1 = Circle(-2, 5, 1)
C2 = Circle(7, -2, 2)
C3 = Circle(1, 1, 1)

figures = [R1, R2, R3, C1, C2, C3]


def Passed(x, y):
    for figure in figures:
        if figure.Pass(x, y):
            return True
    return False


nrays = 1_000_000
xmax = 10.
X = []
for i in range(nrays):
    x = xmax * np.random.uniform(-1., 1., 3)
    x[-1] = -50.
    X.append(x)
X = np.array(X)
print(X.shape)

passed = []
reflected = []
for iray in X:
    if Passed(iray[0], iray[1]):
        passed.append(iray)
    else:
        reflected.append(iray)
passed = np.array(passed)
reflected = np.array(reflected)

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
ax.scatter(passed[:, 0], passed[:, 1], c='#00dfff', marker='.', alpha=1)
plt.xticks(np.arange(-xmax, xmax + 1, 1))
plt.yticks(np.arange(-xmax, xmax + 1, 1))
plt.savefig('figs/passed.png')
# plt.show()

print(passed.shape)
np.save(f'../../data/test_images', passed)

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
ax.scatter(reflected[:, 0], reflected[:, 1], c='#00dfff', marker='.', alpha=1)
plt.xticks(np.arange(-xmax, xmax + 1, 1))
plt.yticks(np.arange(-xmax, xmax + 1, 1))
plt.savefig('figs/reflected.png')
# plt.show()

print('Done!')
