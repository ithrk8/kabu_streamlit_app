def greeting(name):
    print("Hello,", name)


greeting("World")

import yfinance as yf

# 銘柄(APPLE社)を指定
apl = "AAPL"

# 株価データ取得
stock = yf.download(apl)

# 表示
print(stock)

ticker = "AAPL"

from datetime import datetime

# 開始日と終了日を定義
start = datetime(2023, 1, 1)
end = datetime(2023, 12, 31)

# 株価取得
data = yf.download(ticker, start=start, end=end)

# 日時と調整後の終値をそれぞれ切り出しておく
x = data.index
y = data["Adj Close"]

# 過去データの移動平均(simple moving average)を取る
# 平均化する期間は過去の5,25,75日分
data = data.assign(sma5=y.rolling(window=5).mean())
data = data.assign(sma25=y.rolling(window=25).mean())
data = data.assign(sma75=y.rolling(window=75).mean())

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(40, 30))

# 各データをプロット
plt.plot(x, y, label=ticker)
plt.plot(x, data["sma5"], label="sma5")
plt.plot(x, data["sma25"], label="sma25")
plt.plot(x, data["sma75"], label="sma75")

# ラベルや目盛の設定
plt.xlabel("date", fontsize=40)
plt.ylabel("price", fontsize=40)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid()
plt.legend(fontsize=32)

import streamlit as st
import matplotlib.pyplot as plt
import mpl_finance as mpl
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc

st.pyplot(fig)

fig2 = plt.figure(figsize=(40, 30))

# 横軸を調整
fig2.autofmt_xdate(rotation=90, ha="center")

ax = fig2.add_subplot(1, 1, 1)

# フォーマットに合うように加工
data.insert(0, "index", [i for i in range(len(data))])

# 描画
mpl.candlestick_ohlc(ax, data.values, width=0.5, colorup="r", colordown="b")

# 横軸設定
plt.xticks([x for x in range(len(data))], [x.strftime("%Y-%m-%d") for x in data.index])
locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)

# ラベルや目盛の設定
plt.xlabel("date", fontsize=40)
plt.ylabel("price", fontsize=40)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid()
plt.legend(fontsize=32)
st.pyplot(fig2)

fig3 = plt.figure(figsize=(40, 30))

# barメソッドにするだけ
plt.bar(x, data["Volume"], label="Volume")

# ラベルや目盛の設定
plt.xlabel("date", fontsize=40)
plt.ylabel("Volume", fontsize=40)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid()
plt.legend(fontsize=32)
st.pyplot(fig3)

# 指数移動平均を求めるため期間
FastEMA = 12
SlowEMA = 26
SignalSMA = 9

# MACDとシグナルを計算
data = data.assign(
    MACD=data["Adj Close"].ewm(span=FastEMA).mean()
    - data["Adj Close"].ewm(span=SlowEMA).mean()
)
data = data.assign(Signal=data["MACD"].rolling(SignalSMA).mean())

# プロット
fig4 = plt.figure(figsize=(40, 30))
plt.plot(x, data["MACD"], label="MACD")
plt.plot(x, data["Signal"], label="Signal")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid()
plt.legend(fontsize=32)
st.pyplot(fig4)

import datetime as dt
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance as mpl
import warnings
from matplotlib.dates import DateFormatter

warnings.simplefilter("ignore")

st.title("株価情報集計サイト")
ticker = st.sidebar.text_input("銘柄", "AMZN")
start = st.sidebar.date_input("開始日", dt.date(2020, 1, 1))
end = st.sidebar.date_input("終了日", dt.date(2021, 1, 1))

data = yf.download(ticker, start=start, end=end)

# 日時と調整後の終値をそれぞれ切り出しておく
x = data.index
y = data["Adj Close"]

# 過去データの移動平均(simple moving average)を取る
# 平均化する期間は過去の5,25,75日分
data = data.assign(sma5=y.rolling(window=5).mean())
data = data.assign(sma25=y.rolling(window=25).mean())
data = data.assign(sma75=y.rolling(window=75).mean())

# matplotlibを使ってグラフ化
st.header("調整後の終値及び移動平均株価")
fig = plt.figure(figsize=(40, 30))
plt.plot(x, y, label=ticker)
plt.plot(x, data["sma5"], label="sma5")
plt.plot(x, data["sma25"], label="sma25")
plt.plot(x, data["sma75"], label="sma75")
plt.xlabel("date", fontsize=40)
plt.ylabel("price", fontsize=40)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid()
plt.legend(fontsize=32)

# streamlitにはmatplotlibで描画した図を出力する関数がある
st.pyplot(fig)

# ロウソクチャート
st.header("ロウソクチャート")
fig2 = plt.figure(figsize=(40, 30))
fig2.autofmt_xdate(rotation=90, ha="center")
ax = fig2.add_subplot(1, 1, 1)
data.insert(0, "index", [i for i in range(len(data))])
mpl.candlestick_ohlc(ax, data.values, width=0.5, colorup="r", colordown="b")
plt.xticks([x for x in range(len(data))], [x.strftime("%Y-%m-%d") for x in data.index])
locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)
plt.xlabel("date", fontsize=40)
plt.ylabel("price", fontsize=40)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid()
st.pyplot(fig2)

# 出来高の棒グラフ
st.header("出来高グラフ")
fig3 = plt.figure(figsize=(40, 30))
plt.bar(x, data["Volume"], label="Volume")
plt.xlabel("date", fontsize=40)
plt.ylabel("Volume", fontsize=40)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid()
plt.legend(fontsize=32)
st.pyplot(fig3)

# MACDの計算
st.header("MACD")
FastEMA = 12
SlowEMA = 26
SignalSMA = 9
data = data.assign(
    MACD=data["Adj Close"].ewm(span=FastEMA).mean()
    - data["Adj Close"].ewm(span=SlowEMA).mean()
)
data = data.assign(Signal=data["MACD"].rolling(SignalSMA).mean())

fig4 = plt.figure(figsize=(40, 30))
plt.plot(x, data["MACD"], label="MACD")
plt.plot(x, data["Signal"], label="Signal")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid()
plt.legend(fontsize=32)
st.pyplot(fig4)
