import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is a FLOWS010 testcase from test cases document template.
       Check whether flows are discarded when having 'in_port' parameter 
       set to not exitsing port or defining output action for non existing port"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 10
        numberOfPorts = 4
        waitTimeAfterAllFlowsSent = 10 

        doClearTraces = self.myOFTestTool.clearSwitchTraces()

        for n in range(numberOfFlows):

            port = n % numberOfPorts + 1

            flow = "in_port=" + str(port) + ",dl_type=0x0800,dl_vlan=" + str(n) + ",nw_src=192.168.1.1,nw_dst=192.168.7.4,actions=output:1"

            if(n==3):
                flow = "in_port=7" + ",dl_type=0x0800,dl_vlan=" + str(n) + ",nw_src=192.168.1.1,nw_dst=192.168.7.4,actions=output:1"


            if(n==6):
                flow = "in_port=" + str(port) + ",dl_type=0x0800,dl_vlan=" + str(n) + ",nw_src=192.168.1.1,nw_dst=192.168.7.4,actions=output:10"

            if(n==9):
                flow = "in_port=8,dl_type=0x0800,dl_vlan=" + str(n) + ",nw_src=192.168.1.1,nw_dst=192.168.7.4,actions=output:23"


            self.myOFTestTool.addFlow(flow)

        self.myOFTestTool.wait(waitTimeAfterAllFlowsSent)

        if(doClearTraces):
            numberOfDiscardedFlows = self.myOFTestTool.countDiscardedFlows()
            if(numberOfDiscardedFlows == 3):
                print "TEST_OK :)"
            else:
                print "TEST_FAILED :("

            
    

