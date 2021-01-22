import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def polyfit(x, y, degree):
    results = {}

    coeffs = np.polyfit(x, y, degree)

     # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = np.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot

    return results


df = pd.read_csv("test.csv")
power = 1


print(polyfit(df['aaa'], df['test'], power))

plt.plot(np.unique(df['aaa']), np.poly1d(np.polyfit(df['aaa'], df['test'], power))(np.unique(df['aaa'])))
plt.scatter(df['aaa'], df['test'], marker="x")
plt.show()
