# Adapted from: https://github.com/keivanK1/aws-create-thing-boto3/blob/master/createThing-Cert.py

################################################### Connecting to AWS
import boto3
import os
import json
################################################### Create random name for things
import random
import string

################################################### Parameters for Thing
thingArn = ''
thingId = ''
defaultPolicyName = 'Thing1_Policy'
###################################################

def createThing(thingName):
  global thingClient
  thingResponse = thingClient.create_thing(
      thingName = thingName
  )
  data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
  for element in data: 
    if element == 'thingArn':
        thingArn = data['thingArn']
    elif element == 'thingId':
        thingId = data['thingId']
    createCertificate(thingName)

def createCertificate(thingName):
	global thingClient
	certResponse = thingClient.create_keys_and_certificate(
			setAsActive = True
	)
	data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
	for element in data: 
			if element == 'certificateArn':
					certificateArn = data['certificateArn']
			elif element == 'keyPair':
					PublicKey = data['keyPair']['PublicKey']
					PrivateKey = data['keyPair']['PrivateKey']
			elif element == 'certificatePem':
					certificatePem = data['certificatePem']
			elif element == 'certificateId':
					certificateId = data['certificateId']
							
	with open(os.path.join('certificates', '') + thingName + 'public.key', 'w') as outfile:
			outfile.write(PublicKey)
	with open(os.path.join('certificates', '') + thingName + 'private.key', 'w') as outfile:
			outfile.write(PrivateKey)
	with open(os.path.join('certificates', '') + thingName + 'cert.pem', 'w') as outfile:
			outfile.write(certificatePem)

	response = thingClient.attach_policy(
			policyName = defaultPolicyName,
			target = certificateArn
	)
	response = thingClient.attach_thing_principal(
			thingName = thingName,
			principal = certificateArn
	)
	response = thingClient.add_thing_to_thing_group(
		    thingGroupName='Things_group1',
			thingGroupArn='arn:aws:iot:us-west-2:646855605562:thinggroup/Things_group1',
			thingName=thingName,
			thingArn=thingArn
	)



thingClient = boto3.client('iot')

def main(): 
	for i in range(5):
		thingName = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
		createThing(thingName)

if __name__ == '__main__':
	main()
