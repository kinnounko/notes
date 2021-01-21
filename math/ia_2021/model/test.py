import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("test.csv")

plt.plot(np.unique(df['aaa']), np.poly1d(np.polyfit(df['aaa'], df['test'], 1))(np.unique(df['aaa'])))
plt.scatter(df['aaa'], df['test'], marker="x")
plt.show()
