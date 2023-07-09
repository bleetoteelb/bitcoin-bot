# import config
# import pyupbit
# import time
# import datetime
# import math
# import logging
import sys
import queue

# import numpy as np
# import pandas as pd


# upbit = pyupbit.Upbit(config.access_key, config.secret_key)
#
# tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-LTC"]

# print(pyupbit.get_current_price("KRW-BTC"))
# print(pyupbit.get_current_price(tickers))

# 시가, 고가, 저가, 종가, 거래량, 시총(?) 조회
# df = pyupbit.get_ohlcv("KRW-BTC")
# print(df.tail())

# 현재 자산 가져오기
# print(upbit.get_balance("KRW"))
# print(upbit.get_balance("KRW-BTC"))


# one_minute_btc = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=30)
# print(one_minute_btc)

# grid 최저가
LOW_WATERMARK  = 10000000
# grid 최고가
HIGH_WATERMARK = 100000000

# 몇개로 구간을 나눌것인지?
TARGET_GRID = 500

# 초기 자본
START_AMOUNT = 10000000
MY_AMOUNT = START_AMOUNT

CURRENT_PRICE = 0
INTERVAL = (HIGH_WATERMARK - LOW_WATERMARK) / TARGET_GRID

# filenames = ["data_202301.csv", "data_202302.csv", "data_202303.csv", "data_202304.csv"]
filenames = []
for i in range(2020, 2023):
    for ii in range(1, 13):
        filenames.append("data_" + str(i) + str(ii).zfill(2) + ".csv")
filenames.append("data_202301.csv")
filenames.append("data_202302.csv")
filenames.append("data_202303.csv")
filenames.append("data_202304.csv")

# print(filenames)
with open(filenames[0], 'r') as file:
    line = file.readline()
    CURRENT_PRICE = int(float(line.split(',')[1]))

PROFIT_PER_GRID = ((HIGH_WATERMARK - LOW_WATERMARK) / TARGET_GRID) / CURRENT_PRICE * 100 - 0.1
AMOUNT_PER_GRID = MY_AMOUNT / TARGET_GRID

print("설정한 LOW_WATERMARK  : ", LOW_WATERMARK)
print("설정한 HIGH_WATERMARK : ", HIGH_WATERMARK)
print("설정한 설정구간 개수  : ", TARGET_GRID)
print("GRID            간격  : ", INTERVAL)
print("한 줄당 거래금        : ", AMOUNT_PER_GRID)
print("한 줄당 수익          : ", "{:.5f}".format(PROFIT_PER_GRID), "%")
print("시작 가격             : ", CURRENT_PRICE)
# is_test_continue = input("실험을 진행하시겠습니까?  (y/N) : ")
# if not (is_test_continue == "Y" or is_test_continue == "y"):
#     sys.exit()


current_price = CURRENT_PRICE
# 큐에는 지금 구매한 주문이 들어감
# [ 팔아야할 가격, 구매수량 ]
buy_orders = []

# 초기 구매
multiple = 1
while current_price < HIGH_WATERMARK:
    buy_orders.append([current_price + INTERVAL, AMOUNT_PER_GRID * 0.9995 / CURRENT_PRICE])
    MY_AMOUNT -= AMOUNT_PER_GRID
    multiple += 1
    current_price += INTERVAL

buy_orders.reverse()
# for b in buy_orders:
#     print(b)

# sys.exit()

next_buy_price = CURRENT_PRICE - INTERVAL
total_fee = (multiple - 1) * AMOUNT_PER_GRID * 0.0005
total_buy_count = multiple - 1
total_sell_count = 0
# 데이터는 다음과 같음
# 시간               , 시가[1], 최고가[2], 최저가[3], 종가[4]
# 2023-04-26T12:32:00, 3333333, 33333333 , 33333333 , 33333333
timeline_cnt = 0
for d in filenames:
    # print(d)
    with open(d, 'r') as file:
        for line in file:
            splited = line.split(',')
            current_price = int(float(splited[4]))

            # print("----------------------------------------------")
            # print("current_price  : ", current_price)
            # print("next_buy_price : ", next_buy_price)
            # print("last_buy_order : ", buy_orders[-1])
            while (int(float(splited[4])) >= LOW_WATERMARK and int(float(splited[4])) <= next_buy_price):
                # print("BUY!! ", next_buy_price)
                buy_orders.append([next_buy_price + INTERVAL, AMOUNT_PER_GRID * 0.9995 / next_buy_price])
                MY_AMOUNT -= AMOUNT_PER_GRID
                total_fee += AMOUNT_PER_GRID * 0.0005
                next_buy_price -= INTERVAL
                total_buy_count += 1

            while (len(buy_orders) > 0 and int(float(splited[4])) >= buy_orders[-1][0]):
                # print("SELL!! ", next_buy_price)
                # print(buy_orders[-1], buy_orders[-1][0] * buy_orders[-1][1])
                MY_AMOUNT += buy_orders[-1][0] * buy_orders[-1][1] * 0.9995
                total_fee += buy_orders[-1][0] * buy_orders[-1][1] * 0.0005
                buy_orders.pop()
                next_buy_price += INTERVAL
                total_sell_count += 1
            timeline_cnt += 1
            if (timeline_cnt == 1440):
                timeline_cnt = 0
                tmp_total_amount = MY_AMOUNT
                for order in buy_orders:
                    tmp_total_amount += current_price * order[1] * 0.9995
                print(int(tmp_total_amount))

# 남은 것들 현재가로 일괄 판매
for order in buy_orders:
    MY_AMOUNT += order[1] * current_price * 0.9995

print("last price          :", current_price)
print("total_fee           :", total_fee)
print("total_buy_count     :", total_buy_count)
print("total_sell_count    :", total_sell_count)
print("Profit              :", MY_AMOUNT - START_AMOUNT)
print("Profit              :", (MY_AMOUNT - START_AMOUNT) / START_AMOUNT * 100, "%")
