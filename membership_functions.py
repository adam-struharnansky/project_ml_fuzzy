

class MembershipFunction:
    def __init__(self):
        pass

    def y(self, x):
        pass

    def edges(self):
        pass


class TriangleMF(MembershipFunction):
    def __int__(self, left, middle, right):
        super().__init__()
        self.left = left
        self.middle = middle
        self.right = right
        self.left_interval = middle - left
        self.right_interval = right - middle

    def y(self, x):  # todo - verify correctness
        if x <= self.left or x >= self.right:
            return 0
        if x <= self.middle:
            return (x - self.left) / self.left_interval
        return (self.right - x) / self.right_interval

    def edges(self):
        return self.left, self.right


class TrapezoidMF(MembershipFunction):
    def __init__(self, left, top_left, top_right, right):
        super().__init__()
        self.left = left
        self.top_left = top_left
        self.top_right = top_right
        self.right = right
        self.left_interval = top_left - left
        self.right_interval = right - top_right

    def y(self, x):  # todo - verify correctness
        if x <= self.left or x >= self.right:
            return 0
        if self.top_left <= x <= self.top_right:
            return 1
        if x < self.top_left:
            return (x - self.left) / self.left_interval
        return (self.right - x) / self.right_interval

    def edges(self):
        return self.left, self.right
