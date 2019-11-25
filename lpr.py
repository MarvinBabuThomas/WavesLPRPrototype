#Developed for : Waves Car Wash
#Developed by  : Marvin Babu Thomas
#Copyrights    : Copyright 1992-2019 FreeBSD 
#Last Updated  : 17-Aug-2019

#General Libraries
import RPi.GPIO as gp
import os, glob, shutil, time, datetime, subprocess

#Libraries for Integration with Camera 
from CameraLED import CameraLED

#Libraries for Integration with OpenALPR
import requests, base64, json

#Libraries for Integration with Imagatec 
import urllib.request

#Libraies for Integration with Android App
from bluedot import BlueDot
from signal import pause


#Configuration ParamVerwaltungeters
logMode = True                                                #Flag to log text
CaptureLogMode = True                                         #Flag to log text
ProximityPin = 8                                              #Board Pin Assigned for Proximity Sensor                       
RedPin = 36                                                   #Board Pin Assigned for Red LED
BluePin = 40                                                  #Board Pin Assigned for Blue LED
IsDark = 0                                                    #Flag for Darkness; 0 - Not Dark, 1 - Is Dark
GeoLocation = 2                                               #Enum for Wash Site  0 - Braddon, 1 - Gungahlin, 2 - Phillip
IMAGE_PATH = '/home/pi/WavesLPR/capture1.jpg'                 #Path of Current Captured Image
LOG_PATH = glob.glob('/home/pi/WavesLPR/log/*')               #Path of Captured Image Logs
SECRET_KEY = 'sk_45936eee41497f9fa775b746'                    #Secret Key for OpenALPR Cloud API Integration
PPUrlBraddon   = "http://59.167.251.106"                      #Static IP Url for Waves Car Wash Braddon
PPUrlGunghalin = "http://203.173.10.173"                      #Static IP Url for Waves Car Wash Gunghalin
#PPUrlPhillip   = "http://203.173.10.173"                     #Static IP Url for Waves Car Wash Phillip
count = 0
KillFlag = False

#Instantiations
DayVision = CameraLED()                              #Instantiate Camera Motor Object
bd = BlueDot()                                         #Instantiate Bluetooth Connection Object 
#General IO Settings
gp.setwarnings(False)                                  #Suppress all warnings from GPIO
gp.setmode(gp.BOARD)                                   #Choosing the GPIO Mode
gp.setup(ProximityPin, gp.IN, pull_up_down=gp.PUD_UP)  #Pulling Up the GPIO pin to compensate for 5v - 3.3V
gp.setup(RedPin,gp.OUT)                                #Pin for Red LED
gp.setup(BluePin,gp.OUT)                               #Pin for Blue LED    

#Time Parameters
now  = time.time()
now_str = datetime.datetime.fromtimestamp(now).strftime('%d-%m-%Y %H:%M:%S')
date = time.strftime('%d-%m-%y')
timet = time.strftime("%X")
nowTime = datetime.datetime.now()
SunRiseTime = nowTime.replace(hour=6, minute=0, second=0, microsecond=0)
SunSetTime = nowTime.replace(hour=18, minute=0, second=0, microsecond=0)

def main():
    gp.output(RedPin,gp.HIGH)
    try:
        while True:
            time.sleep(1)
            bd.when_rotated = killer
            if (KillFlag == True):
                exit("Killed by BlueDot")
            CarDetected = (gp.input(ProximityPin)==False)
            if (CarDetected):
                #Notify Car Detected
                print (" ")
                print ("Car Detected!")
                print (" ")
                BlueDotRotation
                #Capture Number Plate Photo
                if((nowTime < SunRiseTime) and (nowTime > SunSetTime)):
                    DayVision.off() # Enable Night Vision
                    print("Night Vision Mode")
                    print(" ")
                    gp.output(BluePin,gp.HIGH)
                    time.sleep(1)
                    gp.output(BluePin,gp.LOW)
                    capture(1)
                else:
                    DayVision.on()  # Enable Daily Vision
                    print("Day Vision Mode")
                    print(" ")
                    gp.output(BluePin,gp.HIGH)
                    time.sleep(1)
                    gp.output(BluePin,gp.LOW)
                    capture(1)
                                
                #Send Image to server and Receive Rego
                rego = processImage()
                    
                #Send Rego to POS
                if(rego==0):
                    print('No Number Plate found in Camera frame!')
                    print(' ')
                    print ('RED LED is Flashing!')
                    print(' ')
                    gp.output(RedPin,gp.LOW)
                    time.sleep(0.16)
                    gp.output(RedPin,gp.HIGH)
                    time.sleep(0.67)
                    gp.output(RedPin,gp.LOW)
                    time.sleep(0.16)
                    gp.output(RedPin,gp.HIGH)
                else:
                    print ('Car LPR Successful!')
                    print(' ')
                    print ('BLUE LED is Flashing!')
                    gp.output(BluePin,gp.HIGH)
                    time.sleep(0.67)
                    gp.output(BluePin,gp.LOW)
                    time.sleep(0.16)
                    gp.output(BluePin,gp.HIGH)
                    time.sleep(0.67)
                    gp.output(BluePin,gp.LOW)
                    
                    print(' ')
                    print('REGO : %s' %(rego))
                    print(' ')
                    print('Message from IPOS Server:')
                    
                    if (GeoLocation==0):
                        x = urllib.request.urlopen('http://59.167.251.106/lpr/lpr.asp?rego="+rego')
                        print(x.read())
                        print(' ')
                    elif (GeoLocation==1):
                        y = urllib.request.urlopen('http://203.173.10.173/lpr/lpr.asp?rego="+rego')
                        print(y.read())
                        print(' ')
                    elif (GeoLocation==2):
                        z = urllib.request.urlopen('http://accept.waves.iposmaster.com/lpr/lpr.asp?rego="+rego')
                        print(z.read())
                        print(' ')
                    else:
                        print("Not on WAVES Site!")
                    
                    if (logMode==True):
                        for f in LOG_PATH:
                            if os.stat(f).st_mtime < now - (30 * 86400):
                                if os.LOG_PATH.isfile(f):
                                    os.remove(f)
                                else:
                                    shutil.rmtree(f)
                        
                        if (CaptureLogMode == True):
                            IMAGE_LOG_PATH = "/home/pi/WavesLPR/log/capture_%s_%s_%s.jpg" %(date,timet,rego)  
                            shutil.copy(IMAGE_PATH,IMAGE_LOG_PATH)
                        
                        with open("./log/log.csv", "a") as logfile:
                            logfile.write("%s,%s,%s,capture_%s_%s_%s.jpg\n" %(date,timet,rego,date,timet,rego))
      
      
                #Stay here until Car Moves away
                while (CarDetected):
                    time.sleep(1)
                    CarDetected = (gp.input(ProximityPin)==False)
                    bd.when_rotated = killer
                    if (KillFlag == True):
                        exit("Killed by BlueDot")
                    if (bd.is_pressed == True):
                        print ('Recapture Intiated!')
                        break
                    print('Waiting for Boom Gate...')
                
                print(' ')
            
            else:
                print ("No CAR ...")
                
    finally:
        gp.cleanup()
        
    DayVision.on()  # Enable Daily Vision


def capture(cam):
    cmd = "raspistill -o capture%d.jpg" % cam
    os.system(cmd)

def killer(rotation):
    global count, KillFlag
    count += rotation.value
    if (count > 3):
        bd.color = "Red"
        KillFlag = True
        #Batcmd = "ps aux | grep /home/pi/WavesLPR/lpr.py |head -1| awk '{print $2}'"
        #processNum = subprocess.check_output(Batcmd,shell=True)
        #print(processNum.strip())
        #os.system('sudo kill %s' %(processNum.strip()))
        
def processImage():
    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64= base64.b64encode(image_file.read())
    #url = 'https://api.openalpr.com/v2/recognize_bytes?cl=1&country=au&topn=1&recognize_vehicle=1&secret_key=%s' % (SECRET_KEY)
    url = 'https://api.openalpr.com/v2/recognize_bytes?cl=1&country=au&topn=1&secret_key=%s' % (SECRET_KEY)
    plateDetailsJSON = requests.post(url,data = img_base64)
    plateDetailsPY = json.loads(json.dumps(plateDetailsJSON.json(), indent=2)) 
    
    #print('REGO                 : '+str(plateDetailsPY["results"][0]["plate"]))
    #print('REGO Confidence      : '+str(plateDetailsPY["results"][0]["confidence"]))
    #print('Region               : '+str(plateDetailsPY["results"][0]["region"]))
    #print('Region Confidence    : '+str(plateDetailsPY["results"][0]["region_confidence"]))
    #print('Processing Time (ms) : '+str(plateDetailsPY["results"][0]["processing_time_ms"]))
    #print('Body Type            : '+str(plateDetailsPY["results"][0]["vehicle"]["body_type"][0]["name"]))
    #print('Color                : '+str(plateDetailsPY["results"][0]["vehicle"]["color"][0]["name"]))
    #print('Year                 : '+str(plateDetailsPY["results"][0]["vehicle"]["year"][0]["name"]))
    #print('Make                 : '+str(plateDetailsPY["results"][0]["vehicle"]["make"][0]["name"]))
    #print('Model                : '+str(plateDetailsPY["results"][0]["vehicle"]["make_model"][0]["name"]))
    
    try:
        pass
        return plateDetailsPY["results"][0]["plate"]
    except IndexError:
        return 0

if __name__ == "__main__":
    DayVision.on()
    main()
      