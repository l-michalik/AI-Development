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
    preds = model.predict_proba(test[predictors])[:,1]
    preds[preds > 0.6] = 1 # custom logic
    preds[preds <= 0.6] = 0
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

# predictions['Predictions'].value_counts() # show the predictions count

# precision_score(predictions['Target'], predictions['Predictions']) # show the precision score

# predictions['Target'].value_counts() / predictions.shape[0] # show the target count

horizons = [2, 5, 60, 250, 1000]
new_predictors = []

for horizon in horizons:
    rolling_avarages = sp500.rolling(horizon).mean()

    ratio_column = f'Close_{horizon}'
    sp500[ratio_column] = sp500['Close'] / rolling_avarages['Close']

    trend_column = f'Trend_{horizon}'
    sp500[trend_column] = sp500.shift(1).rolling(horizon).sum()["Target"]

    new_predictors += [ratio_column, trend_column]

sp500  = sp500.dropna()

model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)

predictions = backtest(sp500, model, new_predictors)

print(predictions['Predictions'].value_counts())

# print(precision_score(predictions['Target'], predictions['Predictions']))