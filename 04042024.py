from io import BytesIO
import os
from PIL import Image, ImageDraw
import requests

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

'''
This example uses a local image and a remote URL image for analysis. 
It detects the objects in them, draws a bounding box around them, and then detects the tags in the image.

Install the Computer Vision SDK:
pip install --upgrade azure-cognitiveservices-vision-computervision

References: 
Computer Vision SDK: https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-computervision/?view=azure-python
Computer Vision documentation: https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/
Computer Vision API: https://westus.dev.cognitive.microsoft.com/docs/services/5cd27ec07268f6c679a3e641/operations/56f91f2e778daf14a499f21b
'''

# Local and remote (URL) images
# Download the objects image from here (and place in your root folder): 
# https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/ComputerVision/Images
local_image = "01dwq/0001dwq/2024_0403_104440_060.JPG"
# remote_image = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/objects.jpg"
# Select visual feature type(s) you want to focus on when analyzing an image
image_features = ['objects', 'tags']

'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = 'cccdf57814e9416d85270af465a1a960'
endpoint = 'https://try000004.cognitiveservices.azure.com/'

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

#Tags=["outdoor","plant","sky","tree","grass","nature","subshrub","shrub","vegetation","park"]

# Draws a bounding box around an object found in image
def drawRectangle(object, draw):
    # Represent all sides of a box
    rect = object.rectangle
    left = rect.x
    top = rect.y
    right = left + rect.w
    bottom = top + rect.h
    coordinates = ((left, top), (right, bottom))
    draw.rectangle(coordinates, outline='red')


# Gets the objects detected in the image
def getObjects(results, draw):
    # Print results of detection with bounding boxes
    print("OBJECTS DETECTED:")
    if len(results.objects) == 0:
        print("No objects detected.")
    else:
        for object in results.objects:
            print("object at location {}, {}, {}, {}".format(
                object.rectangle.x, object.rectangle.x + object.rectangle.w,
                object.rectangle.y, object.rectangle.y + object.rectangle.h))
            drawRectangle(object, draw)
        print()
        print('Bounding boxes drawn around objects... see popup.')
    print()


# Prints the tag found from the image
def getTags(results,Tags_Dict):
    # Print results with confidence score
    print("TAGS: ")
    if (len(results.tags) == 0):
        print("No tags detected.")
    else:
        for tag in results.tags:
            print("'{}' with confidence {:.2f}%".format(
                tag.name, tag.confidence * 100))
            Tags_Dict.add(tag.name)
    print()


'''
Analyze Image - local
This example detects different kinds of objects with bounding boxes and the tags from the image.
'''
print("===== Analyze Image - local =====")
print()
file_path = "resizephotos"
Tags_Dict=set()
# Get local image with different objects in it
for local_image in os.listdir(file_path):
    print(local_image)
    if local_image == ".DS_Store":
        continue
    else:
        local_image_objects = open("resizephotos/{}".format(local_image),"rb")
        image_l = Image.open("resizephotos/{}".format(local_image))
    #image_l = image_l.resize((640,480))
    #image_l.save("resizephotos/{}".format(local_image))
        draw = ImageDraw.Draw(image_l)
        results_local = computervision_client.analyze_image_in_stream(local_image_objects, image_features)
        getObjects(results_local, draw)
        getTags(results_local,Tags_Dict)


# Display the image in the users default image browser.
# image_l.show()
print()


'''
# Detect Objects - remote
# This example detects different kinds of objects with bounding boxes in a remote image.
# '''
# print("===== Analyze Image - remote =====")
# print()
# # Call API with URL to analyze the image
# results_remote = computervision_client.analyze_image(remote_image, image_features)

# # Download the image from the url, so can display it in popup/browser
# object_image = requests.get(remote_image)
# image_r = Image.open(BytesIO(object_image.content))
# draw = ImageDraw.Draw(image_r)

# # Show bounding boxes around objects
# getObjects(results_remote, draw)
# # Print tags from image
# getTags(results_remote)

# # Display the image in the users default image browser.
# image_r.show()
