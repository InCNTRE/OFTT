import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is FLOWS004 example test case defined in test template document -> delete previously added flows"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 10

        for n in range(numberOfFlows):

            flow = "in_port=1,dl_type=0x800,dl_vlan=" + str(n) + ",dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2"
            self.myOFTestTool.addFlow(flow)

        print "You may now check whether the flows were added to OF app... \n" \
              "Invoke \"show openflow switch statistics flows <SW_ID>\" command in the switch console \n" \
              "Also automatic check is going to be processed \n" \
              "Flows will be deleted in 30 seconds"

        self.myOFTestTool.wait(30)

        if(self.myOFTestTool.getFlowsNumber() != numberOfFlows):
            print "Automatic check failed !!! - not all expected flows were added to OF app"
            return

        for n in range(numberOfFlows):
 
            flow = "in_port=1,dl_type=0x800,dl_vlan=" + str(n) + ",dl_dst=00:33:44:22:11:11,nw_proto=6"
            self.myOFTestTool.delFlow(flow)


        print "You may now check whether the flows were deleted from OF app... \n" \
              "Invoke \"show open flow switch statistics flows\" command in the switch console \n" \
              "Also automatic check is going to be processed"

        self.myOFTestTool.wait(5)

        if(self.myOFTestTool.getFlowsNumber() != 0):
            print "Automatic check failed !!! - not all expected flows were deleted to OF app"
            return

        print "TEST OK :)"

