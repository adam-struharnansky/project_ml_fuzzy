import matplotlib.pyplot as plt


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

    def end(self):
        pass


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
        self.value = self.ingoing[0].get() - self.ingoing[1].get()

    def sent_values(self):
        for pipe in self.outgoing:
            pipe.set(self.value)


class Multiplication(Filter):
    value = 0

    def apply_function(self):
        self.value = 0
        for pipe in self.ingoing:
            self.value *= pipe.get()

    def sent_values(self):
        for pipe in self.outgoing:
            pipe.set(self.value)


class Division(Filter):
    value = 0

    def apply_function(self):
        self.value = self.ingoing[0] / self.ingoing[1]

    def sent_values(self):
        for pipe in self.outgoing:
            pipe.set(self.value)


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
        for pipe in self.outgoing:
            pipe.set(self.value)


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
        for pipe in self.outgoing:
            pipe.set(self.value)


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
    def __init__(self, ingoing, outgoing, name='', visualise=True,):
        super().__init__(ingoing, outgoing)
        self.visualise = visualise
        self.values = []
        for _ in range(len(ingoing)):
            self.values.append([])
        self.xs = []
        self.name = name

    def apply_function(self):
        self.xs.append(self.time)
        for i in range(0, len(self.ingoing)):
            self.values[i].append(self.ingoing[i].get())

    def end(self):
        if self.visualise:
            for i in range(0, len(self.ingoing)):
                plt.plot(self.xs, self.values[i], label=self.ingoing[i].name)
            plt.title(self.name)
            plt.legend()
            plt.show()


class Gain(Filter):
    def __init__(self, ingoing, outgoing, gain=1):
        super().__init__(ingoing, outgoing)
        self.value = 0
        self.gain = gain

    def apply_function(self):
        self.value = self.ingoing[0] * self.gain

    def sent_values(self):
        self.apply_function()
        for pipe in self.outgoing:
            pipe.set(self.value)
