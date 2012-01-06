import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This test case periodically modifies flows loaded on port A (and redirecting traffic to port B) to redirect traffic
       to port C. After defined time period the traffic is redirected to port B again. This scenario is repeated.
       Port A should be connected to some traffic generator (eg. IXIA) which should be able to generate traffic maching configured flows"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        iterations = 10
        numberOfFlows = 1000
        pauseBetweenSwitchovers = 60

        i = 0
        for i in range(iterations):
            ipStart = struct.unpack("!L", socket.inet_aton("192.168.2.0"))[0]

            for n in range(numberOfFlows):

                ip = socket.inet_ntoa(struct.pack("!L", ipStart + n))
                flow = "in_port=1,dl_type=0x0800,nw_src=192.168.1.1,nw_dst=" + ip +  ",actions=output:3"
                self.myOFTestTool.addFlow(flow)

            print "Iteration: " + str(i)

            self.myOFTestTool.wait(pauseBetweenSwitchovers)

            for n in range(numberOfFlows):

                ip = socket.inet_ntoa(struct.pack("!L", ipStart + n))
                flow = "in_port=1,dl_type=0x0800,nw_src=192.168.1.1,nw_dst=" + ip +  ",actions=output:4"
                self.myOFTestTool.addFlow(flow)

            print "End of iteration: " + str(i)
            self.myOFTestTool.wait(pauseBetweenSwitchovers)
            
    

