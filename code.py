# Write your code here :-)
from math import atan2, sqrt
import time
from adafruit_lsm6ds import lsm6dsox
import board
import neopixel
import random
import busio
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
max = 7
q = [0]*max
d = [0]*max
wait = 0
state = 1
t = 0
p = 0
j = 0

#initate LED parameters
numled = 186
rings = [8, 12, 16, 20, 24, 24, 24, 20, 16, 12, 8, 1]

ledarray = [0]*(numled*3)
offset = 20

led = neopixel.NeoPixel(board.D9,numled,auto_write = False, pixel_order = neopixel.GRBW)

#Led colors
maxbright = 30
red = (maxbright,0,0,0)
orange = (maxbright, maxbright/2.8,0,0)
green = (0,maxbright,0,0)
blue = (0,0,maxbright,0)
white = (0,0,0,maxbright)
off = (0,0,0,0)

#initate IMU
i2c = busio.I2C(board.SCL, board.SDA)
imu = LSM6DSOX(i2c)
#LSM6DSOX._set_gyro_range(imu, )
imu.gyro_range = 2
imu.accelerometer_range = 2
imu.accelerometer_data_rate = 8
imu.gyro_data_rate = 8
#set adresses
temp = 0
for a in range(0,numled):
    ledarray[temp] = a 
    temp = temp+3

#set theta around the y axis
temp = 1
for b in range(0,12):
    w = rings[b]
    x = float(360.0/w)
    for t in range(1,(w+1)):
        ledarray[temp] = (x*t)
        temp = temp+3

#set phi
temp = 2
for a in range(0,12):
    for t in range(0,rings[a]):
        ledarray[temp] = 15*a
        temp = temp + 3

'''#print coridate array
for i in range(0,(numled*3),3):
    t = i+3
    print(str(ledarray[i]) + ", " + str(ledarray[i+1]) + ", " + str(ledarray[i+2]))'''


while(True):
    gyro = imu.gyro
    

    if(wait >= 20):
        if(gyro[0] <= -15.0):
            state += 1
            wait = 0
            if(state > 6):
                state = 1
    else:
        wait += 1

    if(state == 1):
        led.fill(white)
        led.show()

    if (t > 360):
        t = 0

    #check IMU values
    if(state == 6):
        accel = imu.acceleration
        theta = (57.295*atan2(accel[0],accel[1]))+180
        phi = (57.295*atan2(sqrt((accel[2]**2)+(accel[1]**2)),accel[0]))
        gyro = imu.gyro
        #print(theta)
        #print(phi)
        print("Acceleration: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} m/s^2".format(*accel))
        print("Gyro          X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} rad/s".format(*gyro))
        for w in range(1,numled*3,3):
            checktheta = ledarray[w]
            checkphi = ledarray[w+1]
            x = ledarray[w-1]
            if( checktheta >= theta-offset and checktheta <= theta+offset and checkphi >= phi-offset and checkphi <= phi+offset):
                led[x] = white

            else:
                led[x] = off

        led.show()

    '''#set all leds to white
    led.fill(white)
    led.show()
    time.sleep(2)
    #print(ledarray)'''

    #roating green and orange
    if(state == 2):
        t += 15
        for w in range(1,numled*3,3):
            checktheta = ledarray[w]
            checkphi = ledarray[w+1]
            x = ledarray[w-1]
            if( checktheta >= t-offset and checktheta <= t+offset):
                led[x] = orange
                
            elif( checktheta >= t+180-offset and checktheta <= t+180+offset):
                led[x] = green
                
            elif(checktheta >= t+360-offset or checktheta <= t-360+offset):
                led[x] = orange

            elif(checktheta >= t-180-offset and checktheta <= t-180+offset):
                led[x] = green

            else:
                led[x] = off
        led.show()

    if(state == 3):
        t += 15
        for w in range(1,numled*3,3):
            checktheta = ledarray[w]
            checkphi = ledarray[w+1]
            x = ledarray[w-1]
            if( checktheta >= t-offset and checktheta <= t+offset):
                led[x] = white
    
                
            elif(checktheta >= t+360-offset or checktheta <= t-360+offset):
                led[x] = white


            else:
                led[x] = off
        led.show()

    #firework
    '''maxbright = 10
    for t in range(0,180,15):
        for w in range(2,numled*3, 3):
            checkphi = ledarray[w]
            x = ledarray[w-2]
            if( checkphi >= t-offset and checkphi <= t+offset):
                led[x] = white
            else: 
                led[x] = off
        led.show()
    
    time.sleep(3)
    maxbright = 255
    led.fill(white)
    led.show()
    time.sleep(0.05)
    led.fill(off)
    led.show()
    randtheta = [0]*max
    needtheta = [0]*max
    maxbright = 10



    for phi in reversed(range(0, 180, 20)):
        for i in range(0,max):
            randtheta[i] = random.randint(0,360)

        for w in range(1,numled*3, 3):
            for q in range(0,max):
                theta = randtheta[q]
                checktheta = ledarray[w]
                checkphi = ledarray[w+1]
                x = ledarray[w-1]
                if(checktheta >= theta-offset and checktheta <= theta+offset and checkphi >= phi-offset-20 and checkphi <= phi+offset+20):
                    needtheta[q] = x
        #print(needtheta) 

           
        for w in range(0, numled):
            if w in needtheta:
                led[w] = white
            else:
                led[w] = off
        led.show()
    
    time.sleep(0.1)
    led.fill(off)
    led.show()
    time.sleep(5)'''
 



    #random flashing
    if state == 4:
        d = q
        for i in range(0,max):
            q[i] = random.randint(0,numled-1)

        for i in range(0,max):
            led[q[i]] = white
            #led[d[i]] = off
        led.show()
        #print(q)
        #print(d)
        time.sleep(0.04)
        for i in range(0,max):
            #led[q[i]] = white
            led[d[i]] = off


    if state == 5:
        if(j == 0):
            p += 10
            if p >= 180:
                j = 1
        elif(j == 1):
            p -= 10
            if p <= 0:
                j = 0
        for w in range(1,numled*3,3):
            checkphi = ledarray[w+1]
            x = ledarray[w-1]
            if( checkphi >= p-offset and checkphi <= p+offset):
                led[x] = white

            else:
                led[x] = off
        led.show()

 
    #pixels[0] = red
    #pixels.show()
    #time.sleep(0.5)
    #pixels[0] = blue
    #pixels.show()
    #time.sleep(0.5)
    #pixels[0] = green
    #pixels.show()
    #time.sleep(0.5)
    #pixels[0] = white
    #pixels.show()
    #time.sleep(0.5) 
    #pixels[0] = off
    #pixels.show()
    #time.sleep(0.5)
