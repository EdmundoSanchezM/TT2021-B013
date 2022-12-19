import RPi.GPIO as GPIO
import time

SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500
Servo = 24


GPIO.setmode(GPIO.BCM)       
GPIO.setup(Servo, GPIO.OUT)  
GPIO.output(Servo, GPIO.LOW) 
p = GPIO.PWM(Servo, 50)     
p.start(0)                    


def map(value, inMin, inMax, outMin, outMax):
    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin
                   

def setAngle(angle):      
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)
    
def turningSense(x):
    if(x):
        for i in range(0, 90, 5):   
            setAngle(i)    
            time.sleep(0.002)
        time.sleep(1)
    else:
        for i in range(90, -1, -5): 
            setAngle(i)
            time.sleep(0.001)
        time.sleep(1)
        
def destroy():
    p.stop()
    GPIO.cleanup()

try:
    turningSense(1)#0 cerrar 1 abrir
    destroy()
except KeyboardInterrupt:
    destroy()


