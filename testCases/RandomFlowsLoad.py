import sys, random
import OFTestTool, RandomFlowGenerator

sys.path.append('../')

class TestCase:

    """This test case loads the desired amount of randomly generated flows
       with randomly chosen bursts and intervals"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()
        self.myRandomFlowGenerator = RandomFlowGenerator.RandomFlowGenerator()

    def run(self):
        iterations = 1
        numberOfFlows = 10000
        maxBurstSize = 300
        maxPauseBetweenBursts = 60

        flowsSent = 0
        while(flowsSent < numberOfFlows):
            burstSize = self.myRandomFlowGenerator.generateRandomBurstSize(maxBurstSize)
            for n in range(burstSize):
                flow = self.myRandomFlowGenerator.generateFlow(RandomFlowGenerator.FlowTypes.L2FLOW)
                #flow = self.myRandomFlowGenerator.generateFlow(RandomFlowGenerator.FlowTypes.L3FLOW)
                #flow = self.myRandomFlowGenerator.generateFlow(RandomFlowGenerator.FlowTypes.RANDOMFLOW)
                print "Sending flow: %s" % (flow)
                self.myOFTestTool.addFlow(flow)
                flowsSent = flowsSent + 1
                if(flowsSent >= numberOfFlows):
                    break

            self.myOFTestTool.wait(self.myRandomFlowGenerator.generateRandomWaitTime(maxPauseBetweenBursts))

        self.myOFTestTool.wait(300)

