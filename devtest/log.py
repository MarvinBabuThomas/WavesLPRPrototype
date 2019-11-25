import os, glob, shutil, time, datetime

logpath = glob.glob('/home/pi/WavesLPR/log/*')
now  = time.time()
now_str = datetime.datetime.fromtimestamp(now).strftime('%d-%m-%Y %H:%M:%S')

date = time.strftime('%d/%m/%y')
time = time.strftime("%X")
rego = "XYZ8"

for f in logpath:
    if os.stat(f).st_mtime < now - (30 * 86400):
        if os.logpath.isfile(f):
            os.remove(f)
        else:
            shutil.rmtree(f)

with open("../log/log.csv", "a") as logfile:
    logfile.write("%s,%s,%s\n" %(date,time,rego))
    





