import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is a PERF011 test case from test cases template document.
       1000 flows, wildcarded input port.
       Automatic measurement of flows addition time is done at the end
       based on user's decision whether to clear traces before executing
       the test"""


    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 1000
        waitTimeAfterAllFlowsSent = 2000
        firstFlowCookie = 1000
        lastFlowCookie = 2000

        doClearTraces = self.myOFTestTool.clearSwitchTraces()

        for n in range(numberOfFlows):

            flow = "dl_vlan=" + str(n) + ",dl_type=0x800,dl_src=55:33:22:44:22:44,dl_dst=44:11:44:22:44:55,nw_proto=17,actions=output:1"

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


            
    

