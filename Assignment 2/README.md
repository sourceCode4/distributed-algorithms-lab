# Assignment  2 - Version A

## Test case 1 - best case scenario
Three nodes in a complete network, two messages are sent from each node to every
other, marker is the first message that is sent, followed by the messages with random delays.

## Test case 2 - half way snapshot
Three nodes in a complete network, marker is sent by a designated node once half 
of its messages are sent all with random delays.

## Test case 3 - force full buffers
Three nodes in a complete network; the initiator initially waits for the incoming 
buffers to fill up, then sends the marker and starts receiving messages. 
The rest immediately start sending. This enforces the channels into the initiator
to fill up and be recorded as such.

## Test case 4 - force empty buffers
Five nodes in a complete network; everyone initially sends two messages to every other 
node, then the algorithm is triggered