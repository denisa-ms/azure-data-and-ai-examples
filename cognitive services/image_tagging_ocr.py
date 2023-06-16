# DESCRIPTION:
#     This example shows how to extract tags from Images using Azure Computer Vision services SDK.
# USAGE:
#   Make sure to build a virtual environment and install the following packages:
#       pip install -r requirements.txt
#   Create a file in this folder called ".env" and add the following lines:
#       AZURE_COMPUTER_VISION_ENDPOINT="https://<your-custom-subdomain>.cognitiveservices.azure.com/"
#       AZURE_COMPUTER_VISION_KEY="<your-computer-vision-resource-key>"
#   Run the sample with:     
#       python image_tagging_ocr.py
#     
#   For more information about how to use the Azure Computer Vision SDK, see:
#   https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/client-library?tabs=windows%2Cvisual-studio&pivots=programming-language-python

import os
from dotenv import load_dotenv
import os
import json
from array import array
import os
from PIL import Image
import sys
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

load_dotenv()
AZURE_COMPUTER_VISION_ENDPOINT = os.environ["AZURE_COMPUTER_VISION_ENDPOINT"]
AZURE_COMPUTER_VISION_KEY = os.environ["AZURE_COMPUTER_VISION_KEY"]

def analyze_image(image_url):
    # Select the visual feature(s) you want.
    remote_image_features = [VisualFeatureTypes.categories,VisualFeatureTypes.color,VisualFeatureTypes.description,VisualFeatureTypes.tags]
    results = computervision_client.analyze_image(image_url , remote_image_features)

    print("Categories from image: ")
    if (len(results.categories) == 0):
        print("No categories detected.")
    else:
        for category in results.categories:
            print("'{}' with confidence {:.2f}%".format(category.name, category.score * 100))
    print()

    print("Tags in the image: ")
    if (len(results.tags) == 0):
        print("No tags detected.")
    else:
        for tag in results.tags:
            print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
    
if __name__ == "__main__":
    computervision_client = ComputerVisionClient(AZURE_COMPUTER_VISION_ENDPOINT, CognitiveServicesCredentials(AZURE_COMPUTER_VISION_KEY))
    url = "https://i1.adis.ws/i/jpl/go_329338_a?w=1000&q=90"
    analyze_image(url)
    url = "https://i1.adis.ws/i/jpl/go_231625_a?w=1000&q=90"
    analyze_image(url)