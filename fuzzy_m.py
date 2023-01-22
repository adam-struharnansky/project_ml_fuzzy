from filter import Filter


class FuzzyRules(Filter):
    def __init__(self, ingoing, outgoing, rules, outgoing_names, aggregation_method='max'):
        super().__init__(ingoing, outgoing)
        self.rules = rules
        self.values = [0] * len(outgoing_names)
        self.names = outgoing_names
        self.type = type
        self.aggregation_method = aggregation_method

    def add_rule(self, rule):
        self.rules.append(Rule(rule))

    def clear_rules(self):
        self.rules = []

    def apply_function(self):
        for i in range(0, len(self.values)):
            self.values[i] = 0

        dictionary = []
        for pipe in self.ingoing:
            for membership in pipe.get():
                dictionary.append([pipe.name, membership[0], membership[1]])

        for rule in self.rules:
            result = rule.apply_rule(dictionary)
            for i in range(0, len(self.names)):
                if self.names[i] == result[1]:
                    self.values[i] = self.aggregate(self.values[i], result[2])

    def aggregate(self, a, b):
        if self.aggregation_method == 'max':
            return max(a, b)

    def sent_values(self):
        for pipe in self.outgoing:
            pipe.set(self.values)


class Rule:
    def __init__(self, text, function_type=''):
        self.left_variables = []
        self.left_values = []
        self.right_variable = ''  # todo pre viac outputov
        self.right_value = ''
        if 'AND' in text:
            self.function = min_and
        else:
            self.function = max_or
        self.set_function(function_type)
        parts = text.split()
        then_occurred = False
        for i in range(0, len(parts)):
            if parts[i] == 'is' or parts[i] == 'IS':
                if then_occurred:
                    self.right_variable = parts[i - 1]
                    self.right_value = parts[i + 1]
                else:
                    self.left_variables.append(parts[i - 1])
                    self.left_values.append(parts[i + 1])
            if parts[i] == 'then' or parts[i] == 'THEN':
                then_occurred = True

    def set_function(self, function_type):
        if function_type == 'product_and':
            self.function = product_and
        elif function_type == 'min_and':
            self.function = min_and
        elif function_type == 'probor':
            self.function = probabilistic_or
        elif function_type == 'max_or':
            self.function = max_or

    def apply_rule(self, dictionary):
        result = -1
        for i in range(0, len(self.left_variables)):
            value = 0
            for line in dictionary:
                if line[0] == self.left_variables[i] and line[1] == self.left_values[i]:
                    value = line[2]
            if result == -1:
                result = value
            else:
                result = self.function(result, value)
        return self.right_variable, self.right_value, result


def product_and(x, y):
    return x * y


def min_and(x, y):
    return min(x, y)


def probabilistic_or(x, y):
    return x + y - x * y


def max_or(x, y):
    return max(x, y)


def fuzzy_not(x):
    return 1 - x
