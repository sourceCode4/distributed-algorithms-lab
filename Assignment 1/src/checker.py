import os

dir_path = r'C:\Users\hanhe\Documents\TU Delft\Msc CS1\Q2\IN4150 Distributed Algorithms\Lab\IN4150-Python-Template-master\LogFiles'
logs = []
for path in os.scandir(dir_path):
    with open(path, "r") as reader:
        logs.append(reader.read())

last = logs[0]
correct = True
for i in logs:
    if i != last:
        correct &= False

print(correct)