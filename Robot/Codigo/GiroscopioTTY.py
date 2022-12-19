from serial import Serial
import time
import os
from Archivo import setPIDFileGyro
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def getPID():
	pid = os.getpid()
	print("PID main", pid)
	return pid
	
if __name__ == '__main__':
	setPIDFileGyro(getPID())
	ser = Serial('/dev/ttyUSB0',9600,timeout=1)
	ser.flush()
	tecla = True
	while True:
		if(ser.in_waiting>0):
			line = ser.readline().decode('utf-8').rstrip()
			lineArray = line.split(',   ')
			print(lineArray)
			if(len(lineArray)>0):
				if('ENTER' in lineArray[0]):
					ser.write(b"a\n")
					time.sleep(1)
				if('Failed' not in lineArray[0]):
					if('Yaw' in lineArray[0]):
						yawValueS = lineArray[0].replace('Yaw','')
						yawValue = float(yawValueS.replace(' ',''))
						print(type(yawValue))
						if(-60 < yawValue and yawValue < 60):
							if(yawValue>2.2):
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("N\n"+str(yawValue))
							elif(yawValue<-0):
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("N\n"+str(yawValue))
							else:
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("Ok\ncomplemento")
						elif(yawValue <-70 and yawValue > -120):
							yawValue = yawValue + 90
							if(yawValue>1.8):
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("W\n"+str(yawValue))
							elif(yawValue<-0):
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("W\n"+str(yawValue))
							else:
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("Ok\ncomplemento")
						elif( 70 < yawValue and yawValue < 120):
							yawValue = yawValue - 90
							if(yawValue>1.8):
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("E\n"+str(yawValue))
							elif(yawValue<-0):
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("E\n"+str(yawValue))
							else:
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("Ok\ncomplemento")
						elif(yawValue<180 and yawValue > 160):
							yawValue = (yawValue - 175)
							if(yawValue>1.8):
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("SP\n"+str(yawValue))
							elif(yawValue<-0):
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("SP\n"+str(yawValue))
							else:
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("Ok\ncomplemento")
						elif(yawValue<-250 and yawValue > -270):
							yawValue = (yawValue + 265)
							if(yawValue>1.8):
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("SN\n"+str(yawValue))
							elif(yawValue<-0):
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("SN\n"+str(yawValue))
							else:
								with open(os.path.join(__location__, 'GyroYawdata.txt'), 'w') as f:
									f.write("Ok\ncomplemento")
						print(yawValue)	
