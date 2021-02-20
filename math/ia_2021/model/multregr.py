import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


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

    # Doubtful runups to be removed
    filter_df = filter_doubtful(filter_df)

    # Drop all columns except the ones needed for X1, X2 and the Y variables.
    filter_df = filter_df.drop(
        get_droppable(filter_df,
                      ['earthquake magnitude',
                       'distance from source (km)',
                       'maximum water height (m)']), axis=1)

    # Drop all rows with a NaN value  
    filter_df = filter_df.dropna(how='any')

    # Set X to the independent variables (equivalent to dropping the dependent)
    X = filter_df.drop('maximum water height (m)', 1)

    # Set y to our output column: maximum water height
    y = filter_df['maximum water height (m)']

    # The values to predict y with
    pred = [[5.2, 225]]

    # Fit the values 
    poly = PolynomialFeatures(degree=2)
    X_ = poly.fit_transform(X)
    predict_ = poly.fit_transform(pred)

    # Predict 
    mlr_model = LinearRegression()
    mlr_model.fit(X_, y)
    y_pred = mlr_model.predict(predict_)
    print(y_pred)

    # Print the coefficients and intercept
    theta0 = mlr_model.intercept_
    theta1, theta2, theta3, theta4, theta5, theta6 = mlr_model.coef_
    print(theta0, theta1, theta2, theta3, theta4, theta5, theta6)
