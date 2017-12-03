# Copyright (c) Microsoft. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# author: janpos@microsoft.com
# ==============================================================================


from cntk.ops.functions import load_model
from PIL import Image 
import numpy as np
from path_helper import *
import os
import sys
from path_helper import *

userDirectory = UserDirectory("CarRegistrationPlateDetector")

#projectName = "CarRegistrationPlate"

ModelFileName = "faster_rcnn_eval_AlexNet_e2e.model"

imageSize = (850, 850)

modelPath = os.path.abspath(os.path.join(".", "Output", ModelFileName))

print (modelPath)

model = load_model(modelPath)

imagesDir = userDirectory.getImageDir("positive")

print ("Searching for images in " + imagesDir)

imageFiles = getFilesInDirectoryByType(imagesDir, ["jpg"])

#for imageFileName in sys.argv:
for imageFileName in imageFiles:
    print ("Processing file: " + imageFileName)
    imageFileName = os.path.join(imagesDir, imageFileName)
    inMemImage = Image.open(imageFileName)
    inMemImage = inMemImage.resize(imageSize)
    
    rgb_image = np.asarray(inMemImage, dtype=np.float32) - 128
    bgr_image = rgb_image[..., [2, 1, 0]]
    pic = np.ascontiguousarray(np.rollaxis(bgr_image, 2))
    
    predictions = np.squeeze(model.eval({model.arguments[0]:[pic]}))
    top_class = np.argmax(predictions)
    print ("Labels: " + top_class)