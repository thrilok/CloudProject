import boto3
import json
import sys
import os
import subprocess
from pprint import pprint

class actions:
	ec2 = boto3.resource('ec2', region_name='us-west-2')
	dns = {
	
	}
	def createKeyPair(self):
		file_name = sys.argv[2]
		outfile = open(file_name,'w')
		key_pair = self.ec2.create_key_pair(KeyName=file_name)
		KeyPairOut = str(key_pair.key_material)
		outfile.write(KeyPairOut)
		
	def createInstance(self):
		config_file = open('config.json', 'r')
		configuration = json.load(config_file)
		instance = self.ec2.create_instances(ImageId=configuration['Id'],
										MinCount=configuration['MinCount'],
										MaxCount=configuration['MaxCount'],
										InstanceType=configuration['Type'],
										KeyName=configuration["Key"])
		print("Instance created with the instnace id {}".format(instance[0].instance_id))

	def getInstances(self):
		ec2client = boto3.client('ec2', region_name='us-west-2')
		response = ec2client.describe_instances()
		for reservation in response["Reservations"]:
			for instance in reservation["Instances"]:
				print("id - {};\t status - {};\t public DNS - {}".format(instance["InstanceId"], instance['State']['Name'], instance['PublicDnsName']))

	def startInstance(self, instance_id):
		instance = self.ec2.Instance(instance_id)
		instance.start()
		
	def rebootInstance(self, instance_id):
		instance = self.ec2.Instance(instance_id)
		instance.reboot()
		
	def stopInstance(self, instance_id):
		instance = self.ec2.Instance(instance_id)
		instance.stop()

	def terminateInstance(self, instance_id):
		instance = self.ec2.Instance(instance_id)
		instance.terminate()
	
	def getAddress(self):
		ec2client = boto3.client('ec2', region_name='us-west-2')
		response = ec2client.describe_instances()
		for reservation in response["Reservations"]:
			for instance in reservation["Instances"]:
				self.dns[instance["InstanceId"]] = instance['PublicDnsName']
	
	def runApplication(self, instance_id):
		subprocess.call(['sudo','chmod', '+x', 'script.sh'])
		push_script = "scp -i cloud_test.pem script.sh ubuntu@"+self.dns[instance_id]+":"
		push_script = push_script.split(" ")
		subprocess.call(push_script)
		login = "ssh -i cloud_test.pem ubuntu@"+self.dns[instance_id]+" chmod +x script.sh && ./script.sh"
		login = login.split(" ")
		subprocess.call(login)
		pull_result = "scp -i cloud_test.pem ubuntu@"+self.dns[instance_id]+":~/blast_example/results.txt localpath/to/save"
		pull_result = pull_result.split(" ")
		subprocess.call(pull_result)

if __name__ == '__main__':
	demoActions = actions()
	if sys.argv[1] == "--help" or sys.argv[1] == "-h":
		print("\n"
		      "Usage: \n"
		      "\tpython InstanaceActions.py <options>\n"
		      "Options:\n"
		      "\tcreateInstance\n"
		      "\tgetInstances\n"
		      "\tstart instance_id\n"
		      "\tstop instance_id\n"
		      "\treboot instance_id\n"
		      "\tterminate instance_id\n")
	if sys.argv[1] == "createInstance":
		demoActions.createInstance()
	elif sys.argv[1] == "getInstances":
		demoActions.getInstances()
	elif sys.argv[1] == "start":
		instance = sys.argv[2]
		demoActions.startInstance(instance)
	elif sys.argv[1] == "stop":
		instance = sys.argv[2]
		demoActions.stopInstance(instance)
	elif sys.argv[1] == "reboot":
		instance = sys.argv[2]
		demoActions.rebootInstance(instance)
	elif sys.argv[1] == "terminate":
		instance = sys.argv[2]
		demoActions.terminateInstance(instance)
	elif sys.argv[1] == "run":
		instance = sys.argv[2]
		demoActions.getAddress()
		demoActions.runApplication(instance)
	else:
		print("Please enter correct arguments\n")
