import asyncio
import socket
from math import log

from abstractprocess import AbstractProcess, Message

class Node(AbstractProcess):

    def __init__(self, idx: int, addresses: dict, inits: bool):
        super().__init__(idx, addresses, inits)
        self.level = 0
        self.size = 0
        self.owner_id = -1
        self.owner:           int | None = None
        self.potential_owner: int | None = None
        self.killed = not inits
        self.link = -1
        self.initiating = self.candidate_process = inits
        self.init = self.level, self.idx, (self.idx + 1) % len(self.addresses)

    async def send(self, level, id, link):
        msg = Message(level, id, self.idx)
        await self.send_message(msg, link)

    async def receive(self):
        if self.buffer.has_messages():
            r_level, r_id, link, elected = msg = self.buffer.get().unpack()
            self.log(f'RECEIVED {r_level, r_id} from {link}' if not elected
                     else f'ELECTED {link}')
            return msg
        else:
            return None

    async def announce(self):
        for link in filter(lambda k: k != self.idx, self.addresses.keys()):
            await self.send_message(Message(None, None, self.idx, True), link)
        self.winner = self.idx
        self.running = False

    async def candidate(self, r_level, r_id, r_link):
        if not self.candidate_process:
            return

        if len(self.untraversed) == 0 and self.link < 0:
            if not self.killed:
                await self.announce()
        elif self.link < 0:
            self.link = self.untraversed[0]
            self.log(f'CAPTURING {self.link}')
            await self.send(self.level, self.idx, self.link)
        else:
            if r_id == self.idx and not self.killed:
                self.log(f'CAPTURED {self.untraversed[0]}')
                self.size += 1
                self.level = max(r_level, log(self.size))
                self.untraversed.pop(0)
                self.link = -1      # == no goto
            elif (r_level, r_id) < (self.level, self.idx):
                return  # == goto
            else:
                self.log(f'OK to {r_link}')    # killed
                await self.send(r_level, r_id, r_link)
                self.killed = True
                return  # == goto

    async def ordinary(self, r_level, r_id, r_link):
        if (r_level, r_id) < (self.level, self.owner_id):
            return
        elif (r_level, r_id) > (self.level, self.owner_id):
            self.potential_owner = r_link
            self.level, self.owner_id = r_level, r_id
            if self.owner is None:
                self.owner = self.potential_owner
            else:
                self.log(f'KILL {r_link}')
            await self.send(r_level, r_id, self.owner)
        else:
            self.log(f'ACK to {self.owner_id}')
            self.owner = self.potential_owner
            await self.send(r_level, r_id, self.owner)

    async def algorithm(self) -> None:
        if self.initiating:
            r_level, r_id, link = [None] * 3
            await self.candidate(r_level, r_id, link)
            self.initiating = False
            return

        received = await self.receive()
        if received is not None:
            r_level, r_id, link, elected = received
            if not elected:
                await self.candidate(r_level, r_id, link)
                await self.ordinary(r_level, r_id, link)
            else:
                self.winner = link
                self.running = False
        else:
            r_level, r_id, link = [-1] * 3
            await self.candidate(r_level, r_id, link)
