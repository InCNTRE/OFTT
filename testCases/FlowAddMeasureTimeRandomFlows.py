import sys, time
import OFTestTool, RandomFlowGenerator

sys.path.append('../')

class TestCase:

    """This test case measures the time of adding the next portion of flows on top of flows already loaded.
       User may define final number of flows to load anda size of flows portion to be loaded in one step.
       Flows here are randomly generated."""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()
        self.myRandomFlowGenerator = RandomFlowGenerator.RandomFlowGenerator()


    def run(self):
        numberOfFlows = 10000
        flowPortion = 100
        flowRepetitionNumber = 15 #TODO - restest this - find a way that flow are not to be repeted during random generation (more imatch params)
        timeout = 3600
        
        tmp = 1
        fileHandler = open("flow_portions_measurment", 'w')
        startTime = time.time()
        for n in range(1, numberOfFlows + 1):
       
            flow = self.myRandomFlowGenerator.generateFlow(RandomFlowGenerator.FlowTypes.L2FLOW)
            self.myOFTestTool.addFlow(flow)

            if(not(n%flowPortion) and n!=0):
                
                expectedFlowNumber = tmp * flowPortion
                while True:
                    actualFlowNumber = self.myOFTestTool.getFlowsNumber()
                    print " expected %d" % (expectedFlowNumber)

                    if(((actualFlowNumber >= expectedFlowNumber - flowRepetitionNumber)) or ((time.time() - startTime) >= timeout)):
                        endTime = time.time()
                        timeDelta = endTime - startTime
                        print "Adding next %d flows took %f seconds" % (flowPortion, timeDelta)

                        stringToWrite = str(actualFlowNumber) + "    " + str(expectedFlowNumber) + "    " + str(timeDelta) + "\n"
                        fileHandler.write(stringToWrite)
                        fileHandler.flush()
                        tmp = tmp + 1
                        startTime = time.time()
                        break
            
