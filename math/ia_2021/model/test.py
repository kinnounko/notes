import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_table("test.csv", sep='\t')

plt.scatter(df['aaa'], df['test'], marker="x")
plt.show()
