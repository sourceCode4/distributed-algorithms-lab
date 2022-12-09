# Assignment  2 - Version A

## Test case 1 - best case scenario
Three nodes in a complete network, two messages are sent from each node to every
other, marker is the first message that is sent, followed by the messages with random delays.

### Result:
#### channels:
    0 -> 1 = []
    0 -> 2 = []
    1 -> 0 = [1]
    1 -> 2 = []
    2 -> 0 = [1]
    2 -> 1 = []

### processes:
    process0 = {1: (0, 0), 2: (0, 0)}
    process1 = {0: (1, 0), 2: (2, 1)}
    process2 = {0: (1, 0), 1: (1, 2)}

## Test case 2 - half way snapshot
Three nodes in a complete network, marker is sent by a designated node once half 
of its messages are sent all with random delays.

### Result:
#### channels:
    0 -> 1 = []
    0 -> 2 = []
    1 -> 0 = [1, 2]
    1 -> 2 = []
    2 -> 0 = [2]
    2 -> 1 = [2]

#### processes:
    process0 = {1: (1, 0), 2: (1, 1)}
    process1 = {0: (2, 1), 2: (1, 1)}
    process2 = {0: (2, 1), 1: (2, 1)}

## Test case 3 - force full buffers
Three nodes in a complete network; the initiator waits for the incoming 
buffers to fill up, then sends the marker and starts receiving messages. 
The rest immediately start sending. This enforces the channels into the initiator
to fill up and be recorded as such.

### Result:

#### channels:
    0 -> 1 = []
    0 -> 2 = []
    1 -> 0 = [1, 2]
    1 -> 2 = []
    2 -> 0 = [1, 2]
    2 -> 1 = []

#### processes:
    process0 = {1: (1, 0), 2: (0, 0)}
    process1 = {0: (2, 1), 2: (2, 2)}
    process2 = {0: (2, 0), 1: (2, 2)}

## Test case 4 - force empty buffers
Five nodes in a complete network; everyone initially sends two messages to every other 
node, then the algorithm is triggered

### Result:
#### channels:
    0 -> 1 = []
    0 -> 2 = []
    0 -> 3 = []
    0 -> 4 = []
    1 -> 0 = []
    1 -> 2 = []
    1 -> 3 = []
    1 -> 4 = []
    2 -> 0 = []
    2 -> 1 = []
    2 -> 3 = []
    2 -> 4 = []
    3 -> 0 = []
    3 -> 1 = []
    3 -> 2 = []
    3 -> 4 = []
    4 -> 0 = []
    4 -> 1 = []
    4 -> 2 = []
    4 -> 3 = []

#### processes:
    process0 = {1: (2, 2), 2: (2, 2), 3: (2, 2), 4: (2, 2)}
    process1 = {0: (2, 2), 2: (2, 2), 3: (2, 2), 4: (2, 2)}
    process2 = {0: (2, 2), 1: (2, 2), 3: (2, 2), 4: (2, 2)}
    process3 = {0: (2, 2), 1: (2, 2), 2: (2, 2), 4: (2, 2)}
    process4 = {0: (2, 2), 1: (2, 2), 2: (2, 2), 3: (2, 2)}