import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def model_output():
    
    df = pd.read_csv('heart.csv')

    df['Sex'].replace(['M','F'],[0,1],inplace=True)
    df['ChestPainType'].replace(['TA','ATA','NAP','ASY'],[0,1,2,3],inplace=True)
    df['RestingECG'].replace(['Normal','ST','LVH'],[0,1,2],inplace=True)
    df['ExerciseAngina'].replace(['N','Y'],[0,1],inplace=True)
    df['ST_Slope'].replace(['Up','Flat','Down'],[0,1,2],inplace=True)

    y = df.HeartDisease
    X = df.drop('HeartDisease', axis = 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    reg = LinearRegression().fit(X_train, y_train)
    return reg.coef_


print(model_output())