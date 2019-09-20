#Master function for sending data to esubridge
#Created by: Jared Wagler
#Updated on: 09/20/2019

ESU_PORT = 15471
ESU_RCV_SZ = 1024
   
def esu_send(cmdNum,cmdVal):
	#code to send to esubridge
	if cmdNum == 29: #direction
		if cmdVal == 0:
			print ('Train is going forwards.')
		elif cmdVal == 1:
			print ('Train is going backwards.')
		else:
			print ('Train is idling.')

	return

def throttle_send(throttlePos)
	#code to send to esubridge
	print ('Train is traveling at speed %d.' % (throttlePos))
	return