import ephem
import datetime

Braddon = ephem.Observer()
Gunghalin = ephem.Observer()
Phillip = ephem.Observer()

Braddon.lat =  
Braddon.lon = 
Braddon.elevation = 
Braddon.horizon = '-0:34'

Gunghalin.lat = 
Gunghalin.lon = 
Gunghalin.elevation = 
Gunghalin.horizon = '-0:34'

Phillip.lat = 
Phillip.lon = 
Phillip.elevation = 
Phillip.horizon = '-0:34'

if ((now > braddon.previous_rising(ephem.Sun(), use_center=True)) and (now < braddon.next_setting(ephem.Sun(), use_center=True))):
    IsDark = 0
else:
    IsDark = 1

    
