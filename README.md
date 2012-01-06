OpenFlow Test Tool (OFTT)
========================

Copyright (c) 2011 Juniper Networks.

VERSION 1.0 

What is OFTT?
-------------

OFTT is a test harness that enables the performance of different tests against an Openflow switch. OFTT uses the OpenVswitch OpenFlow controller module, which has been modified for testing purposes. A python-based test language is used to define test cases when are executed against the device under test (DUT).

In OFTT, tests consist of adding and deleting different flow combinations within different time intervals. When used against the JUNOS OpenFlow implementation, information is also gathered from the operating system on the device under test (DUT) in respect to resource usage while the test cases are being executed.

NOTE - this test framework does not interact with a traffic-generation source. A traffic-generator should be used for generating the traffic streams against which the flow-matching will take place but the traffic-generator is controlled independently.

NOTE - Only one switch instance is supported per OFTT instance.

The package consists of the modified Open VSwitch controller together with a set of test-cases which can be executed against the DUT. The test-cases can be modified to suit the user's needs.

The OFTT package is executed on a Linux host platform that must have network access to the Openflow switch device under test.

Requirements
------------
Linux distribution including GCC and GNU Make including libc-devel (and Development Tools packages for your Linux distribution)

Python 2.4.3 or later

JUNOS SDK Openflow Application v1.0 or later

Openflow 1.0 compliant switch

Installation
------------

1. download the .gz file containing the OFTT files

Further steps of this instruction assume that you are in package top directory <OFTestTools>

2. 'cd ./ovsTtools'

3. 'make'. This will build the ovs-controller, ovs-ofctl module (part of Open VSwitch package) as well as the OFTT modules. 
	
	You should not see any compilation errors. 'ovs-controller' and 'ovs-ofctl' binaries should appear in OVS_tools directory (compilation tested with GCC 4.1.2 20080704 (Red Hat 4.1.2-48) and GNU Make 3.81)
	
4. 'cd ..'

5. 'chmod 777 StartController ExecuteTest' (if needed)

6. Change the configuration file 'configuration.cfg' according to your needs 
   (see 'Configuration file structure' section for details)

7. Enable key-based ssh authentication for a configured user between the DUT and OFTT 
	(see 'Miscellaneous' section below)

NOTE: If you are using non-default (6633) port number for OpenFlow control channel communication between the DUT and OFTT, you must modify the 'StartController' file. 

OFTT Operation
--------------

1) './StartController' -> this will execute the script to start the OFTT controller. In the case where the DUT has already been configured to communicate with the controller, a connection will be established using the configured TCP port. The DUT can be configured at a later point and still successfully connect to the OFTT controller.

During the DUT connection to OFTT controller you should see something like this:

-bash-3.2$ ./StartController
Oct 14 07:09:19|00001|poll_loop|DBG|[POLLIN] on fd 3: 0x40e7ea 0x4207c9 0x41f74e 0x4188fa 0x417ef5 0x402f84
Oct 14 07:09:19|00002|rconn|DBG|tcp:<SW_IP>:<port>: entering ACTIVE
Oct 14 07:09:19|00003|vconn|DBG|tcp:<SW_IP>:<port>: sent (Success): hello (xid=0x7ecb1):
Oct 14 07:09:19|00004|poll_loop|DBG|[POLLIN] on fd 8: 0x40e7ea 0x42058e 0x41f3f6 0x41f42e 0x418751 0x417bf5 0x410ec3 0x402fc0
Oct 14 07:09:19|00005|poll_loop|DBG|[POLLIN] on fd 8: 0x40e7ea 0x42058e 0x41f3f6 0x41f42e 0x418751 0x417bf5 0x41102c 0x402fcd
Oct 14 07:09:19|00006|vconn|DBG|tcp:<SW_IP>:<port>: received: hello (xid=0xe4ff0):


2) './Executetest testCases/testCase' -> this step will execute the the test case 'testCase'. All test cases should be placed in the './testCases' directory (test cases tested using Python 2.4.3)

Example of successful test run :

-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
-bash-3.2$ ./ExecuteTest testCases/Flows002.py
Running test case: Flows002
Current Configuration:
Section Installation Dirs:
OVS tools installation dir:  ovsTools
Section Switch
Switch IP address:  <SW_IP>
Switch ID:  0
Switch user:  regress
Switch tracefile name: ext/juniperipgcto/of_trace
Section Resources Manager
Resources file prefix:  system_resources
Switch resources sampling frequency:  10
Oct 17 06:48:01|00001|ofctl|INFO|do_junos_add_flow: args received: in_port=1,dl_type=0x800,dl_vlan=0,dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2
Oct 17 06:48:01|00001|ofctl|INFO|do_junos_add_flow: args received: in_port=1,dl_type=0x800,dl_vlan=1,dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2
Oct 17 06:48:01|00001|ofctl|INFO|do_junos_add_flow: args received: in_port=1,dl_type=0x800,dl_vlan=2,dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2
Oct 17 06:48:01|00001|ofctl|INFO|do_junos_add_flow: args received: in_port=1,dl_type=0x800,dl_vlan=3,dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2
Oct 17 06:48:01|00001|ofctl|INFO|do_junos_add_flow: args received: in_port=1,dl_type=0x800,dl_vlan=4,dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2
Oct 17 06:48:01|00001|ofctl|INFO|do_junos_add_flow: args received: in_port=1,dl_type=0x800,dl_vlan=5,dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2
Oct 17 06:48:01|00001|ofctl|INFO|do_junos_add_flow: args received: in_port=1,dl_type=0x800,dl_vlan=6,dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2
Oct 17 06:48:01|00001|ofctl|INFO|do_junos_add_flow: args received: in_port=1,dl_type=0x800,dl_vlan=7,dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2
Oct 17 06:48:01|00001|ofctl|INFO|do_junos_add_flow: args received: in_port=1,dl_type=0x800,dl_vlan=8,dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2
Oct 17 06:48:01|00001|ofctl|INFO|do_junos_add_flow: args received: in_port=1,dl_type=0x800,dl_vlan=9,dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2
You may now check whether the flows were added to OF app...
Invoke "show openflow switch statistics flows <SW_ID>" command in the switch console
Also automatic check is going to be processed
Actual number of flows: 10
TEST OK :)
Signal received to stop child process
User defined signal 1
-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-



Configuration file structure ('configuration.cfg')
--------------------------------------------------

[Installation Dirs]
OVS_TOOLS_DIR: ovsTools                     	#Path to directory with OVS tools binaries 

[Switch]
SWITCH_IP: 10.1.1.1                          	#IP address / hostname of a switch to be tested
SWITCH_ID: 0									#The id of a switch configured on DUT
SWITCH_USER: lab                            	#Username configured on the DUT
SWITCH_TRACEFILE: ext/juniperipgcto/of_trace	#Location of TRACES on the DUT

[Resources Monitor]
RESOURCES_FILE_PREFIX: system_resources     	#Name of a file to which switch resources information is written during test
												#case execution. NOTE - This is a JUNOS-specific function.
SAMPLING_FREQUENCY: 3                       	#Switch resources sampling frequency. NOTE - This is a JUNOS-specific 
										    	#function.


JUNOS Resources Monitor
-----------------------
The resources monitor is a separate process, which collects information from the DUT during test execution. This is a JUNOS-specific function and does not apply to generic OpenFlow switches when configured as the DUT.

The resource monitor process is started automatically when the test case is executed. Currently information about following processes is gathered: dfwd, sampled, of-switchd. The number of programmed flow entries is also gathered. 
The results are written to file configured in RESOURCES_FILE_PREFIX option value in test tool configuration.


Miscellaneous
-------------
In order to enable key-based SSH authentication between OFTT and the DUT, one must generate the required keys on the OFTT host machine and copy the key onto the DUT. For JUNOS, follow the following steps:

1. Invoke 'ssh-keygen -t rsa' on OFTT host machine. Use default values for each option to be set. 
   This will generate a private and public keypair in '~/.ssh' directory (id_rsa and id_rsa.pub). 

2. Ensure that there is a user account created on the DUT where the username == the username contained in the configuration.cfg file. This can be done using the following 'set' commands in configuration mode:

	'set system login user <configured_user> class super-user'
	'commit'

3. Copy the public key (id_rsa.pub) to the DUT to '/var/home/<configured_user>/.ssh'. This can be acheived using a range of file-transfer options from the router including FTP and scp. 

3. Add the key to the user account by logging in to the DUT and in JUNOS configuration mode, issue the command:

   'set system login user <configured_user> authentication load-key-file <path_to_public_key>'
   'commit'
   
4. Check that ssh access is now working by trying to start an ssh session from the OFTT host machine to the DUT 
	(ssh <configured_user>@<DUT ip address or DNS name>). Access to the configured user account should be now enabled without entering the password.



Writing test cases
------------------
All test cases should be placed in './testCases' directory. Each individual test case should be placed in separate file. 
There is no fixed format for the test case filename. 

Each testcase is programmatically defined as a Python class named 'TestCase'. Each test case should instantiate the OFTestTool class object in its constructor. Each test case should implement a method called 'run' where the test case execution is programmed. The example below provides a basic test-case container:

-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

import sys
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is an example test case"""

        def __init__(self):
            self.myOFTestTool = OFTestTool.OFTestTool()

        def run(self):

        """Write your test code here. Use methods from OFTestTool class"""
        
             self.myOFTestTool.aMethodFromOFTestToolClass()
-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-


The following example is located in directory "testCases".

The following test case (Flows002.py) adds 10 flows that match:

incoming port 1, 
Ethernet frame type: 0x800, 
Input VLAN id: 0-9, 
Ethernet destination address: 00:33:44:22:11:11, 
IP protocol: 6 (TCP), 
Action : forward via port 2.

-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

import sys, socket, struct
import OFTestTool

sys.path.append('../')

class TestCase:

    """This is FLOWS002 example test case defined in test template document -> add predefined flows to the application"""

    def __init__(self):
        self.myOFTestTool = OFTestTool.OFTestTool()

    def run(self):
        numberOfFlows = 10

        for n in range(numberOfFlows):

            flow = "in_port=1,dl_type=0x800,dl_vlan=" + str(n) + ",dl_dst=00:33:44:22:11:11,nw_proto=6,actions=output:2"
            self.myOFTestTool.addFlow(flow)

        print "You may now check whether the flows were added to OF app... \n" \
              "Invoke \"show openflow switch statistics flows <SW_ID>\" command in the switch console \n" \
              "Also automatic check is going to be processed "

        self.myOFTestTool.wait(5)

        if(self.myOFTestTool.getFlowsNumber() != numberOfFlows):
            print "Automatic check failed !!! - not all expected flows were added to OF app"
            return

        print "TEST OK :)"
-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

TestTool class: 
This class is implementing a set of tools / methods which can be used while defining test cases.

The following methods are currently supported:

* addFlow(flowDefinition)		 		/* Add a new flow */
* delFlow(flowDefinition) 				/* Delete existing flow ('strict' currenty not supported) */
* wait(timeToWait)						/* Simple sleep */
* sendPacketOut(outputPortNumberString)	/* Send packet-out message with output port as parameter (the packet currently contains a 64 byte payload set to 0x00) */
* flushFlows()							/* Stop controller, wait, start controller */
* restartFirewall()						/* Restart the firewall daemon on DUT - JUNOS SPECIFIC */
* restartSampling()						/* Restart the sampling daemon on DUT - JUNOS SPECIFIC */
* restartOFSwitchd()					/* Restart the openflow daemon on DUT - JUNOS SPECIFIC */
* restartAll()							/* Perform firewall, sampled and openflow restart - JUNOS SPECIFIC */ 
* clearSwitchLogs(forceClear = 0)		/* Clear message log on DUT */
* getSwitchLogs()						/* Get the /var/log/messages file from DUT - JUNOS SPECIFIC */
* clearSwitchTraces()					/* Clear the traces file (location defined in configuration.cfg) - JUNOS SPECIFIC */
* waitTillQueueLength(queueLength)		/* Wait until DUT request queue will be less than input number  */
* getFlowsNumber()						/* Print and return actual number of flows on DUT */
* getPortsNumber()						/* Print and return number of configured ports */
* getOFApplicationPID()					/* Print and return the PID of switch */ 
* measureFlowsLoadTime(firstFlowCookie, lastFlowCookie)	/* Print the time spent to add flows identified by firstFlowCookie and lastFlowCookie */
* countDiscardedFlows()					/* Return the number of discarded flows */ 
* clearOFSwitchdCoreDumps()				/* Clear any of-switchd core dump files on DUT - JUNOS SPECIFIC */ 
* clearDfwdCoreDumps()					/* Clear any dfwd core dump files on DUT - JUNOS SPECIFIC */
* clearSampledCoreDumps() 				/* Clear any sampled core dump files on DUT - JUNOS SPECIFIC */
* getOFSwitchdCoreDumps() 				/* Get any of-switchd core dump files from DUT - JUNOS SPECIFIC */
* getDfwdCoreDumps()				    /* Get any dfwd core dump files from DUT - JUNOS SPECIFIC */	
* getSampledCoreDumps()					/* Get any sampled core dump files from DUT - JUNOS SPECIFIC */


Questions
---------
mailto:networkprogrammability@juniper.net

NOTICE
------
This section is included in compliance with the Apache 2.0 license, available at 

http://www.apache.org/licenses/LICENSE-2.0.html

OpenFlow Test Tool
Copyright (c) 2011 Juniper Networks, Inc.

Open vSwitch
Copyright (c) 2007, 2008, 2009 Nicira Networks.

Apache Portable Runtime
Copyright 2008 The Apache Software Foundation.

This product includes software developed by The Apache Software Foundation (http://www.apache.org/).
Portions of this software were developed at the National Center for Supercomputing Applications (NCSA) at the University of Illinois at Urbana-Champaign.

COPYING
-------
This file is a summary of the licensing of files in this distribution.
Some files may be marked specifically with a different license, in
which case that license applies to the file in question.
 
The files contained in the directory 'ovsTools' are licensed under the Apache License, Version 2.0:
 
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:

        http://www.apache.org/licenses/LICENSE-2.0
 
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Files under python/ are licensed under the Python Software Foundation License, version 2:

PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
--------------------------------------------

1. This LICENSE AGREEMENT is between the Python Software Foundation
("PSF"), and the Individual or Organization ("Licensee") accessing and
otherwise using this software ("Python") in source or binary form and
its associated documentation.

2. Subject to the terms and conditions of this License Agreement, PSF
hereby grants Licensee a nonexclusive, royalty-free, world-wide
license to reproduce, analyze, test, perform and/or display publicly,
prepare derivative works, distribute, and otherwise use Python
alone or in any derivative version, provided, however, that PSF's
License Agreement and PSF's notice of copyright, i.e., "Copyright (c)
2001, 2002, 2003, 2004, 2005, 2006, 2007 Python Software Foundation;
All Rights Reserved" are retained in Python alone or in any derivative
version prepared by Licensee.

3. In the event Licensee prepares a derivative work that is based on
or incorporates Python or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to Python.
 
4. PSF is making Python available to Licensee on an "AS IS"
basis.  PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

7. Nothing in this License Agreement shall be deemed to create any
relationship of agency, partnership, or joint venture between PSF and
Licensee.  This License Agreement does not grant permission to use PSF
trademarks or trade name in a trademark sense to endorse or promote
products or services of Licensee, or any third party.

8. By copying, installing or otherwise using Python, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.

