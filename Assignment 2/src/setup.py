from sys import argv
from os import mkdir

position = argv.index("-n") if "-n" in argv else None
n = int(argv[position + 1]) if position is not None else 3

for i in range(n):
    mkdir(f'logs/node{i}')

lines = map(lambda i: f"  node{i}:\n    build: .\n    ports:\n      - '{9090 + i}:{9090 + i}'"
                      f"\n    environment:\n      PID: {i}\n    volumes:\n      - type: bind"
                      f"\n        source: ./logs/node{i}\n        target: /log", range(n))
lines = "version: '3.3'\nservices:\n" + '\n'.join(lines)

with open('docker-compose.yml', 'w') as file:
    file.write(lines)

with open("resources/addresses.txt", 'w') as file:
    file.write('\n'.join(map(lambda i: f"{i} localhost {9090 + i}", range(n))))

lines = '\n'.join(map(lambda i: f"{i} node{i} {9090 + i}", range(n)))
with open('resources/addresses_docker.txt', 'w') as file:
    file.write(lines)
