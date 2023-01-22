

class SimpleEnvironment:
    def __init__(self, filters):
        self.filters = filters

    def add_filter(self, new_filter):
        self.filters.append(new_filter)

    def clear_values(self):
        pass

    def run(self, interval, step):
        self.clear_values()
        current_step = 0
        while current_step < interval:
            for f in self.filters:
                f.set_time(current_step)
            for f in self.filters:
                f.apply_function()
            for f in self.filters:
                f.sent_values()
            current_step += step
        for f in self.filters:
            f.end()
