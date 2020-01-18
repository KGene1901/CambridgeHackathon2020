import RPi.GPIO as GPIO
import integration as email
import time as t

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

start = t.time()
print("hello")
#end = t.time()
#t.sleep(5)
timeElapsed = int((t.time() - start) % 60)
print("the time elapsed is:" + str(timeElapsed)) 
#for i in range(0,5):
#    print (GPIO.input(4))
try:
   #if()
  #initialStateOfSensor = GPIO.input(4)
  notificationSend = False
  while True:
     #temp = hat.analog.one.read()
     #converting voltage to celcius
     #initialStateOfSensor = GPIO.input(4)
    if not notificationSend:
      start = t.time()
      while GPIO.input(4) == 1:
        #initialStateOfSensor = GPIO.input(4)
        print("dark")
        timeElapsed = int((t.time() - start) % 60)
        if timeElapsed >= 10:
          print("bro,: ) close your fridge")
          email.createEmail()
          notificationSend = True
          break
      print("light")
    else:
      print("waiting")
      if GPIO.input(4) != 1:
        notificationSend = False
except KeyboardInterrupt:
  pass
#email.createEmail()