
import base64
import io
import json
import requests

import pprint
import math
import os


# Based on https://cloud.google.com/vision/automl/docs/containers-gcs-tutorial
def container_predict(image_file_path, image_key):
  
  automlDockerServiceName = "automl-model"
  automlDockerPortNumber = "8501"

  """Sends a prediction request to TFServing docker container REST API.

  Args:
      image_file_path: Path to a local image for the prediction request.
      image_key: Your chosen string key to identify the given image.
      port_number: The port number on your device to accept REST API calls.
  Returns:
      The response of the prediction request.
  """

  with io.open(image_file_path, 'rb') as image_file:
      encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

  # The example here only shows prediction with one image. You can extend it
  # to predict with a batch of images indicated by different keys, which can
  # make sure that the responses corresponding to the given image.
  instances = {
          'instances': [
                  {'image_bytes': {'b64': str(encoded_image)},
                    'key': image_key}
          ]
  }

  # This example shows sending requests in the same server that you start
  # docker containers. If you would like to send requests to other servers,
  # please change localhost to IP of other servers.
  url = "http://" + automlDockerServiceName + ":" + automlDockerPortNumber + "/v1/models/default:predict"

  response = requests.post(url, data=json.dumps(instances))
  return response.json() # This fails with escaping error, if the file analyzed is not a supported image file

def getKeyValue(data, key):
#  labelNeedle = "upvote"
  labelNumber = False
  i = 0

  for label in data['predictions'][0]['labels']:
    if label == key:
      labelNumber = i
    else:
      i = i + 1

#  print(labelNumber)

  value = data['predictions'][0]['scores'][labelNumber]

  ret = {}
  ret[key] = value
  return ret


def getAllKeysValues(data):
  ret = {}
  for label in data['predictions'][0]['labels']:
    ret.update(getKeyValue(data, label))
  return ret

# --------------------------------------------

print("Start\n")
baseDir = "images"
print(baseDir + "\n")
data = {}

for filename in os.listdir(baseDir):
  if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):

    filePath = baseDir + "/" + filename
    predictionJson = container_predict(filePath, filename)
  #  print(predictionJson['predictions'][0]['labels'])

    imageData = {}
    imageData[predictionJson['predictions'][0]['key']] = getAllKeysValues(predictionJson)
    data.update(imageData)

    print(predictionJson)

# DEBUG: Change file name based on quality
    qualitySuffix = str(imageData[filename]['upvote']) + "000"
    qualitySuffix= qualitySuffix[2:5]
    print(qualitySuffix)

    oldFilePath = filePath
    newFilePath = baseDir + "/" + qualitySuffix + "_" + filename;

    print("\n" + oldFilePath)
    print("\n" + newFilePath)

    os.rename(oldFilePath, newFilePath)


#print("\n---------------------------------\n")
#print(data)

print("\n---------------------------------\n")

sortBy = "larva"
sortBy = "upvote"

so = sorted(data.items(), key=lambda item: float(item[1][sortBy]))
print(so)

#for x in range(0, 400):
#  fileNumberString = leadingZeros(x)
#  filePath = baseFilePath + "." + fileNumberString + ".png"
#  fileKey = fileNumberString

  # Check if file = segments exists
#  if not os.path.exists(filePath):
#    print("\nNo more segments")
#    break

  # Predict
#  predictionJson = container_predict(filePath, fileKey)

  # Format results
#  resultDict = toDict(predictionJson)
#  print(toHumanReadable(resultDict))

#  pp = pprint.PrettyPrinter(indent=2)
#  pp.pprint(resultDict)




#  print(json.dumps(resultDict, default_flow_style=False))

#  print(result.json())


#response = requests.get("http://localhost:8081")
#print(response)

print("\nEnd")

# Muutin tässä googlen ohjeeseen verrattuna: localhost -> service name
