
# todo - nastavit tym filtrom, ktore maju iba jeden vystup, aby bol poslany do vsetkych vychadzajucich pipeov
class Filter:
    def __init__(self, ingoing, outgoing):
        self.ingoing = ingoing
        self.outgoing = outgoing
        self.time = 0

    def add_ingoing(self, pipe):
        self.ingoing.append(pipe)

    def add_outgoing(self, pipe):
        self.outgoing.append(pipe)

    def apply_function(self):
        pass

    def sent_values(self):
        pass

    def set_time(self, time):
        self.time = time


class Addition(Filter):
    value = 0

    def apply_function(self):
        self.value = 0
        for pipe in self.ingoing:
            self.value += pipe.get()

    def sent_values(self):
        for pipe in self.outgoing:
            pipe.set(self.value)


class Subtraction(Filter):
    value = 0

    def apply_function(self):
        self.value = self.ingoing[0] - self.ingoing[1]

    def sent_values(self):
        self.outgoing[0].set(self.value)


class Multiplication(Filter):
    value = 0

    def apply_function(self):
        self.value = 0
        for pipe in self.ingoing:
            self.value *= pipe.get()

    def sent_values(self):
        self.outgoing[0].set(self.value)


class Division(Filter):
    value = 0

    def apply_function(self):
        self.value = self.ingoing[0] / self.ingoing[1]

    def sent_values(self):
        self.outgoing[0].set(self.value)


class Derivative(Filter):
    value = 0

    def __init__(self, ingoing, outgoing, step=0.1, initial_value=0):
        super().__init__(ingoing, outgoing)
        if step == 0:
            self.step = 0.1
        else:
            self.step = step
        self.previous_value = initial_value

    def apply_function(self):
        self.value = (self.previous_value - self.ingoing[0].get()) / self.step
        self.previous_value = self.ingoing[0].get()

    def sent_values(self):
        self.outgoing[0].set(self.value)


class Integral(Filter):
    def __init__(self, ingoing, outgoing, step=0.1, initial_value=0):
        super().__init__(ingoing, outgoing)
        if step == 0:
            self.step = 0.1
        else:
            self.step = step
        self.value = initial_value

    def apply_function(self):
        self.value += self.ingoing[0] * self.step

    def sent_values(self):
        self.outgoing[0].set(self.value)


class Constant(Filter):
    def __init__(self, ingoing, outgoing, value):
        super().__init__(ingoing, outgoing)
        self.value = value

    def apply_function(self):
        pass

    def sent_values(self):
        for pipe in self.outgoing:
            pipe.set(self.value)


class Impulse(Filter):
    def __init__(self, ingoing, outgoing, impulses, times):
        super().__init__(ingoing, outgoing)
        self.impulses = impulses
        self.times = times
        self.next = 0
        self.value = 0

    def apply_function(self):
        self.value = 0
        for index in range(self.next, len(self.impulses)):
            if self.times[index] < self.time:
                self.value += self.impulses[index]
            else:
                self.next = index
                break

    def sent_values(self):
        for pipe in self.outgoing:
            pipe.set(self.value)


class Scope(Filter):
    def apply_function(self):
        line = ''
        for pipe in self.ingoing:
            line = line + str(pipe.get())
        print(line)
        # todo - dat tu plot



