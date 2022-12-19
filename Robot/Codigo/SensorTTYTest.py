from serial import Serial
import time,signal,os
from Caminante import Caminante
from Archivo import getMapESCOM,getFilePosCaminante,saveMap,getPIDFile,deletePIDFile,getUbicFinal,caminanteEnd,getPIDFileGyro,deletePIDFileGyro
import subprocess
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	
def killProcessCaminante(pid):#Funcionando
	try:
		os.kill(pid, signal.SIGKILL) #de sigkill solo diosito se salva xd
		deletePIDFile()
		print("Process Successfully terminated")
	except:
		print("Error Encountered while running script")
		
def killProcessGyro(pid):#Funcionando
	try:
		os.kill(pid, signal.SIGKILL) #de sigkill solo diosito se salva xd
		deletePIDFileGyro()
		print("Process Successfully terminated")
	except:
		print("Error Encountered while running script")

def objetoDetectado(dist, dist_2): #Manejar archivo global, la idea se detecta cuando el bot termina de moverse y va al siguiente paso
	killProcessCaminante(int(getPIDFile()))
	mapESCOM = getMapESCOM()
	robot = getFilePosCaminante()
	print(robot)
	if(dist >= 90 and dist_2 >= 90):
		if(robot.orientacion == "N"):
			mapESCOM[robot.pos_y-1][robot.pos_x] = 0.0
			mapESCOM[robot.pos_y-2][robot.pos_x] = 2.0
			mapESCOM[robot.pos_y-3][robot.pos_x] = 2.0
		elif(robot.orientacion == "E"):
			mapESCOM[robot.pos_y][robot.pos_x+1] = 0.0
			mapESCOM[robot.pos_y][robot.pos_x+2] = 2.0
			mapESCOM[robot.pos_y][robot.pos_x+3] = 2.0
		elif(robot.orientacion == "S"):
			mapESCOM[robot.pos_y+1][robot.pos_x] = 0.0
			mapESCOM[robot.pos_y+2][robot.pos_x] = 2.0
			mapESCOM[robot.pos_y+3][robot.pos_x] = 2.0
		elif(robot.orientacion == "W"):
			mapESCOM[robot.pos_y][robot.pos_x-1] = 0.0
			mapESCOM[robot.pos_y][robot.pos_x-2] = 2.0
			mapESCOM[robot.pos_y][robot.pos_x-3] = 2.0
		print("Casilla vacia, colocar rojo colocar rojo, recalcular" )
	elif(dist >= 60 and dist_2 >= 60):
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
	robotObstaculo = subprocess.Popen(['python3', os.path.join(__location__, "lanzador.py")] + [getUbicFinal(),"1"])

if __name__ == '__main__':
	try:    
		objetoDetect = False
		ser = Serial('/dev/ttyACM0',9600,timeout=1)
		ser.flush()
		tecla = True
		while True:
			if(ser.in_waiting>0):
				line = ser.readline().decode('utf-8').rstrip()
				print(line)
				if('ENTER' in line):
					ser.write(b"a\n")
					time.sleep(1)
				if('cm' in line):
					sensors = line.split('cm')
					print(sensors)
					sensor1 = int(sensors[0].replace('cm',''))
					sensor2 = int(sensors[1].replace('cm',''))
					print(sensor1)   
					print(sensor2)   	        
					if( (sensor1 <= 32 or sensor2 <= 32) and not objetoDetect ): #Objeto encontrado Nos acercamos al objeto
						objetoDetectado(sensor1,sensor2)
						objetoDetect = True
						time.sleep(10)
					if( sensor1 > 40 or sensor2 > 40):
						objetoDetect = False
					if(caminanteEnd()):
						killProcessGyro(int(getPIDFileGyro()))
						break			
	# Reset by pressing CTRL + C
	except KeyboardInterrupt:
		print("Measurement stopped by User")
