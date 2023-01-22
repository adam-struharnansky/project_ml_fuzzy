from fuzzy_m import Rule


def create_rules(names, values, output_values):
    result = []
    for x in range(0, len(values[0])):
        for y in range(0, len(values[1])):
            text = 'IF ' + str(names[0]) + ' is ' + values[0][x] + ' and ' + str(names[1]) + ' is ' + values[1][y] + \
                   ' THEN ' + 'output' + ' is ' + output_values[0]
            result.append(text)
    return result


def random_search(environment, fuzzy_rules, names, values, output_values):
    rules = create_rules(names, values, output_values)
    fuzzy_rules.clear_rules()
    for rule in rules:
        fuzzy_rules.add_rule(rule)
    environment.run(20, 0.1)
