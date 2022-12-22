import random

from abstractprocess import AbstractProcess, Message
from asyncio import sleep
from random import shuffle


class GlobalState(AbstractProcess):
    """
    Example implementation of a distributed process.
    Only the algorithm() function needs to be implemented.
    The function send_message(message, to) can be used to send asynchronous messages to other processes.
    """

    def __init__(self, idx: int, addresses: dict):
        super().__init__(idx, addresses)
        self.PROCESS_COUNT = len(self.addresses) + 1
        self.send_buffer = list(addresses.keys()) * 2
        shuffle(self.send_buffer)
        self.local_state = {k: (0, 0) for k in addresses.keys()}
        self.channel_state: dict[int, list[int]] = {k: [] for k in addresses.keys()}
        self.sent_count = 0
        self.recorded = False
        self.mark_count = 0
        self.done = False
        self.done_count = 1

    def record_channel(self, sender: int):
        state = f'channel {sender} -> {self.idx} = {self.channel_state[sender]}'
        self.log += f'{state}\n'
        print(state)

    async def send(self, content: str, receiver: int):
        receiver_state = self.local_state[receiver]

        if content == "marker" or content == "done":
            print(f"{content.upper()} SENT to {receiver}")
        elif receiver != self.idx:
            self.sent_count += 1
            self.local_state[receiver] = (receiver_state[0] + 1, receiver_state[1])

        msg = Message(content, self.idx, self.local_state[receiver][0])
        await self.send_message(msg, receiver)

    async def record_and_send_markers(self):
        self.mark_count += 1

        # record local state
        local_state = f"process{self.idx} = {self.local_state}"
        self.log += f'{local_state}\n'
        print(local_state)

        self.recorded = True
        for pid in self.addresses.keys():
            await self.send("marker", pid)

    async def handle_receive(self):
        if not self.buffer.has_messages(): return

        content, sender, count = self.buffer.get().unpack()

        if content == "marker":
            print(f"MARKER RECEIVED from {sender}")
            self.mark_count += 1
            self.record_channel(sender)
            if not self.recorded:
                # assume it is empty
                await self.record_and_send_markers()
        elif content == "done":
            self.done_count += 1
        elif sender != self.idx:
            sender_state = self.local_state[sender]
            self.local_state[sender] = (sender_state[0], sender_state[1] + 1)
            if self.recorded:
                self.channel_state[sender].append(count)
            print(f"RECEIVED message {count}: '{content}' from process #{sender}, local state: {self.local_state}")

    async def handle_send(self):
        if len(self.send_buffer) != 0:
            receiver = self.send_buffer.pop()
            await self.send(f"msg{self.sent_count}", receiver)

    async def algorithm(self):
        await self.handle_receive()
        await self.handle_send()

        # if self.idx != 0 and not self.done and len(self.send_buffer) == 0:
        #     self.done = True
        #     await self.send("done", 0)

        # node 0 initializes
        if self.idx == 0 and not self.recorded \
                and len(self.send_buffer) <= self.PROCESS_COUNT \
                + random.choice(range(-self.PROCESS_COUNT, self.PROCESS_COUNT)):
            # and self.done_count == self.PROCESS_COUNT:
            await self.record_and_send_markers()

        self.running = self.mark_count < self.PROCESS_COUNT or \
                       len(self.send_buffer) != 0
