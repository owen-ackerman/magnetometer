import time
import busio
import board
import digitalio
 
import adafruit_mlx90393
 
I2C_BUS = busio.I2C(board.SCL, board.SDA)
SENSOR = adafruit_mlx90393.MLX90393(I2C_BUS, gain=adafruit_mlx90393.GAIN_1X)
MX, MY, MZ = SENSOR.magnetic 

led = digitalio.DigitalInOut(board.D18)
led.direction = digitalio.Direction.OUTPUT
 
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

print(type(button.pull))
print(type(button.direction))
print(type(led.value))
print(type(button.value))

def getData():
    MX, MY, MZ = SENSOR.magnetic
    #print("[{}]".format(time.monotonic()))
    print("XXX: {} uT".format(MX), "Y: {} uT".format(MY),  "Z: {} uT".format(MZ))
    # Display the status field if an error occured, etc.
    if SENSOR.last_status > adafruit_mlx90393.STATUS_OK:
        SENSOR.display_status()
    time.sleep(1.0)

def calibration():
    x = MX
    y = MY
    z = MZ
    led.value = not button.value
    print(x, y, z)
    return x, y, z

def buttonPress():
    if not button.value:
        calibration()

while True:
    getData()
    if button.direction:
        buttonPress()
