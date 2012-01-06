import ConfigParser

class ConfigurationReader:

    """Class reading the configuration from configuration.cfg file"""

    def __init__(self, configurationFile = 'configuration.cfg'):
        self.configurationFile = configurationFile
        self.readConfiguration()


    def readConfiguration(self):
        config = ConfigParser.ConfigParser()
        config.read(self.configurationFile)

        #OVS tools
        self.ovsToolsDir = config.get('Installation Dirs', 'OVS_TOOLS_DIR')
        
        #Switch
        self.switchIP = config.get('Switch', 'SWITCH_IP')
        self.switchID = config.get('Switch', 'SWITCH_ID')
        self.switchUser = config.get('Switch', 'SWITCH_USER')
        self.switchTraceFile = config.get('Switch', 'SWITCH_TRACEFILE')

        #Resources Monitor
        self.resourcesFilePref = config.get('Resources Monitor', 'RESOURCES_FILE_PREFIX')
        self.samplingFreq = config.get('Resources Monitor', 'SAMPLING_FREQUENCY')


    def showConfiguration(self):

        print 'Current Configuration:'
        print 'Section Installation Dirs:'
        print 'OVS tools installation dir: ', self.ovsToolsDir
        
        print 'Section Switch'
        print 'Switch IP address: ', self.switchIP
        print 'Switch ID: ', self.switchID
        print 'Switch user: ', self.switchUser
        print 'Switch tracefile name:', self.switchTraceFile

        print 'Section Resources Manager'
        print 'Resources file prefix: ', self.resourcesFilePref
        print 'Switch resources sampling frequency: ', self.samplingFreq

