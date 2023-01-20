

class Pipe:
    def __init__(self, initial_value=0, name=''):
        self.value = initial_value
        self.initial_value = initial_value
        self.name = name

    def reset(self):
        self.value = self.initial_value

    def set(self, value):
        self.value = value

    def get(self):
        return self.value
