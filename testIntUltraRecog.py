from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import spoonacular as sp
api = sp.API("32705ed053d745d3b9cfe60f248d1ee4")
from picamera import PiCamera
from time import sleep
#setting up camera
camera = PiCamera()
camera.resolution = (1800,1200)
camera.framerate = 15
import asyncio, io, glob, os, sys, time, uuid, requests
from array import array
import os
import testUltraSonic as ultSonic
from io import BytesIO
from PIL import Image
import sys
import time
# Add your Computer Vision subscription key to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
# Add your Computer Vision endpoint to your environment variables.
if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
#print (subscription_key)
#print (endpoint)
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
#remote_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"
#userProfile = os.environ['userprofile']
imagePath = "/home/pi/Desktop/image.jpg"
#ultSonic.calculateDistance()
def putInFridge(namePara):
    with open("exampleFridgeContent.txt", "r") as f:
        data = f.readlines()
    indexFound = -1
    for i in range(len(data)):
        ingN = data[i].split('$')[0]
        if ingN.lower()==namePara.lower():
            indexFound = i
    f = open("exampleFridgeContent.txt","w")
    for i in range(len(data)):
        if i == indexFound:
            #Code here increments the amount of stuff in the fridge
            split = data[i].split('$')
            newAmount = int(split[1])+1
            f.write(split[0]+'$'+str(newAmount)+'$'+split[2])
        else:
            f.write(data[i])
    print(indexFound)
    if indexFound==-1:
        f.write('\n'+namePara+'$'+str(1)+'$')
    f.close()
while True:
  #ultSonic.calculateDistance()
  if(ultSonic.calculateDistance() <= 10):
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/Desktop/image.jpg')
    camera.stop_preview()
    buffer = io.BytesIO()
    buffer.write(open(imagePath, 'rb').read())
    buffer.seek(0)
    print("===== Detect Objects - remote =====")
    print("===== Describe an image - remote =====")
    # Call API
    description_results = computervision_client.describe_image_in_stream(image=buffer)
    print("Description of remote image: ")
    if (len(description_results.captions) == 0):
      print("No description detected.")
    else:
      for caption in description_results.captions:
        print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
        print(api.detect_food_in_text(caption.text).json())
        name = api.detect_food_in_text(caption.text).json()['annotations']
        if len(name)!=0:
        	name2 = name[0]['annotation']
	        if name2!="":
	            print(name2)
	            putInFridge(name2)
	            print("New entry added to the fridge")
    sleep(2)

