import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score




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

    # Filter data points before installation of WWSSN
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

    # Dataset split:
    # The dataset is split into two parts, a "training" df_train dataset and 
    # an "test" df_eval dataset. The "training" will be used for the 
    # generation of a regression model and the "test" will 
    # be used for the testing of this model, to calculate its accuracy. 
    df_train, df_test = train_test_split(filter_df, test_size=0.3, random_state=42)

    # For the train dataset, 
    # Set X to the independent variables (equivalent to dropping the dependent)
    # Set y to our output column: maximum water height
    X_train = df_train.drop('maximum water height (m)', 1)
    y_train = df_train['maximum water height (m)']

    # The test dataset, idem to the train dataset
    X_test = df_test.drop('maximum water height (m)', 1)
    y_test = df_test['maximum water height (m)']


    # Fit the values to 
    poly = PolynomialFeatures(degree=2)
    X_ = poly.fit_transform(X_train)
    predict_ = poly.fit_transform(X_test)

    # Predict 
    mlr_model = LinearRegression()
    mlr_model.fit(X_, y_train)
    y_pred = mlr_model.predict(predict_)

    print(r2_score(y_test, y_pred))

    # Print the coefficients and intercept
    theta0 = mlr_model.intercept_
    theta1, theta2, theta3, theta4, theta5, theta6 = mlr_model.coef_
    print("Intercept: ", theta0, "Coefficients: ", theta1, theta2, theta3, theta4, theta5, theta6)
