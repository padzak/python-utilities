# script used to run same script multiple times on a remote with the SLUMR queue 
# the sources to be used by this script have to be previously uploaded via FTP 

import paramiko as pm

host = ""
port = 22
username = ""
password = ""
directory = ""
instancesNumber = 10

# below paths regard the remote server
# path to the directory in which code instances will be excecuted  
destinationPath = "destinationPath"
scriptName = "scriptName.sh"
# path to the directory containing the script and code to be excecuted 
codePath = "codePath"


# preparing code instances for queue submission
command = "cd " + destinationPath
for instance in range(instancesNumber):
    
    no = str(instance)
    command += " && mkdir " + no + " && cp -r ../" + codePath + "/. ./" + no


client = pm.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(pm.AutoAddPolicy())
client.connect(host, port, username, password)
channel = client.invoke_shell()

stdin, stdout, stderr = client.exec_command(command)

stdin.close()
stdout.close()
client.close()


# submitting jobs to queue
for instance in range(instancesNumber):

    no = str(instance)
    command = "cd " + destinationPath + "/" + no + " && sbatch " + scriptName

    client = pm.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(pm.AutoAddPolicy())
    client.connect(host, port, username, password)
    channel = client.invoke_shell()

    stdin, stdout, stderr = client.exec_command(command)

    stdin.close()
    stdout.close()
    client.close()


