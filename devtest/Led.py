#Following Peripherals needs to be attached
# 1) Infra Red Sensor
# 2) LDR Sensor
# 3) LED
# 4) Speaker

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,GPIO.OUT)

while True:
    GPIO.output(40,GPIO.HIGH)
    print('LED ON')
    time.sleep(1)
    GPIO.output(40,GPIO.LOW)
    print('LED OFF')
    time.sleep(1)

GPIO.cleanup()


