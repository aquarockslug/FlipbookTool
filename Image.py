import sys
import os
from kivy.uix.widget import Widget
from kivy.uix.image import Image as ImageKivy
from PIL import Image as ImagePIL
from kivy.config import Config
from kivy.core.window import Window

class ImageController(Widget):
    curr = None
    scale = None
    lastCroppedPIL = None
    images = None

    imageIndex = int(sys.argv[1]) if len(sys.argv) > 1 else 0

    def getImages(self, inputDir):
        images = []
        if os.path.exists(inputDir):
            for file in os.listdir(inputDir):
                imgPath = "%s/%s" % (inputDir, file)
                image = CropperImage(imgPath)
                images.append(image)
        else:
            print("File not found")
            return None
        self.images = images
        return images

    def nextImage(self):
        self.imageIndex = self.imageIndex + 1
        self.curr = self.images[self.imageIndex]
        return self.curr
    
    def setImage(self, img, scale):
        self.curr = img
        self.scale = 1/scale

    def saveImage(self):
        if self.lastCroppedPIL == None:
            print("NO CROP SELECTED")
            return
        self.lastCroppedPIL[1].save(self.lastCroppedPIL[0])
        print("CROP SAVED")
    
class Click(Widget):
    ic = None
    c = None
    selection = []

    def on_touch_down(self, touch):
        self.selection.append(touch)
        if len(self.selection) >= 2:
            self.c.createCrop(self.selection)
            self.selection = []
            return
        
        print(touch)


class CropperImage():
    kiv = None # display image
    pil = None 
    path = None

    def __init__(self, path=None):
        self.path = path
        self.pil = ImagePIL.open(path)
        self.kiv = ImageKivy(source=path)

    def crop(self, center, scale):
        # print("center: " + center)
        crop = []
        axis = 0
        step = 50
        for i in range(0, 4):
            crop.append(center[axis] + (step * scale * (-1 if i <= 1 else 1)))
            axis = 0 if axis == 1 else 1
        return self.pil.crop(crop)