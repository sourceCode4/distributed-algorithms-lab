import os


def cmpKey(line: str):
    tokens = line.split()
    return tokens[0] + tokens[2]


lines = []
for i, node in enumerate(os.listdir('./logs')):
    with open(f'./logs/{node}/log{i}.txt', 'r') as reader:
        lines += reader.readlines()

channels = sorted(map(lambda l: ' '.join(l.split()[1:]),
                      filter(lambda l: l.startswith('channel'), lines)),
                  key=lambda l: cmpKey(l))
nodes = map(str.strip, filter(lambda l: l.startswith('process'), lines))

snapshot = "channels:\n" + "\n".join(channels) + "\n\nprocesses:\n" + "\n".join(nodes)

with open(f'./snapshot.txt', 'w') as writer:
    writer.write(snapshot)
