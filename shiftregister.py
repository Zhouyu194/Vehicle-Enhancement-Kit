import RPi.GPIO as GPIO

SRCLK = 7
RCLK = 8
SER = 10
SRCLR = 12

def initShiftRegister():
	GPIO.setup(SRCLK, GPIO.OUT)
	GPIO.setup(RCLK, GPIO.OUT)
	GPIO.setup(SER, GPIO.OUT)
	GPIO.setup(SRCLR, GPIO.OUT)
	
def transmitData(data):
	for i in range(0,24):
		GPIO.output(SRCLR, GPIO.HIGH)
		GPIO.output(RCLK, GPIO.LOW)
		GPIO.output(SRCLK, GPIO.LOW)
		if (data & 0x800000) != 0:
			GPIO.output(SER, GPIO.HIGH)
		else:
			GPIO.output(SER, GPIO.LOW)
		GPIO.output(SRCLK, GPIO.HIGH)
		data = data << 1
	GPIO.output(RCLK, GPIO.HIGH)
	GPIO.output(SRCLR, GPIO.LOW)
	GPIO.output(SRCLK, GPIO.LOW)
	GPIO.output(SER, GPIO.LOW)
	GPIO.output(RCLK, GPIO.LOW)
