import time,signal,os
from Archivo import getMapESCOM,getFilePosCaminante,saveMap,getPIDFile,deletePIDFile,getUbicFinal,caminanteEnd
import subprocess
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
#set GPIO Pins
GPIO_TRIGGER = 15
GPIO_ECHO = 14
GPIO_ECHO_2 = 18
GPIO_TRIGGER_2 = 23

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER_2, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_ECHO_2, GPIO.IN)

GPIO.output(GPIO_TRIGGER, False)
GPIO.output(GPIO_TRIGGER_2, False)

def killProcessCaminante(pid):#Funcionando
	try:
		os.kill(pid, signal.SIGKILL) #de sigkill solo diosito se salva xd
		deletePIDFile()
		print("Process Successfully terminated")
	except:
		print("Error Encountered while running script")

def objetoDetectado(dist, dist_2): #Manejar archivo global, la idea se detecta cuando el bot termina de moverse y va al siguiente paso
	killProcessCaminante(int(getPIDFile()))
	mapESCOM = getMapESCOM()
	robot = getFilePosCaminante()
	print(robot)
	if(dist >= 60 and dist_2 >= 60):
		if(robot.orientacion == "N"):
			mapESCOM[robot.pos_y-1][robot.pos_x] = 0.0
			mapESCOM[robot.pos_y-2][robot.pos_x] = 2.0
		elif(robot.orientacion == "E"):
			mapESCOM[robot.pos_y][robot.pos_x+1] = 0.0
			mapESCOM[robot.pos_y][robot.pos_x+2] = 2.0
		elif(robot.orientacion == "S"):
			mapESCOM[robot.pos_y+1][robot.pos_x] = 0.0
			mapESCOM[robot.pos_y+2][robot.pos_x] = 2.0
		elif(robot.orientacion == "W"):
			mapESCOM[robot.pos_y][robot.pos_x-1] = 0.0
			mapESCOM[robot.pos_y][robot.pos_x-2] = 2.0
		print("Casilla vacia, colocar rojo, recalcular" )
	else:
		if(robot.orientacion == "N"):
			mapESCOM[robot.pos_y-1][robot.pos_x] = 2.0
		elif(robot.orientacion == "E"):
			mapESCOM[robot.pos_y][robot.pos_x+1] = 2.0
		elif(robot.orientacion == "S"):
			mapESCOM[robot.pos_y+1][robot.pos_x] = 2.0
		elif(robot.orientacion == "W"):
			mapESCOM[robot.pos_y][robot.pos_x-1] = 2.0
		print("Casilla colocar rojo, recalcular")
	saveMap(mapESCOM)
	robotObstaculo = subprocess.Popen(['python3', os.path.join(__location__, "Pruebas.py")] + [getUbicFinal(),"1"])

def distance():
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)
	# set Trigger after 0.01ms to LOW, sends signal with 1
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	StartTime = time.time()
	StopTime = time.time()

	# save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()
	# save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()

	# time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	distance = (TimeElapsed * 34300 / 2.-1.511372549019610)/0.908687782805430 

	return distance

def distance2():
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER_2, True)
	# set Trigger after 0.01ms to LOW, sends signal with 1
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER_2, False)

	StartTime = time.time()
	StopTime = time.time()

	# save StartTime
	while GPIO.input(GPIO_ECHO_2) == 0:
		StartTime = time.time()
	# save time of arrival
	while GPIO.input(GPIO_ECHO_2) == 1:
		StopTime = time.time()

	# time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	distance = (TimeElapsed * 34300 / 2.-1.511372549019610)/0.908687782805430

	return distance

if __name__ == '__main__':
	try:
		distp = 500
		objetoDetect = False
		while True:
			dist_1 = distance()
			dist_2 = distance2()
			if( (dist_1 <=32 or dist_2 <=32 ) and not objetoDetect ): #Objeto encontrado Nos acercamos al objeto
					objetoDetectado(dist_1,dist_2)
					objetoDetect = True
					time.sleep(10)
			if(dist_1 > 40 or dist_2 > 40 ):
					objetoDetect = False
			if(caminanteEnd()):
					break	
			print ("Measured Distance = %.1f cm" % dist_1)
			print ("Measured Distance = %.1f cm segunso sensor" % dist_2)
			time.sleep(1)
	# Reset by pressing CTRL + C
	except KeyboardInterrupt:
		print("Measurement stopped by User")
		GPIO.cleanup()
