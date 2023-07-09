from pykrx import stock
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
import sys

# cnt = 500
# BTC 최근 4월 데이터 불러오기
# 데이터는 다음과 같음
# 시간               , 시가[1], 최고가[2], 최저가[3], 종가[4]
# 2023-04-26T12:32:00, 3333333, 33333333 , 33333333 , 33333333
# with open("./backdata/bitcoin/day/data.csv", 'r') as file:
data = []
with open("./backdata/bitcoin/hour1/data.csv", 'r') as file:
    for line in file:
        # if (cnt == 0):
        #     sys.exit()
        # else:
        #     cnt -= 1
        splited = line.split(',')
        data.append([splited[0], splited[4]])



# 학습 모델 생성
model = Prophet()
model.fit(data)

# 예측
future = model.make_future_dataframe(perios=24, freq='H')
forecast = model.predict(future)

# 그래프 그리기
fig1 = model.plot(forecast)
a = add_changepoints_to_plot(fig1.gca(), model, forecast)
