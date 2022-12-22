from sys import argv
from os import mkdir
from random import sample

i_n = argv.index("n") if "n" in argv else None
i_m = argv.index("s") + 1 if "s" in argv else None
n = int(argv[i_n + 1]) if i_n is not None else 3
if i_m is not None and i_n is not None:
    inits = argv[i_m:] if i_m > i_n else argv[i_m:i_n]
elif i_n is None and i_m is not None:
    inits = argv[i_m:]
elif "a" in argv:
    inits = list(range(n))
elif "r" in argv:
    inits = sample(range(n), min(int(argv[argv.index("r") + 1]), n))
else:
    inits = [0]
inits = list(map(int, inits))

BASE_ADDRESS = 9090

for i in range(n):
    mkdir(f'logs/node{i}')

lines = map(lambda i: f"  node{i}:\n    build: .\n    ports:\n      - '{BASE_ADDRESS + i}:{BASE_ADDRESS + i}'"
                      f"\n    environment:\n      PID: {i}\n      initiates: {1 if i in inits else 0}\n    volumes:"
                      f"\n      - type: bind\n        source: ./logs/node{i}\n        target: /log", range(n))
lines = "version: '3.3'\nservices:\n" + '\n'.join(lines)

with open('docker-compose.yml', 'w') as file:
    file.write(lines)

with open("resources/addresses.txt", 'w') as file:
    file.write('\n'.join(map(lambda i: f"{i} localhost {BASE_ADDRESS + i}", range(n))))

lines = '\n'.join(map(lambda i: f"{i} node{i} {BASE_ADDRESS + i}", range(n)))
with open('resources/addresses_docker.txt', 'w') as file:
    file.write(lines)

if __name__ == '__main__':
    pass
