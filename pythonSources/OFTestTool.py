
import sys, os, time, subprocess, datetime

import ConfigurationReader

class OFTestTool:

    """Base class for OFTest framework"""

    def __init__(self):
        self.myConfiguration = ConfigurationReader.ConfigurationReader()
        self.myConfiguration.showConfiguration()
        self.switchIP = self.myConfiguration.switchIP
        self.switchID = self.myConfiguration.switchID                                             
        self.switchUser = self.myConfiguration.switchUser

    def addFlow(self,flowDefinition):
        subprocess.call([self.myConfiguration.ovsToolsDir + '/ovs-ofctl', 'junos-add-flow', '-v', 'unix:junos_socket', flowDefinition])


    def delFlow(self,flowDefinition):
        subprocess.call([self.myConfiguration.ovsToolsDir + '/ovs-ofctl', 'junos-del-flow', '-v', 'unix:junos_socket', flowDefinition])


    def sendPacketOut(self, outputPortNumberString):
        subprocess.call([self.myConfiguration.ovsToolsDir + '/ovs-ofctl', 'junos-packet-out', '-v', 'unix:junos_socket', outputPortNumberString])


    def wait(self,timeToWait):
        time.sleep(timeToWait)


    def flushFlows(self):
        pid = None
        localUser = os.getlogin()
        fd = os.popen("ps -e -o pid,command,user | grep ovs-controller | grep " + localUser + " | grep -v grep")
        psOutput = fd.read()
        controllerPid = psOutput.strip().split(' ')[0]
        print 'controller PID: ', controllerPid
        command = 'kill -9 ' + controllerPid
        subprocess.call(command,shell=True)
        time.sleep(20)
        command = './StartController' 
        subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)

    def restartFirewall(self):
        command = 'ssh %s@%s "cli restart firewall"' % (self.switchUser, self.switchIP)
        tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


    def restartSampling(self):
        command = 'ssh %s@%s "cli restart sampling' % (self.switchUser, self.switchIP)
        tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


    def restartOFSwitchd(self):
        command = 'ssh %s@%s "cli restart openflow-application"' % (self.switchUser, self.switchIP)
        tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


    def restartAll(self):
        self.restartFirewall()
        self.restartSampling()
        self.restartOFSwitchd()


    def clearSwitchLogs(self, forceClear = 0):
        doClear = 1
        if(not forceClear):
            doClear = self.__getUserDecision("Would you like to clear logs on tested switch? [y/n]")
        if(doClear):
            command = 'ssh %s@%s "cli clear log messages"' % (self.switchUser, self.switchIP)
            tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        else:
            print "Logs not cleared"


    def getSwitchLogs(self):
        command = 'scp %s@%s:/var/log/messages .' % (self.switchUser, self.switchIP)
        tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    def clearSwitchTraces(self, forceClear = 0):
        doClear = 1
        if(not forceClear):
            doClear = self.__getUserDecision("Would you like to clear traces on tested switch? [y/n]")
        if(doClear):
            command = 'ssh %s@%s "cli clear log %s"' % (self.switchUser, self.switchIP, self.myConfiguration.switchTraceFile)
            tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        else:
            print "Traces not cleared"
        return doClear


    def waitTillQueueLength(self, queueLength):
        while True:
            command = 'ssh %s@%s "setenv COLUMNS 120; cli show openflow switch statistics queue %s"'  % (self.switchUser, self.switchIP, self.switchID)
            tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            tmp.wait()
            output = tmp.communicate()
            queueLengthActual = output[0].strip().split(" ")[1].split(":")[1]
            queueLengthActual = int(queueLengthActual)
            print "Waiting for queue length to be less than %d. Actual state: %d" % (queueLength, queueLengthActual)
            if(queueLengthActual <= queueLength):
                break
            time.sleep(5)
 

    def getFlowsNumber(self):
        command = 'ssh %s@%s "setenv COLUMNS 120; cli show openflow switch statistics aggregate %s | grep flow_count"'  % (self.switchUser, self.switchIP, self.switchID)
        tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmp.wait()
        output = tmp.communicate()
        flowsNumber = int(output[0].strip().split(" ")[2].split("=")[1])
        print "Actual number of flows: %d" % (flowsNumber)
        return flowsNumber


    def getPortsNumber(self):
        command = 'ssh %s@%s "setenv COLUMNS 120; cli show openflow switch statistics ports %s | grep ports"'  % (self.switchUser, self.switchIP, self.switchID)
        tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmp.wait()
        output = tmp.communicate()
        portsNumber = int(output[0].strip().split(" ")[0])
        print "Actual number of configured ports: %d" % (portsNumber - 1)
        return portsNumber - 1 #local port not couted

    
    def getOFApplicationPID(self):
        command = 'ssh %s@%s "setenv COLUMNS 120; cli show openflow switch controller-status %s | grep pid"' % (self.switchUser, self.switchIP, self.switchID)
        tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmp.wait()
        output = tmp.communicate()
        pid = int(output[0].strip().split("=")[1])
        print "Actual pid of openflow-application: %d" % (pid)
        return pid

    def initBeforeTest(self):
        pid = None
        localUser = os.getlogin()
        fd = os.popen("ps -e -o pid,command,user | grep ovs-controller | grep " + localUser + " | grep -v grep")
        psOutput = fd.read()
        if psOutput:
            if self.getFlowsNumber() > 0:
                self.flushFlows()
                time.sleep(20)
        else:
            command = './StartController'
            subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)
            time.sleep(20)


    def measureFlowsLoadTime(self, firstFlowCookie, lastFlowCookie):
        firstCookieHexString = str(hex(firstFlowCookie))
        command = 'ssh %s@%s "setenv COLUMNS 120; grep flow_mod /var/log/%s | grep cookie:%s"' \
        % (self.switchUser, self.switchIP, self.myConfiguration.switchTraceFile, firstCookieHexString)
        tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmp.wait()
        output = tmp.communicate()
        startTimeString = output[0].strip().split(" ")[2]

        lastCookieHexString = str(hex(lastFlowCookie))
        command = 'ssh %s@%s "setenv COLUMNS 120; grep -A1  \'Following new flow\' /var/log/%s | grep -B1 cookie:%s"' \
        % (self.switchUser,self.switchIP,self.myConfiguration.switchTraceFile, lastCookieHexString)
        tmpp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmpp.wait()
        outputt = tmpp.communicate()
        endTimeString = outputt[0].strip().split(" ")[2]

        startTime = datetime.datetime(*(time.strptime(startTimeString, "%H:%M:%S")[0:6]))
        endTime = datetime.datetime(*(time.strptime(endTimeString, "%H:%M:%S")[0:6]))

        print "Time spent to add flows: " + str(endTime - startTime)


    def countDiscardedFlows(self):
        command = 'ssh %s@%s "setenv COLUMNS 120; grep -c \'type3(OFPET_FLOW_MOD_FAILED)\'  /var/log/%s"' \
        % (self.switchUser, self.switchIP, self.myConfiguration.switchTraceFile)
        tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmp.wait()
        output = tmp.communicate()
        return int(output[0])


    def clearOFSwitchdCoreDumps(self):
        command = 'ssh %s@%s "ls /var/tmp/ | grep of-switchd.core-tarball"' % (self.switchUser, self.switchIP)
        tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmp.wait()
        output = tmp.communicate()
        files =  output[0].strip().split()

        for file in files:
            command = 'ssh root@%s "rm /var/tmp/%s"' % (self.switchIP, file)
            tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


    def clearDfwdCoreDumps(self):
        command = 'ssh %s@%s "ls /var/tmp/ | grep dfwd.core-tarball"' % (self.switchUser, self.switchIP)
        tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmp.wait()
        output = tmp.communicate()
        files =  output[0].strip().split()

        for file in files:
            command = 'ssh root@%s "rm /var/tmp/%s"' % (self.switchIP, file)
            tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


    def clearSampledCoreDumps(self):
        command = 'ssh %s@%s "ls /var/tmp/ | grep sampled.core-tarball"' % (self.switchUser, self.switchIP)
        tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmp.wait()
        output = tmp.communicate()
        files =  output[0].strip().split()

        for file in files:
            command = 'ssh root@%s "rm /var/tmp/%s"' % (self.switchIP, file)
            tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


    def getOFSwitchdCoreDumps(self):
        command = 'ssh %s@%s "ls /var/tmp/ | grep of-switchd.core-tarball"' % (self.switchUser, self.switchIP)
        tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmp.wait()
        output = tmp.communicate()
        files =  output[0].strip().split()
        
        for file in files:
            command = 'scp root@%s:/var/tmp/%s .' % (self.switchIP, file)
            tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


    def getDfwdCoreDumps(self):
        command = 'ssh %s@%s "ls /var/tmp/ | grep dfwd.core-tarball"' % (self.switchUser, self.switchIP)
        tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmp.wait()
        output = tmp.communicate()
        files =  output[0].strip().split()

        for file in files:
            command = 'scp root@%s:/var/tmp/%s .' % (self.switchIP, file)
            tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


    def getSampledCoreDumps(self):
        command = 'ssh %s@%s "ls /var/tmp/ | grep sampled.core-tarball"' % (self.switchUser, self.switchIP)
        tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        tmp.wait()
        output = tmp.communicate()
        files =  output[0].strip().split()

        for file in files:
            command = 'scp root@%s:/var/tmp/%s .' % (self.switchIP, file)
            tmp = subprocess.call(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


    def __getUserDecision(self, questionString="[y/n]"):
        doIt = -1
        while True:
            print questionString
            keyPressed = sys.stdin.read(1)
            if(keyPressed == 'y'):
                doIt = 1
                break
            if(keyPressed == 'n'):
                doIt = 0
                break
            else:
                print "You must choose either 'y' or 'n' !!!"
        return doIt
        
