#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def callback_positive(ev):
  print "[%s] Positive button pressed"%time.time()

def callback_neutral(ev):
  print "[%s] Neutral button pressed"%time.time()

def callback_negative(ev):
  print "[%s] Negative button pressed"%time.time()

GPIO.add_event_detect(23, GPIO.RISING, callback=callback_positive, bouncetime=500)
GPIO.add_event_detect(24, GPIO.RISING, callback=callback_negative, bouncetime=500)
GPIO.add_event_detect(25, GPIO.RISING, callback=callback_neutral, bouncetime=500

while 1:
  pass
GPIO.cleanup()
