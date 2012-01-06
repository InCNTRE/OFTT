import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is FLOWS006 example test case defined in test template document -> delete the same flow multiple times"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 10

        flow = "in_port=1,dl_type=0x800,dl_vlan=4,dl_dst=00:33:54:22:11:11,nw_proto=6,actions=output:2"
        self.myOFTestTool.addFlow(flow)

        print "You may now check whether 1 flow was added to OF app... \n" \
              "Invoke \"show openflow switch statistics flows <SW_ID>\" command in the switch console \n" \
              "Also automatic check is going to be processed \n" \
              "The flow is going to be deleted in 30 seconds"


        self.myOFTestTool.wait(30)
 
        if(self.myOFTestTool.getFlowsNumber() != 1):
            print "Automatic check failed !!! - the flow was not added"
            return


        for n in range(numberOfFlows):

            flow = "in_port=1,dl_type=0x800,dl_vlan=4,dl_dst=00:33:54:22:11:11,nw_proto=6"
            self.myOFTestTool.delFlow(flow)

        self.myOFTestTool.wait(5)

        if(self.myOFTestTool.getFlowsNumber() != 0):
            print "Automatic check failed !!! - flow was not deleted"
            return

        print "TEST OK :)"


