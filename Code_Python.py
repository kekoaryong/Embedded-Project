import RPi.GPIO as GPIO
import serial
from time import sleep

port = "/dev/ttyACM0"
serialFromArduino = serial.Serial(port, 9600)
GPIO.setmode(GPIO.BOARD)

#####	GPIO.setup(DC Motor_Num, GPIO.OUT)	# Fan  DC Motor
GPIO.setup(11, GPIO.OUT)		# Red LED
GPIO.setup(13, GPIO.OUT)		# Yellow LED
GPIO.setup(15, GPIO.OUT)		# Green LED
GPIO.setup(19, GPIO.IN)		# autoDoor control
GPIO.setup(21, GPIO.IN)		# rolling blind control

Motor1A = 16	#direction
Motor1B = 18	#reverse
Motor1E = 22	#enable

Motor2A = 38	#direction
Motor2B = 40	#reverse
Motor2E = 36	#enable

GPIO.setup(Motor1A, GPIO.OUT)	# Window DC Motor
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

GPIO.setup(Motor2A, GPIO.OUT)	# Blind DC Motor
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

window_flag = 1		# open = 1, closed = 0
blind_flag = 1		# rolled up 1, rolled down = 0


try :
        while True :

                                                        # window control  by using button
                
                if(window_flag == 0 and GPIO.input(19) == True) :	# if press the button when window is open
                        print "open"
                        GPIO.output(Motor1A, GPIO.HIGH)		# value of window open
                        GPIO.output(Motor1B, GPIO.LOW)
                        GPIO.output(Motor1E, GPIO.HIGH)
                        sleep(1.0)
                        window_flag = 1				# flag : window is closed
                        GPIO.output(Motor1E, GPIO.LOW)
                        # wait
                        

                if(window_flag == 1 and GPIO.input(19) == True) :	# if press the button when window is closed
                        print "close"
                        GPIO.output(Motor1A, GPIO.LOW)
                        GPIO.output(Motor1B, GPIO.HIGH)
                        GPIO.output(Motor1E, GPIO.HIGH)
                        sleep(1.0)
                        window_flag = 0				# flag : windows is open
                        GPIO.output(Motor1E, GPIO.LOW)
                        
                
                # dust detection

                dust = serialFromArduino.readline()                
                print(float(dust))
                


                #need to print on LCD (########Not implemented######)
                # variance of LED color followed by dust value

                if(float(dust) >= 70.0) :				# Red LED lights
                        GPIO.output(11, GPIO.HIGH)
                        GPIO.output(13, GPIO.LOW)
                        GPIO.output(15, GPIO.LOW)
                        ####### Fan DC Motor Must be Started######


                        
                if(float(dust) < 30.0) :				# Green LED lights
                        GPIO.output(11, GPIO.LOW)
                        GPIO.output(13, GPIO.LOW)
                        GPIO.output(15, GPIO.HIGH)
                        ####### Fan DC Motor Must be stopped######

                        
                if(float(dust) >= 30.0 and float(dust) < 70.0) :			# Yellow LED lights
                        GPIO.output(11, GPIO.LOW)
                        GPIO.output(13, GPIO.HIGH)
                        GPIO.output(15, GPIO.LOW)
                


                
                if(float(dust) >= 70.0 and window_flag == 1) :		# Door must be closed!
                        print "close"
                        GPIO.output(Motor1A, GPIO.LOW)
                        GPIO.output(Motor1B, GPIO.HIGH)
                        GPIO.output(Motor1E, GPIO.HIGH)
                        sleep(1.0)
                        window_flag = 0
                        GPIO.output(Motor1E, GPIO.LOW)
                        

                
                # Blind control by using auto blind button

                if(blind_flag == 1 and GPIO.input(21) == True) :	
                        print "down"
                        GPIO.output(Motor2A, GPIO.HIGH)		# blind roll down
                        GPIO.output(Motor2B, GPIO.LOW)
                        GPIO.output(Motor2E, GPIO.HIGH)
                        sleep(1.5)
                        blind_flag = 0
                        GPIO.output(Motor2E, GPIO.LOW)
                        

                if(blind_flag == 0 and GPIO.input(21) == True) :
                        print "up"					
                        GPIO.output(Motor2A, GPIO.LOW)		# blind roll up
                        GPIO.output(Motor2B, GPIO.HIGH)
                        GPIO.output(Motor2E, GPIO.HIGH)
                        sleep(1.6)
                        blind_flag = 1
                        GPIO.output(Motor2E, GPIO.LOW)


        
		
except KeyboardInterrupt:
        GPIO.cleanup()
        
finally:
        GPIO.cleanup()
