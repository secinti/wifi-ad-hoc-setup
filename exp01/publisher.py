## publisher.py module
#
import os, socket
import threading
import json
import time
import struct

## Publisher class inheriting Thread
#
class Publisher(threading.Thread):

    data = {
        "source" : "ISE306-Publisher",
        "sequence" : 0
    }

    def __init__(self):

        """Set UDP SERVER"""
        self.multicast_group = ('224.3.29.71', 10000)

        # Create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        try:

            group = socket.inet_aton('224.3.29.71')
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except Exception as e:
            self.sock.close()
            raise

            # logging.exception("Cannot init multicast UDP socket: {}".format(e))

        threading.Thread.__init__(self)

    def run(self):
        while True:
            serialized = json.dumps(self.data, indent=4)
            self.sock.sendto(serialized, self.multicast_group)

            # increment sequence number
            old_seq = self.data["sequence"]
            self.data["sequence"] = old_seq + 1

            # Wait for one second
            time.sleep(1)




if __name__ == '__main__':
    try:
        pub = Publisher()
    except Exception as e:
        print "Failed to init publisher!\n"
        print e
    else:
        pub.start()
