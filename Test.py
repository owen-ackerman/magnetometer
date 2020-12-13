import time
import busio
import board
import digitalio
 
import adafruit_mlx90393
 
I2C_BUS = busio.I2C(board.SCL, board.SDA)
SENSOR = adafruit_mlx90393.MLX90393(I2C_BUS, gain=adafruit_mlx90393.GAIN_1X)
MX, MY, MZ = SENSOR.magnetic 
x = 0
y = 0
z = 0
l = []
led = digitalio.DigitalInOut(board.D18)
led.direction = digitalio.Direction.OUTPUT
 
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


def getData():
    #MX, MY, MZ = SENSOR.magnetic
    #print("[{}]".format(time.monotonic()))
    #print("X: {} uT".format(MX), "Y: {} uT".format(MY),  "Z: {} uT".format(MZ))
    # Display the status field if an error occured, etc.
    if SENSOR.last_status > adafruit_mlx90393.STATUS_OK:
        SENSOR.display_status()
    

def calibration():
    global x, y, z
    MX, MY, MZ = SENSOR.magnetic
    x = MX
    y = MY
    z = MZ
    l = [x, y, z]
    led.value = not button.value
    print(x, y, z)
    return l

def buttonPress():
    if not button.value:
        calibration()

def delta(list):
    MX, MY, MZ = SENSOR.magnetic
    dx = x - MX
    dy = y - MY
    dz = z - MZ
    print("dX: {} uT".format(dx), "dY: {} uT".format(dy),  "dZ: {} uT".format(dz))

def main():
    while True:
        buttonPress()
        delta(l)

main()

        