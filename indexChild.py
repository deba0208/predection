import pandas as pd
import numpy as np
import requests
import json
import sys
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns


def arima_forecast(df, column, order, steps):
    # Fit ARIMA model
    model = sm.tsa.arima.ARIMA(df[column], order=order)
    model_fit = model.fit()

    # Forecast
    forecast = model_fit.forecast(steps=steps)
    return forecast


url = "https://deba0208-server.onrender.com/data"
r = requests.get(url)
data = r.json()
df = pd.DataFrame(data)
df = df.drop(columns=['_id', '__v'])
df.dropna(subset=['time', 'AQI'], inplace=True)
df.loc[:, ['nh4']] = np.where(df['nh4'] < 0, df['nh4'].median(), df['nh4'])
df[["time", "date"]] = df["time"].str.split(" ", expand=True)
df = df[["date", "time", "co2", "co", "nh4", "pm25",
         "TVOC", "Temperature", "Humidity", "AQI"]]
df = df.tail(30)

# model = sm.tsa.arima.ARIMA(df["co2"], order=(10, 1, 10), dates=None)
# model_fit = model.fit()
# fore = model_fit.forecast(steps=100)
# size = (fore.mean() * 3.5) / 2
# new_co2 = list(df["co"])
# myList = [size] * (len(df["co2"])+100)
forecast_steps = 100
arima_order = (1, 1, 1)
co2 = arima_forecast(df, "co2", arima_order, forecast_steps)
aqi = arima_forecast(df, "AQI", arima_order, forecast_steps)
tvoc = arima_forecast(df, "TVOC", arima_order, forecast_steps)

co2 = (co2.mean() * 3.5) / 2
aqi = (aqi.mean() * 3.5) / 2
tvoc = (tvoc.mean() * 3.5) / 2
data_to_send = {
    "co2": co2,
    "aqi": aqi,
    "tvoc": tvoc
}
print(json.dumps(data_to_send))
sys.stdout.flush()
# plt.plot(new_co2)
# plt.plot(myList, 'r')
# plt.plot(np.arange(len(df["co2"]), len(df["co2"])+100), fore, 'g')
# plt.show()
# plt.close()
# print(df)
