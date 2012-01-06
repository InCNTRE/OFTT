import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is a Perf012 testcase from test cases document template"""
    """5000 flows, 3params, 6ports"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        iterations = 1
        numberOfFlows = 5000

        i = 0
        for i in range(iterations):

            for n in range(numberOfFlows):

                port = n % 4 + 1

                mac = n & 255
                if mac == 0:
                    mac1 = "00"
                elif ((mac > 0) and (mac < 16)):
                    mac1 = "0%x"%mac
                else:
                    mac1 = "%x"%mac

                mac = (n & 65280) >> 8
                if mac == 0:
                    mac2 = "00"
                elif ((mac > 0) and (mac < 16)):
                    mac2 = "0%x"%mac
                else:
                    mac2 = "%x"%mac


                flow = "in_port=" + str(port) + ",dl_src=00:12:34:56:" + mac2 + ":" + mac1 + ",dl_dst=00:45:23:12:24:66,actions=output:1"
                self.myOFTestTool.addFlow(flow)


            print "End of iteration: " + str(i+1) + " of " + str(iterations)
            
    

