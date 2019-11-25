import arcpy
import os
import re
import sys
import traceback
import collections
import shutil

movdir = r"C:\Scans"
basedir = r"C:\Links"

import os
import shutil
import datetime

now = str(datetime.datetime.now())[:19]
now = now.replace(":","_")

IMAGE_PATH = '/home/pi/WavesLPR/capture1.jpg'
DST_DIR="/home/pi/WavesLPR/captures/capture"+str(now)+".jpg"
shutil.copy(src_dir,dst_dir)