import time
import busio
import board
import digitalio
import math
 
import adafruit_mlx90393
 
I2C_BUS = busio.I2C(board.SCL, board.SDA)
SENSOR = adafruit_mlx90393.MLX90393(I2C_BUS, gain=adafruit_mlx90393.GAIN_1X)
MX, MY, MZ = SENSOR.magnetic 
x = 0
y = 0
z = 0
l1 = []
l2 = []
led = digitalio.DigitalInOut(board.D18)
led.direction = digitalio.Direction.OUTPUT
 
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

led.value = False

def getData():
    MX, MY, MZ = SENSOR.magnetic
    #print("[{}]".format(time.monotonic()))
    print("X: {} uT".format(MX), "Y: {} uT".format(MY),  "Z: {} uT".format(MZ))
    # Display the status field if an error occured, etc.
    if SENSOR.last_status > adafruit_mlx90393.STATUS_OK:
        SENSOR.display_status()
    

def calibration():
    global x, y, z
    MX, MY, MZ = SENSOR.magnetic
    x = MX
    y = MY
    z = MZ
    l1 = [x, y, z]
    print(x, y, z)
    return l1

def buttonPress():
    if not button.value:
        calibration()

def delta(list):
    global dx, dy, dz
    MX, MY, MZ = SENSOR.magnetic
    dx = x - MX
    dy = y - MY
    dz = z - MZ
    print("dX: {} uT".format(dx), "dY: {} uT".format(dy),  "dZ: {} uT".format(dz))
    time.sleep(0.5)
    l2 = [dx, dy, dz]
    return l2

def trip(self):
    v = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2) + math.pow(dz, 2))
    print("v:", v)
    if v > magMath():
        led.value = True

    if v < magMath():
        led.value = False

def magMath():
    global MX
    MX = SENSOR.magnetic
    print(type(MX))
    p = 1/(math.pow(MX, 3))
    print ("p:", p)
    return p


def main():
    while True:
        buttonPress()
        #getData()
        delta(l1)
        trip(l2) 

main()

        