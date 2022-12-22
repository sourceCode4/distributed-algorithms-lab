import os

linesOf = []
for i, folder in enumerate(os.listdir('./logs')):
    with open(f'./logs/{folder}/log{i}.txt', 'r') as file:
        linesOf.append(file.readlines())

captured_count = sum(map(len, filter(lambda l: l.startswith('CAPTURED'))))