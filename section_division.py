import sys
from utils import SectionDivisionMyQueue

SIZE = 60

q = SectionDivisionMyQueue(60)
highest = 0
lowest = 0
prev_section = -1
buy_coin_unit = 0

# 총액이 100만원이라고 했을 때 1분할 가격
ONE_DIVISION_AMOUNT = 1000000 / 10
my_money = 1000000

max_money = my_money
min_money = my_money

buy_count = 0
sell_count = 0


def get_interval_index(start, end, current):
    interval_size = (end - start) / 10
    interval_index = int((current - start) // interval_size) + 1
    # print(start, end, current, interval_index)
    if (interval_index > 10):
        interval_index = 10
    elif (interval_index <= 0):
        interval_index = 0
    return interval_index


filenames = ["./backdata/XRP/hour1/data.csv"]

# 데이터는 다음과 같음
# 시간               , 시가[1], 최고가[2], 최저가[3], 종가[4]
# 2023-04-26T12:32:00, 3333333, 33333333 , 33333333 , 33333333
for filename in filenames:
    with open(filename, 'r') as file:
        for line in file:
            if (q.full()):
                # 전날 기준 20일선이랑 5일선 구하기
                isUpAvg = q.isUpAvg(20)
                isDownAvg = q.isDownAvg(5)
                # isUpAvg = True
                # isDownAvg = True
                CURRENT_PRICE = int(float(line.split(',')[1]))
                ONE_DIVISION_AMOUNT = (my_money + buy_coin_unit * CURRENT_PRICE * 0.9995) / 10
                current_section = get_interval_index(q.getLowest(), q.getHighest(), CURRENT_PRICE)

                if (prev_section < 0):
                    # 첫 매수니까 일단 삼
                    buy_coin_unit += (ONE_DIVISION_AMOUNT / CURRENT_PRICE) * 0.9995
                    my_money -= ONE_DIVISION_AMOUNT
                    # print("BUY !!!!")
                    buy_count += 1
                    # print(prev_section)
                else:
                    # 다음 매수부터는 알고리즘
                    if (prev_section < current_section and isUpAvg):
                        if ((current_section - prev_section) * ONE_DIVISION_AMOUNT < my_money):
                            buy_coin_unit += (ONE_DIVISION_AMOUNT / CURRENT_PRICE) * \
                                (current_section - prev_section) * 0.9995
                            my_money -= (current_section - prev_section) * ONE_DIVISION_AMOUNT
                            buy_count += 1
                            # print("what happen:", (ONE_DIVISION_AMOUNT / CURRENT_PRICE))
                            # print("what happen2:", (current_section - prev_section))
                            # print("buy_coin_unit:", buy_coin_unit)
                            # print("BUY !!!!")

                    elif (prev_section > current_section and isDownAvg):
                        want_sell_unit = (ONE_DIVISION_AMOUNT / CURRENT_PRICE) * \
                            (prev_section - current_section)
                        if (buy_coin_unit >= want_sell_unit):
                            buy_coin_unit -= want_sell_unit
                            my_money += want_sell_unit * CURRENT_PRICE * 0.9995
                        else:
                            my_money += buy_coin_unit * CURRENT_PRICE * 0.9995
                            buy_coin_unit = 0
                        sell_count += 1
                        # print("what happen:", (ONE_DIVISION_AMOUNT / CURRENT_PRICE))
                        # print("what happen2:", (prev_section - current_section))
                        # print("buy_coin_unit:", buy_coin_unit)
                        # print("SELL !!!!")

                prev_section = current_section
                # MDD 계산을 위한 값
                current_money = my_money + buy_coin_unit * CURRENT_PRICE * 0.9995
                if (max_money > current_money):
                    max_money = current_money
                if (min_money < current_money):
                    min_money = current_money

                # print(current_money)
                # print(line)
                # print(q.get()[0])
                # print("isUpAvg20: " + str(isUpAvg20) + " / isDownAvg5: " + str(isDownAvg5))
                # print("my_money:", int(my_money), " / buy_coin_unit", buy_coin_unit)
                # print("current_mony:", int(current_money))
                # print("current_section:", current_section)
                # print("---------------------------------------------------\n\n")
                # print("my_money:", int(current_money))

            q.put([int(float(element)) for element in line.split(",")[1:]])

print(buy_count, sell_count)
print(current_money)
print(int(max_money), int(min_money))
