import subprocess, signal, sys, time, string 
import ConfigurationReader


class ResourcesMonitor:


    """Class getting info about resources distribution on switch side during test case processing"""

    def __init__(self):
        self.myConfiguration = ConfigurationReader.ConfigurationReader()
        self.resourcesFileName = self.myConfiguration.resourcesFilePref #TODO" addd current time date to the resources file name
        self.fileHandler = open(self.resourcesFileName, 'w')
        signal.signal(signal.SIGUSR1, self.signalHandler)
        self.monitorResources()


    def monitorResources(self):
        switchIP = self.myConfiguration.switchIP
        switchID = self.myConfiguration.switchID
        switchUser = self.myConfiguration.switchUser
        samplingFrequency = str(self.myConfiguration.samplingFreq)

        command = 'ssh %s@%s "setenv COLUMNS 120; date +%%s; ps aux | grep -e dfwd -e sampled -e of-switchd | grep -v grep;  cli show openflow switch statistics aggregate %s | grep flow_count"'  % (switchUser, switchIP, switchID)
        while True:
            tmp = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            tmp.wait()
            output = tmp.communicate()
            self.fileHandler.write(self.__prepareOutput(output[0]))
            self.fileHandler.flush()
            time.sleep(float(samplingFrequency))


    def signalHandler(self, signalNumber, parameter):
        print 'Signal received to stop child process'
        self.fileHandler.close()		
        sys.exit(0)

    def __prepareOutput(self, output):
        splittedOutput = output.split('\n')
        dateOfMeasure = splittedOutput[0].strip()
        ofAppMemory = 0
        ofAppCpu = 0
        for i in splittedOutput:
            splittedPsLine = i.strip().split()
            if len(splittedPsLine) > 10:
                if (splittedPsLine[10].find("of-switchd") >=0):
                    ofAppMemory += float(splittedPsLine[4])
                    ofAppCpu += float(splittedPsLine[2])
    
                if (splittedPsLine[10].find("dfwd") >= 0):
                    dfwdMemory = splittedPsLine[4]
                    dfwdCpu = splittedPsLine[2]
                
                if (splittedPsLine[10].find("sampled") >= 0):
                    sampledMemory = splittedPsLine[4]
                    sampledCpu = splittedPsLine[2]
        flowsNumber = splittedOutput[len(splittedOutput)-2].strip().split(' ')[2].split('=')[1]
        formattedOutput = dateOfMeasure + " " + str(ofAppMemory) + " " + str(ofAppCpu) + " " + dfwdMemory + " " + dfwdCpu + " " + sampledMemory + " " + sampledCpu + " " + flowsNumber + '\n'
        return formattedOutput




