import sys
import OFTestTool

sys.path.append('../')

class BasicTestCase:

    """This is a basic test case class. Other test cases may inherit from this class
       as it ptovides proper environment initialization before processing the test.
       It also provides methods to store results after the test is processed(get core dumps,
       logs, etc.)"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

        #TODO: add actions which should be taken before the processing of the test
        # eg. restart of-app, clear logs, etc.


    def run(self):
        self.myOFTestTool.wait(5)


    #TODO: define actions after test execusions, eg. get logs, cores, etc.
