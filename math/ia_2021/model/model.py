import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def filter_time(df, threshold):
    filter_df = df.loc[df.year > threshold].copy()
    return filter_df


def filter_distance(df, threshold):
    filter_df = df.loc[df['distance from source (km)'] < threshold].copy()
    return filter_df


def filter_doubtful(df):
    filter_df = df.loc[df['doubtful runup'] != 'y'].copy()
    return filter_df


def calculate_mean(x):
    x['weight'] * x['maximum water height (m)']


def weighted_mean_height(df):
    return df.groupby('earthquake magnitude', as_index=True).apply(lambda x: (x['weight'] * x['maximum water height (m)']).mean())


def get_droppable(df, whitelist):
    to_drop = []
    for (columnName, columnData) in df.iteritems():
        if columnName not in whitelist:
            to_drop.append(columnName)
    return to_drop


if __name__ == "__main__":
    df = pd.read_table("dataset/runups.tsv", sep='\t')
    df.columns = df.columns.str.lower()

    # Filter data points before installation of
    filter_df = filter_time(df, threshold=1960)

    # No doubtful runups.
    filter_df = filter_doubtful(filter_df)

    # Drop all entries with no reported wave height
    filter_df = filter_df.dropna(how='any', subset=['maximum water height (m)'])

    # Filter waves originating from a certain distance away
    # filter_df = filter_distance(filter_df, 30)

    filter_df = filter_df.drop(get_droppable(filter_df,
                                             ['year', 'mo', 'earthquake magnitude', 'distance from source (km)',
                                              'tsunami event validity',
                                              'maximum water height (m)']), axis=1)

    filter_df['weight'] = 1 - filter_df['distance from source (km)'] / filter_df['distance from source (km)'].max()

    filter_df = weighted_mean_height(filter_df)

    filter_df.to_csv("test.csv")

    print(filter_df)
    
    plt.scatter(filter_df['earthquake magnitude'], filter_df['maximum water height (m)'], marker="x")
    plt.show()
