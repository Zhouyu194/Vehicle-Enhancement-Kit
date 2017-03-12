import RPi.GPIO as GPIO
import time

class SensorInfo(object):
	def __init__(self, trigPin, echoPin):
		self.trigPin = trigPin
		self.echoPin = echoPin
		GPIO.setup(self.trigPin, GPIO.OUT)
		GPIO.setup(self.echoPin, GPIO.IN)
	
	def measure(self):
		startTime = 0
		endTime = 0
		GPIO.output(self.trigPin, GPIO.HIGH)
		time.sleep(10/1000000.)									#Sleep for 10 us
		GPIO.output(self.trigPin, GPIO.LOW)
		startTime = time.time() * 1000000.						#Get Time in us
		while GPIO.input(self.echoPin) == False:
			if (time.time()*1000000. - startTime) / 58 > 100:	#If wait time is too long
				return 4000.
		while GPIO.input(self.echoPin) == True:
			endTime = time.time()*1000000. 
			if (endTime - startTime) / 58 > 100:				#time til signal / 58 -10 = distance in cm
				return 4000.
		return (endTime - startTime) / 58 - 10
		
