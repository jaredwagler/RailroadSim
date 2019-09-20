#Master function for sending data to esubridge
#Created by: Jared Wagler
#Updated on: 09/20/2019

ESU_PORT = 15471
ESU_RCV_SZ = 1024
   
def esu_send(cmdNum,cmdVal):
	#code to send to esubridge
	if cmdNum == 1: #bell
		if cmdVal == 1:
			print ('Bell is ringing.')
		elif cmdVal == 0:
			print ('Bell is off.')
	if cmdNum == 2: #horn
		if cmdVal == 1:
			print ('Horn is blowing.')
		elif cmdVal == 0:
			print ('Horn is off.')
	if cmdNum == 15: #e-brake
		if cmdVal == 1:
			print ('Train is emergency braking.')
		elif cmdVal == 0:
			print ('Emergency brake not pressed.')
	elif cmdNum == 29: #direction
		if cmdVal == 0:
			print ('Train is going forwards.')
		elif cmdVal == 1:
			print ('Train is going backwards.')
		else:
			print ('Train is idling.')
	return

def throttle_send(throttlePos):
	#code to send to esubridge
	print ('Train is traveling at speed %d.' % (throttlePos))
	return