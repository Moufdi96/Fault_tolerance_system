# Fault tolerance system implemented using PBR (Primary-Backup Replication) + TR (Temporal Redundancy) + Satble memory 
The Service delivered by the servers is simply the mean computation of the last n received values from sensor. The n last received values are stored along with their mean result in a json file representing the stable memory. 

Move to the project directory

Open 4 terminals :

* Start the 'Primary server' in the 1st terminal using this command "python3 launch_server1.py"
* Start the 'Backup server' in the 2nd terminal using this command "python3 launch_server2.py"
* Launch the 'Watchdog' in the 3rd terminal using this command "python3 launch_watchdog.py"
* Start the 'Sensor' in the 4th terminal using this command "python3 launch_sensor.py"
 
 To Simulate crash faults just kill the 'launch_server1.py' process using Ctrl+c, the backup will launch automatically
 
 To simulate value faults you may change this two lines of code to generate random value faults injection (this can be viewed as a bit-flip for example) :
 
 * File serverMachine.py, line 24 =========> res_1 = self.computeMean(self.data,faulInjection=True)
 * File serverMachine.py, line 28 =========> res_2 = self.computeMean(self.data,faulInjection=True)
 
