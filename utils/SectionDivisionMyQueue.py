from . MyQueue import MyQueue


# 최대 큐의 크기를 size 만큼 가지는 myQueue
class SectionDivisionMyQueue(MyQueue):
    def __init__(self, size):
        super().__init__(size)

    # 데이터는 다음과 같음
    # 시가[0], 최고가[1], 최저가[2], 종가[3]
    # 3333333, 33333333 , 33333333 , 33333333
    def getLowest(self):
        lowest = float('inf')
        for d in self.queue:
            if (d[1] < lowest):
                lowest = d[1]
        return lowest

    def getHighest(self):
        highest = 0
        for d in self.queue:
            if (d[2] > highest):
                highest = d[2]
        return highest

    # 전일 종가가 전날 xx일선 위에 있는지 여부
    def isUpAvg(self, number):
        sum = 0
        for i in range(self.idx - (number - 1), self.idx + 1):
            sum += self.queue[i][3]
        return (sum / number) < self.queue[self.idx][3]

    # 전일 종가가 전날 xx일선 아래 있는지 여부
    def isDownAvg(self, number):
        sum = 0
        for i in range(self.idx - (number - 1), self.idx + 1):
            sum += self.queue[i][3]
        return (sum / number) < self.queue[self.idx][3]


#
# # 최대 큐의 크기를 size 만큼 가지는 myQueue
# class MyQueue:
#     def __init__(self, size):
#         self.queue = []
#         # 현재 가장 마지막으로 들어온 데이터의 위치
#         self.idx = -1
#         self.size = size
#
#     def getFirst(self):
#         if (len(self.queue) < self.size):
#             return self.queue[0]
#         elif (self.idx == self.size - 1):
#             return self.queue[0]
#         else:
#             return self.queue[self.idx + 1]
#
#     def put(self, n):
#         if (len(self.queue) < self.size):
#             self.queue.append(n)
#             self.idx += 1
#         else:
#             if (self.idx == self.size - 1):
#                 self.queue[0] = n
#                 self.idx = 0
#             else:
#                 self.idx += 1
#                 self.queue[self.idx] = n
#
#     def get(self):
#         return self.queue[self.idx]
#
#     def empty(self):
#         if (len(self.queue) == 0):
#             return True
#         else:
#             return False
#
#     def full(self):
#         if (len(self.queue) == self.size):
#             return True
#         else:
#             return False
#
#     def print(self):
#         print("queue:", self.queue)
#         # print("idx  :", self.idx)
#
#     def sum(self):
#         return sum(self.queue)
#
#
