import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is a PERF005 test case from test cases template document.
       1000 flows, 5 parameters, 1 port.
       Automatic measurement of flows addition time is done at the end
       based on user's decision whether to clear traces before executing
       the test"""


    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 1000
        waitTimeAfterAllFlowsSent = 70
        firstFlowCookie = 1000
        lastFlowCookie = 2000

        doClearTraces = self.myOFTestTool.clearSwitchTraces()

        for n in range(numberOfFlows):

            flow = "in_port=2,dl_type=0x0800,dl_vlan=" + str(n) + ",nw_src=192.168.1.1,nw_dst=192.168.7.4,actions=output:1"

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


            
    

