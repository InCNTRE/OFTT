import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is test case loads a desired number of flows on desired number of ports. Flows are equally
       distributed within a ports."""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 20000
        numberOfPorts = 4
        #TODO: parametrize flow parameters -> FlowBuilder class to be implemented

        for n in range(numberOfFlows):
                
            port = n % numberOfPorts + 1
                
            if(not(n%5000) and n != 0):
                self.myOFTestTool.waitTillQueueLength(1000)

            flow = "in_port=" + str(port) + ",dl_type=0x800,dl_vlan=" + str(n) + ",dl_dst=" + self.__generateMac(n) + ",dl_src=00:22:66:33:22:11,actions=output:3"
            self.myOFTestTool.addFlow(flow)

        self.myOFTestTool.wait(7200)



    def __generateMac(self, iteration):
              mac = iteration & 255
              if mac < 16:
                mac1 = "0%x"%mac
              else:
                mac1 = "%x"%mac
              mac = (iteration & 65280) >> 8
              if mac < 16:
                mac2 = "0%x"%mac
              else:
                mac2 = "%x"%mac
              mac =  "00:12:34:56:" + mac2 + ":" + mac1
              return mac

