import RPi.GPIO as GPIO
import time

def motorIzq(sentido, tiempo=4):
    GPIO.setmode(GPIO.BCM)  
    GPIO.setwarnings(False)
    #Right motor pines
    R_RPWM = 19;  # GPIO pin 19 to the RPWM on the BTS7960 (right controller)
    R_LPWM = 26;  # GPIO pin 26 to the LPWM on the BTS7960 (right controller)
    # For enabling "Left" and "Right" movement 
    R_L_EN = 6;  # connect GPIO pin 6 to L_EN on the BTS7960 (right controller)
    R_R_EN = 13;  # connect GPIO pin 13 to R_EN on the BTS7960 (right controller)

    # Set all of our PINS to output Right
    GPIO.setup(R_RPWM, GPIO.OUT)
    GPIO.setup(R_LPWM, GPIO.OUT)
    GPIO.setup(R_L_EN, GPIO.OUT)
    GPIO.setup(R_R_EN, GPIO.OUT)

    # Enable "Left" and "Right" movement on the HBRidge R
    GPIO.output(R_R_EN, True)
    GPIO.output(R_L_EN, True)

    rpwm= GPIO.PWM(R_RPWM, 500)
    lpwm= GPIO.PWM(R_LPWM, 500)

    if(not sentido): #sentido R
        rpwm.start(0)
        rpwm.ChangeDutyCycle(20)
        time.sleep(tiempo)
    else:#sentido l
        lpwm.start(0)
        lpwm.ChangeDutyCycle(20)
        time.sleep(tiempo)

    GPIO.output(R_RPWM, GPIO.LOW)
    GPIO.output(R_LPWM, GPIO.LOW)
    GPIO.output(R_R_EN, GPIO.LOW)
    GPIO.output(R_L_EN, GPIO.LOW)
    GPIO.cleanup()

def motorDer(sentido, tiempo=4):
    GPIO.setmode(GPIO.BCM)  
    GPIO.setwarnings(False)
    #Left motor pines
    L_RPWM = 20;  # GPIO pin 19 to the RPWM on the BTS7960 (left controller)
    L_LPWM = 21;  # GPIO pin 26 to the LPWM on the BTS7960 (left controller)
    # For enabling "Left" and "Right" movement
    L_L_EN = 12;  # connect GPIO pin 20 to L_EN on the BTS7960 (left controller)
    L_R_EN = 16;  # connect GPIO pin 21 to R_EN on the BTS7960 (left controller)


    # Set all of our PINS to output left
    GPIO.setup(L_RPWM, GPIO.OUT)
    GPIO.setup(L_LPWM, GPIO.OUT)
    GPIO.setup(L_L_EN, GPIO.OUT)
    GPIO.setup(L_R_EN, GPIO.OUT)
    # Enable "Left" and "Right" movement on the HBRidge L
    GPIO.output(L_R_EN, True)
    GPIO.output(L_L_EN, True)
    rpwm= GPIO.PWM(L_RPWM, 500)
    lpwm= GPIO.PWM(L_LPWM, 500)

    if(not sentido): #sentido R
        rpwm.start(0)
        rpwm.ChangeDutyCycle(20)
        time.sleep(tiempo)
    else:#sentido l
        lpwm.start(0)
        lpwm.ChangeDutyCycle(20)
        time.sleep(tiempo)
        
    GPIO.output(L_RPWM, GPIO.LOW)
    GPIO.output(L_LPWM, GPIO.LOW)
    GPIO.output(L_R_EN, GPIO.LOW)
    GPIO.output(L_L_EN, GPIO.LOW)
    GPIO.cleanup()
    
    
if __name__ == '__main__':
	#moverMotorAdelante()
	#GPIO.cleanup()   
	motorDer(False)