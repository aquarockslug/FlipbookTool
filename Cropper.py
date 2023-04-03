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
        return images


class Click(Widget):
    targetImage = None
    scale = None
    lastCroppedPIL = None
    cropScale = 3

    def setImage(self, img, scale):
        self.targetImage = img
        self.scale = 1/scale

    def saveImage(self):
        if self.lastCroppedPIL == None:
            print("NO CROP SELECTED")
            return
        self.lastCroppedPIL[1].save(self.lastCroppedPIL[0])
        print("CROP SAVED")

    def incrementScale(self, d):
        self.cropScale = self.cropScale + 1
        d.text = str(self.cropScale)
    def deincrementScale(self, d):
        self.cropScale = self.cropScale - 1 if self.cropScale > 1 else 1
        d.text = str(self.cropScale)

    def on_touch_down(self, touch):
        print(touch)
        cropCenter = (touch.pos[0]*self.scale,
                      Window.size[1]*self.scale-touch.pos[1]*self.scale)

        if len(sys.argv) > 2:
            self.cropScale = int(sys.argv[2])

        croppedImagePIL = self.targetImage.crop(cropCenter, self.cropScale)
        croppedImagePIL.show()
        self.lastCroppedPIL = (self.targetImage.path[2:], croppedImagePIL)

        print(touch)


class Cropper(App):
    imageIndex = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    images = []
    size = None
    scale = 0.5
    displayedWidgets = None
    img = None

    def nextImage(self, i):
            i.remove_widget(self.img.kiv)
            self.imageIndex = self.imageIndex + 1
            self.img = self.images[self.imageIndex]
            self.updateSize()
            self.click.targetImage = self.img
            i.add_widget(self.img.kiv, 50)

    def updateSize(self):
            self.size = (self.img.pil.width*self.scale, 
                         self.img.pil.height*self.scale)
            self.img.kiv.size = self.size
            Window.size = self.size

    def build(self):
        print(sys.argv)
        
        i = Images()
        self.images = i.getImages('uncropped')
        self.img = self.images[self.imageIndex]
        self.updateSize()

        self.click = Click()
        self.click.setImage(self.img, self.scale)
            
        saveButton = Button(text='Save', font_size=14,
                            pos=(0, self.size[1]-50), size=(50, 50),
                            color=(255, 255, 255, 1),
                            background_color=(1, 150, 1, 1),
                            on_press=lambda s: self.click.saveImage())

        scaleButtonUp = Button(text='IN', pos=(50, self.size[1]-50),
                               size=(50, 50), color=(255, 255, 255, 1),
                               background_color=(255, 255, 255, 1),
                               on_press=lambda s: self.click.deincrementScale(cropScaleDisplay))

        cropScaleDisplay = Label(text='3', pos=(75, self.size[1]-75), font_size=24, bold=True)

        scaleButtonDown = Button(text='OUT', pos=(150, self.size[1]-50),
                                 size=(50, 50), color=(255, 255, 255, 1),
                                 background_color=(255, 255, 255, 1),
                                 on_press=lambda s: self.click.incrementScale(cropScaleDisplay))
        
        nextButton = Button(text='NEXT', pos=(200, self.size[1]-50),
                                 size=(50, 50), color=(255, 255, 255, 1),
                                 background_color=(255, 255, 255, 1),
                                 on_press=lambda s: self.nextImage(i))
        
        indexDisplay = Label(text=str(self.imageIndex), pos=(self.size[0]-75, self.size[1]-75), 
                             font_size=24, bold=True)
        
        self.displayedWidgets = [self.click, saveButton, scaleButtonUp, scaleButtonDown,
                            cropScaleDisplay, indexDisplay, nextButton]

        for widget in self.displayedWidgets:
            i.add_widget(widget)

        i.add_widget(self.img.kiv, 50)

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