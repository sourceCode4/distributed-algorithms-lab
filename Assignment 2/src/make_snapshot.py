import os

def cmpKey(line: str, c: int):
    tokens = line.split()
    return tokens[0] + tokens[1]

lines = []

for i, node in enumerate(os.listdir('./logs')):
    with open(f'./logs/{node}/log{i}.txt', 'r') as reader:
        lines += reader.readlines()
channels = list(map(lambda l: ' '.join(l.split()[1:]), filter(lambda l: l.startswith('channel'), lines)))
channels = sorted(channels, key=lambda l: cmpKey(l, len(channels)))
nodes = map(str.strip, filter(lambda l: l.startswith('process'), lines))

snapshot = "channels:\n" + "\n".join(channels) + "\n\nprocesses:\n" + "\n".join(nodes)

with open(f'./snapshot.txt', 'w') as writer:
    writer.write(snapshot)