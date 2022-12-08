from abstractprocess import AbstractProcess, Message
import random
import operator

class GlobalState(AbstractProcess):
    """
    Example implementation of a distributed process.
    Only the algorithm() function needs to be implemented.
    The function send_message(message, to) can be used to send asynchronous messages to other processes.
    """
    def __init__(self, idx: int, addresses: dict):
        super().__init__(idx, addresses)
        self.local_state = [(0, 0)] * (len(self.addresses) + 1)
        self.counter = 0

    async def algorithm(self):
        # Send a message up to 3 messages
        if self.counter < 3:
            # Compose message
            msg = Message("Hello world", self.idx, self.counter)
            to: int = random.choice(list(self.addresses.keys()))
            await self.send_message(msg, to)
            self.counter += 1
            self.local_state[to] = (self.local_state[to][0] + 1, self.local_state[to][1])
            self.log(f"{self.idx} Send message to {to}, message:{msg.counter}, local state: {self.local_state}")

        # If we have a new message
        if self.buffer.has_messages():
            # Retrieve message
            msg: Message = self.buffer.get()
            if msg.content == "marker":
                self.Bc = [[] for _ in range(len(self.addresses) + 1)]
                
            else:
                self.local_state[msg.sender] = \
                    (self.local_state[msg.sender][0], self.local_state[msg.sender][1] + 1)
                self.log(f'{self.idx} Got message from process {msg.sender}, '
                         f'counter: {msg.counter}, local_state: {self.local_state}')

        if not self.buffer.has_messages() and self.counter >= 3:
            self.running = False
