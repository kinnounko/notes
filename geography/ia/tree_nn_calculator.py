import pandas as pd

treedataset = "/home/octo/les-arbres.csv"
df = pd.read_csv(treedataset)

# Show dataframe
df1 = df[df['arr'] == 'PARIS 16E ARRDT']
df2 = df[df['arr'] == 'PARIS 7E ARRDT']
df = pd.merge(df1, df2, how='outer')

#create JSON file 
json_file = df.to_json(orient='records') 

#export JSON file
with open('trees.json', 'w') as f:
    f.write(json_file)