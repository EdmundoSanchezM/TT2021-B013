from main import lanzadorR
import sys
import subprocess
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
sudo_password = '*******'
cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
iniciarSensores = subprocess.Popen(['sudo','-S','python3', os.path.join(__location__, "SensorTTYTest.py")], stdin=cmd1.stdout, stdout=subprocess.PIPE)
iniciarGiroscopio = subprocess.Popen(['sudo','-S','python3', os.path.join(__location__, "GiroscopioTTY.py")], stdin=cmd1.stdout, stdout=subprocess.PIPE)
print('cmd entry:', sys.argv)
lanzadorR("Robot", str(sys.argv[1]), int(sys.argv[2]))#Inicio,final,tipo
