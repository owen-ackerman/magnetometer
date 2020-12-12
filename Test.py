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
led = digitalio.DigitalInOut(board.D18)
led.direction = digitalio.Direction.OUTPUT
 
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


def getData():
    MX, MY, MZ = SENSOR.magnetic
    #print("[{}]".format(time.monotonic()))
    #print("X: {} uT".format(MX), "Y: {} uT".format(MY),  "Z: {} uT".format(MZ))
    MX, MY, MZ
    # Display the status field if an error occured, etc.
    if SENSOR.last_status > adafruit_mlx90393.STATUS_OK:
        SENSOR.display_status()
    

def calibration():
    global x, y, z
    x = MX
    y = MY
    z = MZ
    #led.value = button.value
    print(x, y, z)
    return x, y, z

def buttonPress():
    if not button.value:
        print(button.value)
        calibration()

def delta():
    global x, y, z
    dx = x - MX
    dy = y - MY
    dz = z - MZ
    print("dX: {} uT".format(dx), "dY: {} uT".format(dy),  "dZ: {} uT".format(dz))

if button.value:
    while True:
        getData()
        delta()
        time.sleep(1.0)


while True:
    buttonPress()
