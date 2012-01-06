import sys
import OFTestTool, RandomFlowGenerator

sys.path.append('../')

class TestCase:

    """This is PKTOUT001 example test case defined in test template document -> verify whether packet_out functionality is working"""
    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):

        numberOfPacketsToSend = 5

        for n in range(numberOfPacketsToSend):
            self.myOFTestTool.sendPacketOut("output_port=1")
            self.myOFTestTool.sendPacketOut("output_port=2")
            self.myOFTestTool.wait(3)

