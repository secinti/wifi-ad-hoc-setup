## subscriber.py module
#
import os, socket
import threading
import json
import struct
import time

## Subscriber class inheriting Thread
#
class Subscriber(threading.Thread):
    def __init__(self, address):

        self.multicast_group = address[0]
        self.port = address[1]

        try:
            # Create the socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Bind to the server address
            self.sock.bind(('', self.port))

            # Tell the operating system to add the socket to the multicast group
            # on all interfaces.
            group = socket.inet_aton(self.multicast_group)
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except socket.error as exp:
            self.sock.close()
            raise

        threading.Thread.__init__(self)

    def run(self):
        # Receive loop
        while True:
            # print >> sys.stderr, '\nwaiting to receive message'
            try:
                data, address = self.sock.recvfrom(1024)
            except socket.timeout:
                print('timed out, no incoming CSI feedback')
                break
            else:
                de_serialized = json.loads(data)
                length = len(de_serialized)
                print('received "%s" from %s - time: %f ' % (de_serialized, self.multicast_group, time.time() ) )



if __name__ == '__main__':
    try:
        sub = Subscriber(('224.3.29.71', 10000))
    except Exception as e:
        print "Failed to init subscriber!\n"
        print e
    else:
        sub.start()
