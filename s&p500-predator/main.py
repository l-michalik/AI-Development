import yfinance as yf

sp500 = yf.Ticker('^GSPC')
sp500 = sp500.history(period='max')

# print(sp500) # show the data 

# print(sp500.index) # show S&P 500 indexes

# print(sp500.plot.line(y='Close', use_index=True)) # show the S&P 500 close price graph

del sp500['Dividends']
del sp500['Stock Splits']

sp500['Tommorow'] = sp500['Close'].shift(-1)
sp500['Target'] = (sp500['Tommorow'] > sp500['Close']).astype(int)

sp500 = sp500.loc["1980-01-01":].copy()

from sklearn.ensemble import RandomForestClassifier
import pandas as pd

model = RandomForestClassifier(n_estimators=100, min_samples_split=100, random_state=1) 

train = sp500.iloc[:-100]
test = sp500.iloc[-100:]

predictors = ["Close", "Volume", "Open", "High", "Low"]

model.fit(train[predictors], train['Target'])

RandomForestClassifier(min_samples_split=100, random_state=1)

from sklearn.metrics import precision_score

preds = model.predict(test[predictors])

preds = pd.Series(preds, index=test.index)

precision_score(test['Target'], preds)

combined = pd.concat([test['Close'], preds], axis=1)
combined.plot()

def predict(train, test, predictors, model):
    model.fit(train[predictors], train['Target'])
    preds = model.predict(test[predictors])
    preds = pd.Series(preds, index=test.index, name="Predictions")
    combined = pd.concat([test['Target'], preds], axis=1)
    return combined

def backtest(data, model, predictors, start=2500, step=250): # 10 years of data
    all_predictions = []
    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+step)].copy()
        preds = predict(train, test, predictors, model)
        all_predictions.append(preds)
    return pd.concat(all_predictions)

predictions = backtest(sp500, model, predictors)

predictions["Predictions"].value_counts()

print(predictions['Predictions'].value_counts()) # show the predictions