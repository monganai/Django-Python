from flask import Flask
import time
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT) #heater relay


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/on")
def on():
    GPIO.output(14,GPIO.LOW)
    return "on"


@app.route("/off")
def off():
    GPIO.output(14,GPIO.HIGH)
    return "off"


@app.route("/timer")
def timer():
    return "timer"

if __name__ == "__main__":
    app.run()
