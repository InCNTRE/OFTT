import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is a PERF004 testcase from test cases template document.
       4000 flows, 5 parameters, 6 ports (flows evenly distributed).
       Automatic measurement of flows addition time is done at the end
       based on user's decision whether to clear traces before executing
       the test"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 4000
        numberOfPorts = 6
        waitTimeAfterAllFlowsSent = 600
        firstFlowCookie = 1000
        lastFlowCookie = 2000

        doClearTraces = self.myOFTestTool.clearSwitchTraces()

        for n in range(numberOfFlows):

            port = n % numberOfPorts + 1

            flow = "in_port=" + str(port) + ",dl_type=0x0800,dl_vlan=" + str(n) + ",nw_src=192.168.1.1,nw_dst=192.168.7.4,actions=output:1"

            if(n==0):
                flow = "cookie=" + str(firstFlowCookie) + ',' + flow

            if(n==numberOfFlows - 1):
                flow = "cookie=" + str(lastFlowCookie) + ',' + flow

            self.myOFTestTool.addFlow(flow)

        self.myOFTestTool.wait(waitTimeAfterAllFlowsSent)

        addedFlowsNumber = self.myOFTestTool.getFlowsNumber()
        if(addedFlowsNumber != numberOfFlows):
            print "Some flows were discarded or not all flows added within expected time."
            return

        if(doClearTraces):
            self.myOFTestTool.measureFlowsLoadTime(firstFlowCookie, lastFlowCookie)

