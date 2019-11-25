from bluedot import BlueDot

bd=BlueDot()

def say_PRESSED():
    print("You pressed the Blue dot!")


while True:
    bd.when_pressed = say_PRESSED

