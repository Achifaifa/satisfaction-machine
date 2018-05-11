#!/usr/bin/env python

import time, os, psycopg2
import RPi.GPIO as GPIO

def log(msg):
  print "[%s] %s"%(time.time(), msg)

def log_event(type):
  print "[%s] %s button pressed"%(time.time(), type)

def fuck():
  log("Aborting")
  try:
    GPIO.cleanup()
    cur.close()
    comm.close()
  except:
    pass
  finally:
    exit()

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
  try:
    cur.execute("INSERT INTO ratings (timestamp, data) VALUES (%s, %s);", (t, value))
    conn.commit()
  except Exception as e:
    log("Error sending to database (%s)"%e)
    try:
      log("Rolling back changes")
      conn.rollback()
    except Exception as e:
      log("Failed to rollback changes")
      fuck()

###

log("Starting")

log("Waiting for internet connection")
while 1:
  try:
    time.sleep(5)
    r=os.system("ping 8.8.8.8 -c1 -w2 > /dev/null 2>&1")
    if not r:
      log("Network up")
      break
    else: 
      log("Network down (%s)"%r)
  except exception as e:
    log("Error checking network (%s)"%e)
    continue

log("Loading creds")
try:
  with open("./postgres-creds","r") as creds:
    c=[i.strip() for i in creds.readlines()]
  log("Creds loaded")
except Exception as e:
  log("Unable to load creds (%s)"%e)
  fuck()

log("Connecting to database")
try:
  conn=psycopg2.connect("dbname=satisfaction user=root host=%s port=%s password=%s"%(c[0],c[1],c[2]))
  cur=conn.cursor()
  log("Connection to database established")
except Exception as e: 
  log("Database connection failed (%s)"%e)
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
except Exception as e:
  log("Failed to set GPIO pins (%s)"%e)
  fuck()

log("Ready")
while 1:
  try:
    pass
  except Exception as e:
    log("Error in main loop (%s)"%s)
  except KeyboardInterrupt:
    log("CTRL+C detected")
    fuck()
