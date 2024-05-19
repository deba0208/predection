import pandas as pd
import numpy as np
import requests
import json
import sys
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
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
model = sm.tsa.arima.ARIMA(df["co"], order=(10, 1, 10), dates=None)
model_fit = model.fit()
fore = model_fit.forecast(steps=100)
new_co2 = list(df["co"])
size = (fore.mean() * 3.5) / 2
myList = [size] * (len(df["co2"])+100)
print(fore)
plt.plot(new_co2)
plt.plot(myList, 'r')
plt.plot(np.arange(len(df["co2"]), len(df["co2"])+100), fore, 'g')
plt.show()
plt.close()
# print(df)
sys.stdout.flush()
