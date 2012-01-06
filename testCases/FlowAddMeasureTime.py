import sys, time
import OFTestTool

sys.path.append('../')

class TestCase:

    """This test case measures the time of adding the next portion of flows on top of flows already loaded.
       User may define final number of flows to load and a size of flows portion to be loaded in one step."""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 10000
        flowPortion = 100
        timeout = 3600
        
        tmp = 1
        fileHandler = open("flow_portions_measurment", 'w')
        startTime = time.time()
        for n in range(1, numberOfFlows + 1):
        
            flow = "in_port=1,dl_type=0x800,dl_vlan=" + str(n) + ",dl_dst=00:45:66:33:22:11,dl_src=00:22:66:44:22:11,actions=output:2"
            self.myOFTestTool.addFlow(flow)

            if(not(n%flowPortion) and n!=0):
                
                expectedFlowNumber = tmp * flowPortion
                while True:
                    actualFlowNumber = self.myOFTestTool.getFlowsNumber()
                    print " expected %d" % (expectedFlowNumber)

                    if(((actualFlowNumber >= expectedFlowNumber)) or ((time.time() - startTime) >= timeout)):
                        endTime = time.time()
                        timeDelta = endTime - startTime
                        print "Adding next %d flows took %f seconds" % (flowPortion, timeDelta)

                        stringToWrite = str(actualFlowNumber) + "    " + str(expectedFlowNumber) + "    " + str(timeDelta) + "\n"
                        fileHandler.write(stringToWrite)
                        fileHandler.flush()
                        tmp = tmp + 1
                        startTime = time.time()
                        break



