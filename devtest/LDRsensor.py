#Following Peripherals needs to be attached
# 1) Infra Red Sensor
# 2) LDR Sensor
# 3) LED
# 4) Speaker

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8,GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    buttonstate = GPIO.input(8)
    time.sleep(0.1)
    if buttonstate == False:
        print ('Car Detected')
    else:
        print ('No Car')

GPIO.cleanup()


