import board
import time
import busio
import adafruit_scd30
import neopixel
import adafruit_ds1307
#import digitalio
import RPi.GPIO as GPIO

pwm = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm, GPIO.OUT)
p = GPIO.PWM(pwm, 100)

from flask import Flask, render_template
app  = Flask(__name__)
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

rtc = adafruit_ds1307.DS1307(i2c)

relay1 = 23
relay2 = 24
relay3 = 9
relay4 = 7

GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
GPIO.setup(relay3, GPIO.OUT)
GPIO.setup(relay4, GPIO.OUT)

pixel_pin = board.D10
num_pixels = 8
ORDER = neopixel.GRB

GPIO.output(relay1, GPIO.HIGH)
GPIO.output(relay2, GPIO.HIGH)
GPIO.output(relay3, GPIO.HIGH)
GPIO.output(relay4, GPIO.HIGH)

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

@app.route('/scd30')
def scd30():
    return "C:{0:.2f} T:{1:.2f} H:{2:.2f};ok".format(scd.CO2,scd.temperature,scd.relative_humidity) 

@app.route('/neopixel/<valR>/<valG>/<valB>')
def neopixel(valR,valG,valB):
    pixels.fill((int(valR),int(valG),int(valB)))
    pixels.show();
    return "R:"+valR+" G:"+valG+" B:"+valB+";ok" 

@app.route('/datetime')
def datetime():
    t = rtc.datetime
    return str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec)

@app.route('/relay/<no>/<val>')
def relay(no, val):
    rel = relay1 
    if (int(no) == 1):
        rel = relay1
    elif (int(no) == 2):
        rel = relay2
    elif (int(no) == 3):
        rel = relay3
    elif (int(no) == 4):
        rel = relay4

    if (int(val) > 0):
        GPIO.output(rel, GPIO.LOW)
    else:
        GPIO.output(rel, GPIO.HIGH)
    return "R"+no+":"+val+";ok" 

@app.route('/pwm/<val>')
def pwm(val):
    p.start(int(val))

    return "P:"+val+";ok"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

