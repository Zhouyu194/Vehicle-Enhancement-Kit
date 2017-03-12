import RPi.GPIO as GPIO
import os
import pygame
import pygame.camera
import time
import sys
import shiftregister
from sensorinfo import SensorInfo
from statemachine import StateMachine
from FMTransmitter import FMTransmitter

period = 1000
tasks = []
Sensors = []
sensorMeasurements = [0] * 8
#Sensor Layout
# 0 1 2
# 6   7
# 5 4 3

#Control Variables
sensorsEnable = False
cameraEnable = False
count = 0

#Installs BCM Camera Module if not already installed
if not os.path.exists('/dev/video0'):
	os.system('sudo modprobe bcm2835-v4l2')

#Camera Variables
pygame.init()
pygame.mouse.set_visible(True)
#make The Cursor Transparent
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
lcd = pygame.display.set_mode((800,480))
lcd.fill((0,0,0))
pygame.display.toggle_fullscreen()
pygame.camera.init()
camera = pygame.camera.Camera('/dev/video0', (800,480), 'RGB')
camera.start()
surf = pygame.Surface((800,480))
font = pygame.font.Font(None, 30)
rectcolor = (255,255,255)

#FM Transmitter Variables
radio = FMTransmitter()
#Set Default Frequency
radio.set_freq(87.5) 
frequency = 87.5
radio.set_gain(0)
gain = 0
radio.set_mute(0)
muted = 0

#Control Finite State Machine
def ControlTickFunction(statemachine):
	global cameraEnable
	global sensorsEnable
	global muted
	buttons = pygame.mouse.get_pressed()
	#Transitions
	if statemachine.state == "init_state":
		statemachine.state = "disabled_state"
	elif statemachine.state == "disabled_state":
		if buttons[0]:
			position = pygame.mouse.get_pos()
			if position[0] < 100 and position[1] < 50:
				statemachine.state = "disabled_to_enabled_wait"
			elif position[0] > 750 and position[1] < 50:
				pygame.display.toggle_fullscreen()
				pygame.mouse.set_pos((800/2,480/2))
			elif position[0] > 325 and position[0] < 365 and position[1] > 290 and position[1] < 340:
				statemachine.state = "frequency_down_wait"
			elif position[0] > 435 and position [0] < 475 and position[1] > 290 and position[1] < 340:
				statemachine.state = "frequency_up_wait"
			elif position[0] > 325 and position[0] < 365 and position[1] > 240 and position[1] < 290:
				statemachine.state = "volume_down_wait"
			elif position[0] > 435 and position[0] < 475 and position[1] > 240 and position[1] < 290:
				statemachine.state = "volume_up_wait"
	elif statemachine.state == "disabled_to_enabled_wait":
		if not buttons[0]:
			statemachine.state = "enabled_state"
	elif statemachine.state == "enabled_state":
		if buttons[0]:
			position = pygame.mouse.get_pos()
			if position[0] < 100 and position[1] < 50:
				statemachine.state = "enabled_to_disabled_wait"
			elif position[0] > 750 and position[1] < 50:
				pygame.display.toggle_fullscreen()
				pygame.mouse.set_pos((800/2,480/2))
	elif statemachine.state == "enabled_to_disabled_wait":
		if not buttons[0]:
			statemachine.state = "disabled_state"
	elif statemachine.state == "frequency_down_wait":
		if not buttons[0]:
			if radio.read_freq() <= 87.5:
				radio.set_freq(107.9)
			else:
				radio.set_freq(float("{0:.1f}".format(radio.read_freq() - 0.2)))
				#Using {0:.1f} to ensure the frequency only has prescion up to 1 dec point
			global frequency
			frequency = radio.read_freq()			
			statemachine.state = "disabled_state"
	elif statemachine.state == "frequency_up_wait":
		if not buttons[0]:
			if radio.read_freq() >= 107.9:
				radio.set_freq(87.5)
			else:
				radio.set_freq(float("{0:.1f}".format(radio.read_freq() + 0.2)))
			global frequency
			frequency = radio.read_freq()
			statemachine.state = "disabled_state"	
	elif statemachine.state == "volume_down_wait":
		gainInstance = radio.read_gain()
		if not buttons[0]:
			if (gainInstance - 1) <= -12:
				radio.set_mute(1)
				muted = 1
				global gain
				gain = -12
			else:
				radio.set_gain(gainInstance - 1)
				global gain
				gain = gainInstance - 1
		statemachine.state = "disabled_state"
	elif statemachine.state == "volume_up_wait":
		gainInstance = radio.read_gain()
		if not buttons[0]:
			if muted:
				radio.set_mute(0)
			if gainInstance >= 12:
				pass
			elif gainInstance + 1 <= 12:
				radio.set_gain(gainInstance + 1)	
			global gain
			gain = gainInstance + 1
			statemachine.state = "disabled_state"
		
	# elif statemachine.state == "disabled_state":
		# buttons = pygame.mouse.get_pressed()
		# if buttons[0]:
			# position = pygame.mouse.get_pos()
			# if position[0] < 100 and position[1] < 50:
				# statemachine.state = "enabled_state"
			# elif position[0] > 750 and position[1] < 50:
				# pygame.display.toggle_fullscreen()
				# pygame.mouse.set_pos((800/2,480/2))
			
	# elif statemachine.state == "enabled_state":
		# buttons = pygame.mouse.get_pressed()
		# if buttons[0]:
			# position = pygame.mouse.get_pos()
			# if position[0] < 100 and position[1] < 50:
				# statemachine.state = "disabled_state"	
			# elif position[0] > 750 and position[1] < 50:
				# pygame.display.toggle_fullscreen()
				# pygame.mouse.set_pos((800/2,480/2))

	else:
		statemachine.state = "init_state"
	
	#Outputs
	if statemachine.state == "init_state":
		pass
	elif statemachine.state == "disabled_state":
		cameraEnable = False
		sensorsEnable = False
	elif statemachine.state == "enabled_state":
		cameraEnable = True
		sensorsEnable = True
	else:
		pass

#Display Finite State Machine
def DisplayTickFunction(statemachine):
	#Transitions
	if statemachine.state == "init_state":
		statemachine.state = "disabled_state"
	elif statemachine.state == "disabled_state":
		if cameraEnable:
			statemachine.state = "enabled_state"
	elif statemachine.state == "enabled_state":
		if not cameraEnable:
			statemachine.state = "disabled_state"
	else:
		statemachine.state = "init_state"
		
	#Outputs
	if statemachine.state == "init_state":
		pass
	elif statemachine.state == "disabled_state":
		global frequency
		global gain
		lcd.fill((0,0,0))
		pygame.draw.rect(lcd, rectcolor, (0,0,100,50))
		text_surface = font.render('enable', True, (0,0,0))
		lcd.blit(text_surface, (15,15))
		pygame.draw.rect(lcd, rectcolor, (325, 290 ,150, 50))
		text_surface = font.render("  -     " + str(frequency) + "     +" , True, (0,0,0))
		lcd.blit(text_surface, (330,300))
		pygame.draw.rect(lcd, rectcolor, (325, 240 ,150, 50))
		text_surface = font.render("  -     " + str(ConvertGainToPercent(gain)) + "%     +" , True, (0,0,0))
		lcd.blit(text_surface, (330,250))		
		pygame.display.update()
	elif statemachine.state == "enabled_state":
		lcd.fill((0,0,0))
		camera.get_image(surf)
		lcd.blit(surf, (0,0))
		pygame.draw.rect(lcd,rectcolor,(0,0,100,50))
		text_surface = font.render('disable', True, (0,0,0))
		lcd.blit(text_surface, (15,15))
		pygame.display.update()
	else:
		pass

#Sensor Control Finite State Machine
def SensorTickFunction(statemachine):
	#Transitions
	if statemachine.state == "init_state":
		Sensors.append(SensorInfo(11,13))
		Sensors.append(SensorInfo(15,16))
		Sensors.append(SensorInfo(19,21))
		Sensors.append(SensorInfo(23,24))
		Sensors.append(SensorInfo(29,31))
		Sensors.append(SensorInfo(32,33))
		Sensors.append(SensorInfo(36,37))
		Sensors.append(SensorInfo(38,40))
		statemachine.state = "disabled_state"
	elif statemachine.state == "disabled_state":
		if sensorsEnable:
			statemachine.state = "enabled_state"
		else:
			statemachine.state = "disabled_state"
	elif statemachine.state == "enabled_state":
		if sensorsEnable:
			pass
		else:
			statemachine.state = "disabled_state"
	else:
		statemachine.state == "init_state"

	#Outputs
	if statemachine.state == "init_state":
		pass
	elif statemachine.state == "disabled_state":
		#In Disabled State Sensors 6 and 7 should still be functional
		#Since they are Blind Spot Sensors
		for i in range(0,6):
			sensorMeasurements[i] = 0
		for i in range(6,8):
			sensorMeasurements[i] = Sensors[i].measure()
	elif statemachine.state == "enabled_state":
		for i in range(0,8):
			sensorMeasurements[i] = Sensors[i].measure()
		
#LED Matrix Finite State Machine
def LedMatrixTickFunction(statemachine):
	#Transitions
	if statemachine.state == "init_state":
		shiftregister.initShiftRegister()
		statemachine.state = "ledMatrixDisabled"
	elif statemachine.state == "ledMatrixDisabled":
		if sensorsEnable:
			statemachine.state = "ledMatrixEnabled"
		else:
			statemachine.state = "ledMatrixDisabled"
	elif statemachine.state == "ledMatrixEnabled":
		if sensorsEnable:
			statemachine.state = "ledMatrixEnabled"
		else:
			statemachine.state = "ledMatrixDisabled"
	else:
		statemachine.state = "init_state"
		
	#Outputs
	if statemachine.state == "init_state":
		pass
	elif statemachine.state == "ledMatrixDisabled":
		data = 0
		if sensorMeasurements[6] < 5:		#Left Blindspot Sensor
			data |= 0x40000
		if sensorMeasurements[7] < 5:		#Right Blindspot Sensor
			data |= 0x80000
		shiftregister.transmitData(data)
		
	elif statemachine.state == "ledMatrixEnabled":
		data = 0
		for i in range(0,6):
			if (sensorMeasurements[i] <= 20 and sensorMeasurements[i] > 15):
				data |= 0x1 << (3*i)
			elif (sensorMeasurements[i]  <= 15 and sensorMeasurements[i] > 10):
				data |= 0x3 << (3*i)
			elif (sensorMeasurements[i] <= 10):
				data |= 0x7 << (3*i)
		
		#print "Left Blind Spot Sensor Distance: %f\n Right Blind Spot Sensor Distance: %f" % (sensorMeasurements[6], sensorMeasurements[7])
		if sensorMeasurements[6] < 5:		#Left Blindspot Sensor
			data |= 0x40000
		if sensorMeasurements[7] < 5:		#Right Blindspot Sensor
			data |= 0x80000
		shiftregister.transmitData(data)
	
def ConvertGainToPercent(gain):
	return int((gain + 12) / 24. * 100)
		

def TimerISR():
	for i in range (0, len(tasks)):
		if tasks[i].elapsedTime >= tasks[i].period:
			tasks[i].TickFunction(tasks[i])
			tasks[i].elapsedTime = 0
		else:
			tasks[i].elapsedTime += period

if __name__ == "__main__":
	GPIO.setmode(GPIO.BOARD)
	shiftregister.initShiftRegister()
	period = 10
	tasks.append(StateMachine(10, ControlTickFunction))
	tasks.append(StateMachine(10, DisplayTickFunction))
	tasks.append(StateMachine(50, SensorTickFunction))
	tasks.append(StateMachine(50, LedMatrixTickFunction))
	try:
		while True:
			TimerISR()
			time.sleep(period/1000.)
			event = pygame.event.poll()
			
			# buttons = pygame.mouse.get_pressed()
			# if buttons[0]:
				# print pygame.mouse.get_pos()
			
			#if event == pygame.MOUSEBUTTONDOWN:
			#	position = pygame.mouse.get_pos()
			#	print "x: %d y: %y" % (position[0], position[1])
				
			#mouse = pygame.mouse.get_pressed()
			#print(mouse)
	except KeyboardInterrupt:
		shiftregister.transmitData(0)
		GPIO.cleanup()
