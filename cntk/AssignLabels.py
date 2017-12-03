# Copyright (c) Microsoft. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# author: janpos@microsoft.com
# ==============================================================================


from __future__ import print_function
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

from PIL import ImageTk
from cntk_helpers import *
import string
import math
from constants import Constants
from path_helper import *
import numpy as np
from plot_helpers import *

####################################
# Parameters
####################################
userDirectory = UserDirectory()
imgDir = UserDirectory.getMissingLabelsImgageDir()

const = Constants()
characters = const.getCzechCharacters()

colCount = 4

drawLineThickness = 1

classes = list(characters)

#no need to change these
drawingImgSize = 1000
boxWidth = 10
boxHeight = 2


####################################
# Main
####################################
# define callback function for tk button
def buttonPressedCallback(s):
    global global_lastButtonPressed
    global_lastButtonPressed = s

# create UI
objectNames = np.sort(classes).tolist()
objectNames += ["UNDEFINED", "SPACE"]
tk = Tk()
if len(objectNames) % colCount > 0:
    rowCount = math.floor(len(objectNames) / colCount) + 1
else:
    rowCount = len(objectNames)
w = Canvas(tk, width=(colCount * boxWidth) + drawingImgSize, height=rowCount * boxHeight, bd = boxWidth, bg = 'white')
w.grid(row = rowCount, column = colCount, columnspan = 1)

for objectIndex,objectName in enumerate(objectNames):
    b = Button(width=boxWidth, height=boxHeight, text=objectName, command=lambda s = objectName: buttonPressedCallback(s))
    b.grid(row = math.floor(objectIndex/colCount), column = objectIndex % colCount)

# loop over all images
imgFilenames = getFilesInDirectoryByType(imgDir, ["jpg","png"])
for imgIndex, imgFilename in enumerate(imgFilenames):
    print (imgIndex, imgFilename)
    labelsPath = os.path.join(imgDir, imgFilename[:-4] + ".bboxes.labels.tsv")
    if os.path.exists(labelsPath):
        print ("Skipping image {:3} ({}) since annotation file already exists: {}".format(imgIndex, imgFilename, labelsPath))
        continue

    # load image and ground truth rectangles
    img = imread(os.path.join(imgDir,imgFilename))
    rectsPath = os.path.join(imgDir, imgFilename[:-4] + ".bboxes.tsv")
    rects = [ToIntegers(rect) for rect in readTable(rectsPath)]

    # annotate each rectangle in turn
    labels = []
    for rectIndex,rect in enumerate(rects):
        imgCopy = img.copy()
        drawRectangles(imgCopy, [rect], thickness = drawLineThickness)

        # draw image in tk window
        imgTk, _ = imresizeMaxDim(imgCopy, drawingImgSize, boUpscale = True)
        imgTk = ImageTk.PhotoImage(imconvertCv2Pil(imgTk))
        label = Label(tk, image=imgTk)
        label.grid(row=0, column=colCount, rowspan=drawingImgSize)
        tk.update_idletasks()
        tk.update()

        # busy-wait until button pressed
        global_lastButtonPressed = None
        while not global_lastButtonPressed:
            tk.update_idletasks()
            tk.update()

        # store result
        print ("Button pressed = ", global_lastButtonPressed)
        character = const.getNationalCharacterAlternative(global_lastButtonPressed)
        labels.append(character)

    writeFile(labelsPath, labels)
tk.destroy()
print ("DONE.")