# 최대 큐의 크기를 size 만큼 가지는 myQueue
class MyQueue:
    def __init__(self, size):
        self.queue = []
        # 현재 가장 마지막으로 들어온 데이터의 위치
        self.idx = -1
        self.size = size

    def getFirst(self):
        if (len(self.queue) < self.size):
            return self.queue[0]
        elif (self.idx == self.size - 1):
            return self.queue[0]
        else:
            return self.queue[self.idx + 1]

    def put(self, n):
        if (len(self.queue) < self.size):
            self.queue.append(n)
            self.idx += 1
        else:
            if (self.idx == self.size - 1):
                self.queue[0] = n
                self.idx = 0
            else:
                self.idx += 1
                self.queue[self.idx] = n

    def get(self):
        return self.queue[self.idx]

    def empty(self):
        if (len(self.queue) == 0):
            return True
        else:
            return False

    def full(self):
        if (len(self.queue) == self.size):
            return True
        else:
            return False

    def print(self):
        print("queue:", self.queue)
        # print("idx  :", self.idx)

    def sum(self):
        return sum(self.queue)


