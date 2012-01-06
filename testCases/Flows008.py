import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is FLOWS008 example test case defined in test template document -> verify whether flows are removed after hard-timeout."""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 10


        for n in range(numberOfFlows):
            hardTimeout = (30 if n%2 else 60)
            flow = "in_port=1,hard_timeout=" + str(hardTimeout) + ",dl_type=0x800,dl_vlan=" + str(n) + ",dl_dst=00:33:54:22:11:11,nw_proto=6,actions=output:2"
            self.myOFTestTool.addFlow(flow)

        print "You may now check whether 10 flows were added to OF app... \n" \
              "Invoke \"show openflow switch statistics flows <SW_ID>\" command in the switch console \n" \
              "Also automatic check is going to be processed \n" \
              "5 flows are going to be deleted in 30 seconds \n"


        self.myOFTestTool.wait(32)

        print "You may now check whether 5 of 10 flows were deleted from OF app... \n" \
              "Invoke \"show open flow switch statistics flows\" command in the switch console \n" \
              "Also automatic check is going to be processed \n" \
              "Last 5 flows are going to be deleted in 30 seconds \n"


        if(self.myOFTestTool.getFlowsNumber() != 5):
            print "Automatic check failed !!! - first 5 flows was not removed"
            return

        self.myOFTestTool.wait(32)

        print "You may now check whether all 10  flows were deleted from OF app... \n" \
              "Invoke \"show open flow switch statistics flows\" command in the switch console \n" \
              "Also automatic check is going to be processed \n"


        if(self.myOFTestTool.getFlowsNumber() != 0):
            print "Automatic check failed !!! - flows were not deleted"
            return

        print "TEST OK :)"


