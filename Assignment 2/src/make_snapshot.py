import os

snapshot = ''

for i, node in enumerate(os.listdir('./logs')):
    with open(f'./logs/{node}/log{i}.txt', 'r') as reader:
        for line in reader.readlines():
            snapshot += line

snapshot = '\n'.join(sorted(snapshot.split('\n'), key=(lambda line: int(line.startswith('process')))))

with open(f'./snapshot.txt', 'w') as writer:
    writer.write(snapshot)