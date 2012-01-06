import sys
import OFTestTool, RandomFlowGenerator

sys.path.append('../')

class TestCase:

    """This test case loads desired amount of flows to the router. Flows are randomly generated.
       Flows are distributed within all ports configured on the router. Flows on ports distribution
       is shown after the generation of all flows. Flows parameter number distribution is shown
       after the generation of all flows"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()
        self.myRandomFlowGenerator = RandomFlowGenerator.RandomFlowGenerator()


    def run(self):
        numberOfFlows = 10000

        for n in range(numberOfFlows):
                
            if(not(n%5000) and n != 0):
                self.myOFTestTool.waitTillQueueLength(1000)

            #flow = self.myRandomFlowGenerator.generateFlow(RandomFlowGenerator.FlowTypes.L2FLOW)
            #flow = self.myRandomFlowGenerator.generateFlow(RandomFlowGenerator.FlowTypes.L3FLOW)
            flow = self.myRandomFlowGenerator.generateFlow(RandomFlowGenerator.FlowTypes.CUSTOMFLOW)
            #flow = self.myRandomFlowGenerator.generateFlow(RandomFlowGenerator.FlowTypes.RANDOMFLOW)

            self.myOFTestTool.addFlow(flow)
        self.myRandomFlowGenerator.showFlowParamsNumberDistribution()
        self.myRandomFlowGenerator.showFlowsOnPortDistribution()
        self.myOFTestTool.wait(15000)


