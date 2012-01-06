import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is a PERF009 test case from test cases template document.
       1000 flows, 7 parameters, 1 port.
       Automatic measurement of flows addition time is done at the end
       based on user's decision whether to clear traces before executing
       the test"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 1000
        waitTimeAfterAllFlowsSent = 90
        firstFlowCookie = 1000
        lastFlowCookie = 2000

        doClearTraces = self.myOFTestTool.clearSwitchTraces()

        for n in range(numberOfFlows):
                
            if n % 2:
                proto = 6
            else:
                proto = 17
            flow = "in_port=2,dl_type=0x0800,dl_vlan=" + str(n) + ",dl_src=00:03:12:23:B0:55,dl_dst=56:34:23:12:32:43,nw_proto=" + str(proto) + ",nw_src=192.168.1.1,actions=output:1"

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


            
    

