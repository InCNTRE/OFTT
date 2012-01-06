import random, sys, socket, struct
import OFTestTool

class FlowTypes:
    L2FLOW = 1                      #only parameters from L2 - in_port, dl_vlan, dl_type, dl_src, dl_dst (first 3 always generated)
    L3FLOW = 2                      #only parameters flom L3 and required from L2 - in_port, dl_type, nw_src, nw_dst, nw_proto (first 3 always generated)
    L4FLOW = 3                      #to be implemented
    WILDCARDEDINPORTFLOW = 4        #to be implemented
    CUSTOMFLOW = 5                  #parameters explicitly defined by user
    RANDOMFLOW = 6                  #parameters chosen from full 10-tuple (at least in_port, dl_vlan, dl_type always generated) 



class FlowParametersFactory:

    def __init__(self):
        pass

    def generateFlowParameters(self, flowType):
        flowTypes = { 
           FlowTypes.L2FLOW: self.__getL2FlowParameters, 
           FlowTypes.L3FLOW: self.__getL3FlowParameters,
           FlowTypes.L4FLOW: self.__getL4FlowParameters,
           FlowTypes.WILDCARDEDINPORTFLOW: self.__getWildcardedInPortFlowParameters,
           FlowTypes.CUSTOMFLOW: self.__getCustomFlow,
           FlowTypes.RANDOMFLOW: self.__getRandomFlowParameters
        }
        return flowTypes.get(flowType)()


    def __getL2FlowParameters(self):
        parametersList = ["in_port=", "dl_vlan=", "dl_type=", "dl_src=", "dl_dst="]
        parametersNumber = random.randint(3,5)

        flowParameters = []
        for i in range(0, parametersNumber):
            flowParameters.append(parametersList[i])
        flowParameters.append("actions=output:")
        return flowParameters

    def __getL3FlowParameters(self):
        parametersList = ["in_port=",  "dl_type=", "nw_src=", "nw_dst=", "nw_proto="]
        parametersNumber = random.randint(3,5)

        flowParameters = []
        for i in range(0, parametersNumber):
            flowParameters.append(parametersList[i])
        flowParameters.append("actions=output:")
        return flowParameters
 

    def __getL4FlowParameters(self):
        pass


    def __getWildcardedInPortFlowParameters(self):
        pass

    def __getCustomFlow(self):
        flowParameters = ["in_port=", "dl_vlan=", "dl_type=", "dl_src=", "dl_dst=", "nw_src=", "nw_dst=", "nw_proto=", "tp_src=", "tp_dst=", "actions=output:"]
        return flowParameters
        
    def __getRandomFlowParameters(self):
        flowParametersList = ["in_port=", "dl_vlan=", "dl_type=", "dl_src=", "dl_dst=", "nw_src=", "nw_dst=", "nw_proto=", "tp_src=", "tp_dst="]
        parametersNumber = random.randint(3,10)
        flowParameters = []
        for i in range(0,parametersNumber):
            flowParameters.append(flowParametersList[i])
        flowParameters.append("actions=output:")    
        return flowParameters




class RandomFlowGenerator:

    """Class genearting random flows."""

    def __init__(self):
        random.seed()
        #TODO: add excteption handling here
        self.numberOfPorts = OFTestTool.OFTestTool().getPortsNumber()
        self.flowParametersFactory = FlowParametersFactory()
        self.flowsOnPortDistributionList = [0] * self.numberOfPorts


    def generateFlow(self, flowType):
        flowParameters = self.flowParametersFactory.generateFlowParameters(flowType)
        flow = self.__assignValues(flowParameters)
        return flow
    
    #to count number of flows with a given number of parameters during the load
    flowParametersNumberDistributionList = [0, 0, 0, 0, 0, 0, 0, 0]

    def __countFlowParamsNumber(self, flowParameters):
        paramsNumber = len(flowParameters)
        self.flowParametersNumberDistributionList[paramsNumber - 4] = self.flowParametersNumberDistributionList[paramsNumber - 4] + 1 #'-4' -> at least 3 parameters always generated + actions are contained in flowParameters argument

    def __countFlowsOnPortDistribution(self, portNumber):
        self.flowsOnPortDistributionList[portNumber - 1] =  self.flowsOnPortDistributionList[portNumber - 1] + 1

    def showFlowParamsNumberDistribution(self):
        for i in range (0, 8):
            print "Number of flows with %d params: %d" % (i + 3, self.flowParametersNumberDistributionList[i])

    def showFlowsOnPortDistribution(self):
        for i in range(len(self.flowsOnPortDistributionList)):
            print "Number of flows per port %d: %d" % (i+1, self.flowsOnPortDistributionList[i])

    #TODO: think whether values generation methods may be used somewhere or should be private
    def generateRandomIPAddress(self):
        ipDec = random.randint(0, 4294967295)
        ip = socket.inet_ntoa(struct.pack("!L", ipDec))
        return ip

    
    def generateRandomMACAddress(self):
        mac = [random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff), \
        random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]

        return ':'.join(map(lambda x: "%02x" % x, mac))


    def generateRandomiOFPortNumber(self):
        port = random.randint(1, self.numberOfPorts)
        if(self.numberOfPorts <= 1):
            print "You must have at lest 2 OF ports configured on the router"
        return port

    def generateRandomL4PortNumber(self):
        port = random.randint(0, 65535)
        return port

    etherTypes = ["0x0800"]   #Internet Protocol, Version 4 (IPv4)
                  #"0x0806"]   #Address Resolution Protocol (ARP)

    def generateRandomDlType(self):
        #TODO: change this method in case of L3 and L4 flows
        randomEtherTypeIndex = random.randint(0, len(self.etherTypes) - 1)
        dlType = self.etherTypes[randomEtherTypeIndex]
        return dlType

    def generateRandomDlVlanId(self):
        vlanId = random.randint(0, 65535)
        return vlanId

    def generateRandomWaitTime(self, maxWait = 60):
        waitTime = random.randint(0,maxWait)
        return waitTime

    def generateRandomBurstSize(self, maxBurstSize = 300):
        burstSize = random.randint(1, maxBurstSize)
        return burstSize

    def generateRandomL4ProtocolType(self):
        if(random.randint(0,1)):
            protocolType = 17
        else:
            protocolType = 6
        return protocolType


    #this is to avoid in_port and output action port to be the same number
    inPortTmp = 0

    def __assignValues(self, flowParameters):
        #count flow params distribution (how many flows with how many parameters generated)
        self.__countFlowParamsNumber(flowParameters)
        flow = ""
        for i in range(len(flowParameters)):
            if(flowParameters[i] == "in_port="):
                self.inPortTmp = self.generateRandomiOFPortNumber()
                self.__countFlowsOnPortDistribution(self.inPortTmp)
                flow = flow + flowParameters[i] + str(self.inPortTmp) + ","
            elif(flowParameters[i] == "dl_type="):
                flow = flow + flowParameters[i] + str(self.generateRandomDlType()) + ","
            elif(flowParameters[i] == "dl_vlan="):
                flow = flow + flowParameters[i] + str(self.generateRandomDlVlanId()) + ","
            elif((flowParameters[i] == "dl_src=") or (flowParameters[i] == "dl_dst=")):
                flow = flow + flowParameters[i] + self.generateRandomMACAddress() + ","
            elif(flowParameters[i] == "nw_proto="):
                flow = flow + flowParameters[i] + str(self.generateRandomL4ProtocolType()) + ","
            elif((flowParameters[i] == "nw_src=") or (flowParameters[i] == "nw_dst=")):
                flow = flow + flowParameters[i] + self.generateRandomIPAddress() + ","
            elif((flowParameters[i] == "tp_src=") or (flowParameters[i] == "tp_dst=")):
                flow = flow + flowParameters[i] + str(self.generateRandomL4PortNumber()) + ","
            elif(flowParameters[i] == "actions=output:"):
                flow = flow + flowParameters[i] + str(self.__generateActionOutputPortNumber(self.inPortTmp))
            else:
                print "Unknown flow parameter - discarding"

        return flow

    def __generateActionOutputPortNumber(self, inPortNumber):
        outputActionPort = self.generateRandomiOFPortNumber()
        if(outputActionPort == inPortNumber):
            print "The same output action port as in_port - regenerating"
            outputActionPort = self.__generateActionOutputPortNumber(inPortNumber)
        print "inport = %d, outport = %d" % (inPortNumber, outputActionPort)
        return outputActionPort



# The rest of defined ether types does not seem to be supported by ovs-ofctl and ovs-controller parsers
# when checking for flow correcteness. So parameter dl_type is limited only to 2 randomly chosen values

#0x0842  Wake-on-LAN Magic Packet, as used by ether-wake and Sleep Proxy Service
#0x1337  SYN-3 heartbeat protocol (SYNdog)
#0x6003  DECnet Phase IV
#0x8035  Reverse Address Resolution Protocol (RARP)
#0x809B  AppleTalk (Ethertalk)
#0x80F3  AppleTalk Address Resolution Protocol (AARP)
#0x8100  VLAN-tagged frame (IEEE 802.1Q)
#0x8137  Novell IPX (alt)
#0x8138  Novell
#0x86DD  Internet Protocol, Version 6 (IPv6)
#0x8808  MAC Control
#0x8809  Slow Protocols (IEEE 802.3)
#0x8819  CobraNet
#0x8847  MPLS unicast
#0x8848  MPLS multicast
#0x8863  PPPoE Discovery Stage
#0x8864  PPPoE Session Stage
#0x886F  Microsoft NLB heartbeat [3]
#0x8870  Jumbo Frames
#0x887B  HomePlug 1.0 MME
#0x888E  EAP over LAN (IEEE 802.1X)
#0x8892  PROFINET Protocol
#0x889A  HyperSCSI (SCSI over Ethernet)
#0x88A2  ATA over Ethernet
#0x88A4  EtherCAT Protocol
#0x88A8  Provider Bridging (IEEE 802.1ad)
#0x88AB  Ethernet Powerlink
#0x88CC  LLDP
#0x88CD  SERCOS III
#0x88D8  Circuit Emulation Services over Ethernet (MEF-8)
#0x88E1  HomePlug AV MME
#0x88E5  MAC security (IEEE 802.1AE)
#0x88F7  Precision Time Protocol (IEEE 1588)
#0x8902  IEEE 802.1ag Connectivity Fault Management (CFM) Protocol / ITU-T Recommendation Y.1731 (OAM)
#0x8906  Fibre Channel over Ethernet
#0x8914  FCoE Initialization Protocol
#0x9000  Configuration Test Protocol (Loop)[4]
#0x9100  Q-in-Q
#0xCAFE  Veritas Low Latency Transport (LLT)[5]
