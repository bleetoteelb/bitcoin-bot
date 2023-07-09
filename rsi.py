import sys
import 'utils/MyQueue'

# 초기 자본
START_AMOUNT = 10000000
MY_AMOUNT = START_AMOUNT

# 단순이동평균(simple moving average, SMA)


SIZE = 14
q = MyQueue(SIZE)
# Average Up
au = 0
auq = MyQueue(SIZE)
# Average Down
ad = 0
adq = MyQueue(SIZE)

# over_sell : 과매도
# normal : 평균
# over_buy : 과매수
status = ""

# 데이터는 다음과 같음
# 시간               , 시가[1], 최고가[2], 최저가[3], 종가[4]
# 2023-04-26T12:32:00, 3333333, 33333333 , 33333333 , 33333333
# with open("./backdata/bitcoin/day/data.csv", 'r') as file:
cnt = 500
with open("./backdata/bitcoin/miniute1/data_202304.csv", 'r') as file:
    # window의 크기는 14
    for line in file:
        if (cnt == 0):
            sys.exit()
        else:
            cnt -= 1
        splited = line.split(',')
        current_price = int(float(splited[4]))
        # 종가만을 활용함
        if (q.empty()):
            q.put(current_price)
            auq.put(0)
            adq.put(0)
            continue
        else:
            au_first = auq.getFirst()
            ad_first = adq.getFirst()
            previous_data = q.get()
            q.put(current_price)

            if (current_price - previous_data > 0):
                auq.put(current_price - previous_data)
                adq.put(0)
            else:
                adq.put(previous_data - current_price)
                auq.put(0)

            au = auq.sum() / SIZE
            ad = adq.sum() / SIZE

            # rsi = au * 100 / (au + ad)

            if (au + ad > 0):
                # print(int(au * 100 / (au + ad)))
                print(current_price)
                # print("RSI : ", "{:.5f}".format(au * 100 / (au + ad)))

# 남은 것들 현재가로 일괄 판매
# for order in buy_orders:
#     MY_AMOUNT += order[1] * current_price * 0.9995
#
# print("last price          :", current_price)
# print("total_fee           :", total_fee)
# print("total_buy_count     :", total_buy_count)
# print("total_sell_count    :", total_sell_count)
# print("Profit              :", MY_AMOUNT - START_AMOUNT)
# print("Profit              :", (MY_AMOUNT - START_AMOUNT) / START_AMOUNT * 100, "%")
