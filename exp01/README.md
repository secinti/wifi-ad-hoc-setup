## Multicast Publisher/Subscriber Example

Publisher sends UDP packets on **('224.3.29.71', 10000)**  multicast ip,port pair on every second containing a JSON with given format below.

`{
      "source" : "ISE306-Publisher",
      "sequence" : 0
  }`


Subscriber listens the given multicast ip,port pair and simply prints out the received data. 
