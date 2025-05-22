import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from models import db,PredictionResult
from datetime import datetime

def procenten(ticker="AAPL"):

    # Hämta data
    df = yf.download(ticker, start="2020-01-01", end=datetime.now().date())

    # Feature engineering
    df["Tomorrow_Close"] = df["Close"].shift(-1)
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA10"] = df["Close"].rolling(10).mean()
    df["Daily_Change"] = df["Close"].pct_change()
    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)



    df = df.dropna()

    # Features och labels
    X = df[["Close", "MA5", "MA10", "Daily_Change"]]
    y = df["Target"]

    # Walk-forward prediction
    predictions = []
    true_values = []

    longest_lookback = 10
    initial_training_size = max(50,longest_lookback + 20)
    for i in range(initial_training_size, len(df)):
        X_train = X[:i]
        y_train = y[:i]
        
        X_test = X[i:i+1]
        y_test = y[i:i+1]

        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        predictions.append(pred[0])
        true_values.append(y_test.values[0])

    # Utvärdera
    accuracy = accuracy_score(true_values, predictions)

    # Spara i databasen
    result = PredictionResult(ticker=ticker, accuracy=accuracy)
    db.session.add(result)
    db.session.commit()

    return accuracy
