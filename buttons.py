#!/usr/bin/env python

import time, psycopg2
import RPi.GPIO as GPIO

log("Starting")

log("Loading creds")
try:
  with open("./postgres-creds","r") as creds:
    c=[i.strip() for i in creds.readlines()]
  log("Creds loaded")
except:
  log("Unable to load creds. Aborting")
  fuck()

log("Connecting to database")
try:
  conn=psycopg2.connect("dbname=satisfaction user=root host=%s port=%s password=%s"%(c[0],c[1],c[2]))
  cur=conn.cursor()
  log("Connection to database established")
except: 
  log("Database connection failed")
  fuck()

log("Setting up GPIO pins")
try:
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.add_event_detect(23, GPIO.RISING, callback=callback_positive, bouncetime=500)
  GPIO.add_event_detect(24, GPIO.RISING, callback=callback_negative, bouncetime=500)
  GPIO.add_event_detect(25, GPIO.RISING, callback=callback_neutral, bouncetime=500)
  log("GPIO pins set")
except:
  log("Failed to set GPIO pins")
  fuck()

def callback_positive(ev):

  log_event("Positive")
  store_rating("+1")

def callback_neutral(ev):

  log_event("Neutral")
  store_rating("0")

def callback_negative(ev):

  log_event("Negative")
  store_rating("-1")

def store_rating(value):
  t=time.time()
  cur.execute("INSERT INTO ratings (timestamp, data) VALUES (%i, %s)",
    (t, value))
  conn.commit()

def log(msg):
  print "[%s] %s"%(time.time(), msg)

def log_press(type):
  print "[%s] %s button pressed"%(time.time(), type)


def fuck():
  GPIO.cleanup()
  cur.close()
  comm.close()
  exit()

while 1:
  try:
    pass
  except:
    fuck()
