import sys
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image as ImageKivy
from PIL import Image as ImagePIL
from kivy.core.window import Window

class Images(Widget):
    def getImages(self, inputDir):
        images = []
        if os.path.exists(inputDir):
            for file in os.listdir(inputDir):
                imgPath = "%s/%s" % (inputDir, file)
                images.append((imgPath, ImagePIL.open(imgPath)))
        else:
            print("File not found")
            return None
        return images


class Click(Widget):
    targetImage = None
    scale = None
    lastCropped = None
    cropScale = 3

    def setImage(self, img, scale):
        self.targetImage = img
        self.scale = 1/scale

    def saveImage(self):
        if self.lastCropped == None:
            print("NO CROP SELECTED")
            return
        self.lastCropped[1].save(self.lastCropped[0][2:])
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

        croppedImage = self.cropImage(self.targetImage,
                                      cropCenter, self.cropScale)
        croppedImage[1].show()
        self.lastCropped = croppedImage

        print(touch)

    def cropImage(self, image, center, scale):
        crop = []
        axis = 0
        step = 50
        for i in range(0, 4):
            crop.append(center[axis] +
                        (step * scale * (-1 if i <= 1 else 1)))
            axis = 0 if axis is 1 else 1
        return (image[0], image[1].crop(crop))

class Cropper(App):
    imageIndex = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    images = []
    size = None

    def nextImage(self, i):
            self.imageIndex = self.imageIndex + 1
            self.pil = self.images[self.imageIndex]
            self.img = ImageKivy(source=self.pil[0])
            self.img.size = self.size
            i.add_widget(self.img)

    def build(self):
        print(sys.argv)
        
        i = Images()
        self.images = i.getImages('uncropped')
        self.pil = self.images[self.imageIndex]
        scale = 0.5
        self.size = (self.pil[1].width*scale, self.pil[1].height*scale)
        Window.size = self.size

        self.click = Click()
        self.click.setImage(self.pil, scale)

        self.img = ImageKivy(source=self.pil[0])
        self.img.size = self.size
            
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
        
        displayedWidgets = [self.click, self.img, saveButton, scaleButtonUp, scaleButtonDown,
                            cropScaleDisplay, indexDisplay]

        for widget in displayedWidgets:
            i.add_widget(widget)

        return i


if __name__ == "__main__":
    Cropper().run()