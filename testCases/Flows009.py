import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is FLOWS009 example test case defined in test template document - verify whether cookie value is shown properly"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 10

        for n in range(numberOfFlows):
            cookie =  n*n
            flow = "in_port=1,dl_type=0x800,dl_vlan=" + str(n) + ",hard_timeout=30,dl_dst=00:33:44:22:11:11,cookie=" + str(cookie) + ",nw_proto=6,actions=output:2"
            self.myOFTestTool.addFlow(flow)
            
        print "You may now check whether the flows with correct cookie values n^2 where n=[0 - 9] were added to OF app... \n" \
              "Invoke \"show openflow switch statistics flows <SW_ID>\" command in the switch console \n" \
              "After 30 seconds flows will be deleted due to hard timeout. \n" \
              "Verify cookies values in messages sent to controller"

        self.myOFTestTool.wait(35)
