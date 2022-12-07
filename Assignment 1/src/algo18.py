from abstractprocess import AbstractProcess, Message
from queue import PriorityQueue

class Algo318(AbstractProcess):
    clock = 0
    prioQueue = PriorityQueue()
    acknowledgements = {}
    sent = 0
    received = 0
    total = 1
    log = ""
    

    async def algorithm(self):
        message = Message("Hello other node", self.idx, self.clock + 1)
        to = list(self.addresses.keys())

        self.clock += 1
        print("Node: " + str(self.idx) + " "+ str(self.prioQueue.queue))
        if self.sent < self.total:
            self.sent += 1
            for i in to:
                print("Node: " + str(self.idx) + " "+"Sending message to: " + str(i))
                await self.send_message(message, i)


        while self.buffer.has_messages():
            m = self.buffer.get()
            if m.content == "ack":
                if (m.counter, m.sender) in self.acknowledgements.keys():
                    self.acknowledgements[(m.counter, m.sender)] += 1
                else:
                    self.acknowledgements[(m.counter, m.sender)] = 1
            else:
                print("Node: " + str(self.idx) + " Received:"+ str((m.counter, m.sender)))
                self.received += 1
                self.prioQueue.put(((m.counter, m.sender), m.content))
                newMessage = Message("ack", m.sender, m.counter)
                if (m.counter, m.sender) not in self.acknowledgements.keys():
                    self.acknowledgements[(m.counter, m.sender)] = 0
                for i in to:
                    print("Node: " + str(self.idx) + " "+"Sending Ack to " + str(i) + " for message", (m.counter, m.sender))
                    await self.send_message(newMessage, i)

        delivering = True

        while delivering and not self.prioQueue.empty():
            first = self.prioQueue.queue[0]
            print("Node: " + str(self.idx) + " "+"Queue" + str(self.prioQueue.queue))
            print("Node: " + str(self.idx) + " "+"Acks" + str(self.acknowledgements))
            if self.acknowledgements[first[0]] == len(to):
                self.log += "Delivered Message! Clock: " + str(first[0][0]) + " Sender Id:" + str(first[0][1]) + "\n"
                self.clock = max(self.clock+1, first[0][0]+1)
                # del self.acknowledgements[(m.counter, m.sender)]
                print("Node: " + str(self.idx) + " "+"Delivered Message: " + str(self.prioQueue.get()))
            else:
                delivering = False

        if self.prioQueue.empty() and self.sent >= self.total and self.received == (self.total * len(self.addresses)) and not self.buffer.has_messages():
            self.running = False
