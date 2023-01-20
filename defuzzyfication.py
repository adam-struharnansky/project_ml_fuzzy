from filter import Filter


class Defuzzify(Filter):
    steps = 100

    def __init__(self, ingoing, outgoing, membership_functions, defuzzyfication_type='bisector'):
        super().__init__(ingoing, outgoing)
        self.membership_functions = membership_functions
        self.type = defuzzyfication_type
        self.value = 0
        self.edges = [0, 0]
        for membership_function in membership_functions:
            minimum, maximum = membership_function.edge()
            self.edges[0] = min(self.edges[0], minimum)
            self.edges[1] = max(self.edges[1], maximum)

    def apply_function(self):
        if self.type == 'bisector': # todo optimize
            integral = 0
            dx = (self.edges[1] - self.edges[0]) / self.steps
            for step in range(0, self.steps):
                x = self.edges[0] + dx * step
                maximum = 0
                for membership_function in self.membership_functions:
                    maximum = max(membership_function.y(x), maximum)
                integral += dx * maximum
            integral_half = integral / 2
            integral = 0
            for step in range(0, self.steps):
                x = self.edges[0] + dx * step
                maximum = 0
                for membership_function in self.membership_functions:
                    maximum = max(membership_function.y(x), maximum)
                integral += dx * maximum
                if integral >= integral_half:
                    self.value = x
                    break

    def sent_values(self):
        for pipe in self.outgoing:
            pipe.set(self.value)
