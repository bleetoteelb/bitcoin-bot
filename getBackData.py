import csv
import config
import calendar
import pyupbit
import datetime
import time

upbitObject = pyupbit.Upbit(config.access_key, config.secret_key)


def write_to_csv(filename, d):
    with open(filename, 'a', newline='') as file:
        for item in d:
            file.write(str(item) + '\n')
        # writer = csv.writer(file)
        # writer.writerow(d)


filename_prefix = "backdata"


def get_last_day(year, month):
    return calendar.monthrange(year, month)[1]


# miniute1 data
def getMinute1(upbit):
    year = [2020, 2021, 2022]
    # month = [1, 2, 3, 4]
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    target_data_list = []
    for yyyy in year:
        for mm in month:
            last_day = get_last_day(yyyy, mm)
            # print(yyyy, mm, ":", get_last_day(yyyy, mm))
            for i in range(last_day):
                target_data_list.append(str(yyyy) + str(mm).zfill(2) + str(i + 1).zfill(2))

    # to 를 20230528 로 주면 28일 9시 이전 기준으로 자료를 전달함
    for date in target_data_list:
        print(date)
        # print(date[0:6])
        df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=60 * 24, to=date)

        result = []
        for idx, (ii, row) in zip(list(df.index), df.iterrows()):
            values = [str(row['open']), str(row['high']), str(row['low']), str(row['close'])]
            result.append(','.join([idx.strftime('%Y-%m-%dT%H:%M:%S')] + values))

        write_to_csv("data_" + date[0:6] + ".csv", result)


# week data
def getWeek(upbit):
    df = pyupbit.get_ohlcv("KRW-BTC", count=125, interval="week", to="20230430")
    result = []
    for idx, (ii, row) in zip(list(df.index), df.iterrows()):
        values = [str(row['open']), str(row['high']), str(row['low']), str(row['close'])]
        result.append(','.join([idx.strftime('%Y-%m-%dT%H:%M:%S')] + values))
    write_to_csv("./backdata/bitcoin/week/data.csv", result)


def getDay(upbit):
    first_day = datetime.datetime.strptime("2021-02-19", "%Y-%m-%d")
    for _ in range(0, 4):
        result = []
        first_day = first_day + datetime.timedelta(days=200)
        day_format = first_day.strftime("%Y%m%d")
        df = pyupbit.get_ohlcv("KRW-BTC", count=200, interval="day", to=day_format)
        for idx, (ii, row) in zip(list(df.index), df.iterrows()):
            values = [str(row['open']), str(row['high']), str(row['low']), str(row['close'])]
            result.append(','.join([idx.strftime('%Y-%m-%dT%H:%M:%S')] + values))
        write_to_csv("./backdata/bitcoin/day/data.csv", result)


def getHour(upbit):
    # first_day = datetime.datetime.strptime("2020-12-24", "%Y-%m-%d")
    last_day = datetime.datetime.strptime("2023-07-01", "%Y-%m-%d")
    first_day = last_day - datetime.timedelta(days=920)
    cnt = 114
    retry = False

    while (cnt >= 0):
        time.sleep(5)
        try:
            result = []
            if (not retry):
                first_day = first_day + datetime.timedelta(days=8)
                retry = False
            day_format = first_day.strftime("%Y%m%d")
            print(first_day, day_format)
            df = pyupbit.get_ohlcv("KRW-XRP", count=192, interval="minute60", to=day_format)
            for idx, (ii, row) in zip(list(df.index), df.iterrows()):
                values = [str(row['open']), str(row['high']), str(row['low']), str(row['close'])]
                result.append(','.join([idx.strftime('%Y-%m-%dT%H:%M:%S')] + values))
            write_to_csv("./backdata/XRP/hour1/data.csv", result)
            cnt -= 1
        except AttributeError:
            retry = True
            print(df)
            time.sleep(30)


getHour(upbitObject)
