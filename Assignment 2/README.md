# Assignment  1 - Version A

Our code implements the algorithm for total ordering of broadcast messages, executed on each node. In pseudocode it looks as follows:

initially: C = 0, priorityQueue = empty PriorityQueue, acks[m] = 0 forall m
on SendMessage(m):
	C = C + 1
	send(m, C, pid)
on Receive(m, Cj, IDj):
	if (m is ACK):
		acks[m] += 1
	if (acks[m] == #processes and m is priorityQueue.head):
		deliver(m)
	else:
		priorityQueue.insert(m)

In order to validate our algorithm we ran a sequence of tests, with the last and the largest one executing eight nodes concurrently, each sending 4 messages. After the algorithm finished each node logged the order in which events were delivered and we ran a python script to make sure all the ordering of delivery was the same for every node. The test script can be found in the src folder and is called checker.py.