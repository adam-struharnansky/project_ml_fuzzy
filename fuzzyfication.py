from filter import Filter


class Fuzzify(Filter):
    def __init__(self, ingoing, outgoing, membership_functions, names):
        super().__init__(ingoing, outgoing)
        self.membership_functions = membership_functions
        self.values = [['', 0]] * len(membership_functions)
        self.names = names

    def apply_function(self):
        for i in range(0, len(self.membership_functions)):
            self.values[i] = [self.names[i], self.membership_functions[i].y(self.ingoing[0].get())]

    def sent_values(self):
        for pipe in self.outgoing:
            pipe.set(self.values)
