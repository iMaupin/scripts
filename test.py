list_of_dicts = [
        {'id': 1, 'fruits': ['apple']},
        {'id': 2, 'fruits': ['orange']},
        {'id': 3, 'fruits': ['banana', 'apple']},
        {'id': 4, 'fruits': ['banana', 'apple', 'orange']}
        ]

acceptable_fruits = ['apple', 'banana']

filtered_list = [
    d for d in list_of_dicts
    if any(fruit in acceptable_fruits for fruit in d['fruits'])]

print(filtered_list)
