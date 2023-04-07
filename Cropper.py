import sys
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image as ImageKivy
from PIL import Image as ImagePIL
from kivy.config import Config
from kivy.core.window import Window

class Images(Widget):
    curr = None
    scale = None
    lastCroppedPIL = None
    cropScale = 3
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

    def getCrop(self, touch):
        cropCenter = (touch.pos[0]*self.scale,
                      Window.size[1]*self.scale-touch.pos[1]*self.scale)

        if len(sys.argv) > 2:
            self.cropScale = int(sys.argv[2])

        croppedImagePIL = self.curr.crop(cropCenter, self.cropScale)
        self.lastCroppedPIL = (self.curr.path[2:], croppedImagePIL)
        return croppedImagePIL
    
class Click(Widget):
    i = None
    def on_touch_down(self, touch):
        print(touch)
        crop = self.i.getCrop(touch)
        crop.show()

class Cropper(App):
    i = Images()
    size = None
    scale = 0.5
    displayedWidgets = None

    def next(self, i):
            i.remove_widget(self.i.curr.kiv)
            i.nextImage()
            self.updateSize()
            self.updateIndexDisplay()
            i.add_widget(self.i.curr.kiv, 50)

    def updateSize(self):
            curr = self.i.curr
            self.size = (curr.pil.width*self.scale, 
                         curr.pil.height*self.scale)
            curr.kiv.size = self.size
            Window.size = self.size

    def updateIndexDisplay(self):
        d = self.displayedWidgets[1] # todo: find d index
        d.text = str(self.i.imageIndex)

    def incrementScale(self, d):
        self.i.cropScale = self.i.cropScale + 1
        d.text = str(self.i.cropScale)

    def deincrementScale(self, d):
        self.i.cropScale = self.i.cropScale - 1 if self.i.cropScale > 1 else 1
        d.text = str(self.i.cropScale)

    def build(self):
        i = self.i
        images = i.getImages('uncropped')
        i.setImage(images[i.imageIndex], self.scale)
        self.updateSize()
            
        saveButton = Button(text='Save', font_size=14,
                            pos=(0, self.size[1]-50), size=(50, 50),
                            color=(255, 255, 255, 1),
                            background_color=(1, 150, 1, 1),
                            on_press=lambda s: self.i.saveImage())

        scaleButtonUp = Button(text='IN', pos=(50, self.size[1]-50),
                               size=(50, 50), color=(255, 255, 255, 1),
                               background_color=(255, 255, 255, 1),
                               on_press=lambda s: self.deincrementScale(cropScaleDisplay))

        cropScaleDisplay = Label(text='3', pos=(75, self.size[1]-75), font_size=24, bold=True)

        scaleButtonDown = Button(text='OUT', pos=(150, self.size[1]-50),
                                 size=(50, 50), color=(255, 255, 255, 1),
                                 background_color=(255, 255, 255, 1),
                                 on_press=lambda s: self.incrementScale(cropScaleDisplay))
        
        nextButton = Button(text='NEXT', pos=(200, self.size[1]-50),
                                 size=(50, 50), color=(255, 255, 255, 1),
                                 background_color=(255, 255, 255, 1),
                                 on_press=lambda s: self.next(i))
        
        indexDisplay = Label(text=str(i.imageIndex), pos=(self.size[0]-75, self.size[1]-75), 
                             font_size=24, bold=True)
        
        click = Click()
        click.i = i
        
        self.displayedWidgets = [click, indexDisplay, saveButton, scaleButtonUp, scaleButtonDown,
                            cropScaleDisplay, nextButton]

        for widget in self.displayedWidgets:
            i.add_widget(widget)

        i.add_widget(self.i.curr.kiv, 50)

        return i
    
class CropperImage():
    kiv = None # display image
    pil = None 
    path = None

    def __init__(self, path=None):
        self.path = path
        self.pil = ImagePIL.open(path)
        self.kiv = ImageKivy(source=path)

    def crop(self, center, scale):
        print(center)
        crop = []
        axis = 0
        step = 50
        for i in range(0, 4):
            crop.append(center[axis] +
                        (step * scale * (-1 if i <= 1 else 1)))
            axis = 0 if axis is 1 else 1
        return self.pil.crop(crop)

if __name__ == "__main__":
    Config.set('graphics', 'resizable', False)
    Cropper().run()