import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd

xideal = list([0,1,2,3,4,5,4,3,2,1])
xgemessen = list([-0.1,1.3,1.9,3,4.01,5.1,4,3.01,2,1.0])
ygemessen = list([1,2,3,4,5,6,3,2,1,0])

f = interpolate.interp1d(xgemessen, ygemessen)
yinter = f(xideal)

#yinter = np.interp(xideal, xgemessen, ygemessen, period=360)

# Plot the data
plt.figure()
plt.subplot(2,1,1)
plt.title('gemessen')
plt.plot(xgemessen, ygemessen, c = 'C0', marker = '.')
# plt.xlim(-0.05,0.95)

plt.subplot(2,1,2)
plt.title('interpoliert')
plt.plot(xideal, yinter, c = 'C1', marker = '.')
# plt.xlim(-0.05,0.95)

plt.tight_layout()

plt.show()