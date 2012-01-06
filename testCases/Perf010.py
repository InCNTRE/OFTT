import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is a PERF010 test case from test cases template document.
       2000 flows, 10 params, 6 ports (flows evenly distributed).
       Automatic measurement of flows addition time is done at the end
       based on user's decision whether to clear traces before executing
       the test"""


    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 2000
        numberOfPorts = 6
        waitTimeAfterAllFlowsSent = 90
        firstFlowCookie = 1000
        lastFlowCookie = 2000

        doClearTraces = self.myOFTestTool.clearSwitchTraces()

        for n in range(numberOfFlows):

            port = n % numberOfPorts + 1

            flow = "in_port=" + str(port) + ",dl_type=0x0800,dl_src=00:45:23:12:45:66,dl_dst=00:03:12:23:B0:55,dl_vlan=" + str(n) + ",nw_proto=17,nw_src=192.168.1.1,nw_dst=192.168.7.4,tp_src=40000,tp_dst=2000,actions=output:1"

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


            
    

