#Master function for sending data to esubridge
#Created by: Jared Wagler
#Updated on: 09/17/2019

ESU_PORT = 15471
ESU_RCV_SZ = 1024
   
def esu_send(cmdNum, throttlePos = 128):
	#code to send to esubridge
	if throttlePos < 127:
		#code for sending throttle speed
	else:
		#code for all other commands