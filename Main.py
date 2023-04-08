import math
import sys
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from Image import ImageController
from Image import Click


class Cropper(App):
    ic = ImageController()
    size = None
    scale = 0.5
    if len(sys.argv) > 1:
        oneClick = True if sys.argv[1] == "true" else False
    else:
        oneClick = False
    oneClickCropScale = 3

    crop = None
    margin = 1.5
    displayedWidgets = None

    def next(self, ic):
        ic.remove_widget(self.ic.curr.kiv)
        ic.nextImage()
        self.updateSize()
        self.updateIndexDisplay()
        ic.add_widget(self.ic.curr.kiv, 50)

    # Use the positions of the last two clicks to find center and scale of crop
    def createCrop(self, selection):
        cropScale = 1 / self.scale

        if self.oneClick:
            self.crop = self.ic.curr.crop((selection[0]*cropScale, 
                                          Window.size[1]*cropScale-selection[1]*cropScale),
                                          self.oneClickCropScale)
            self.crop.show()
            return

        p2 = None
        if selection[0] is not None:
            p1 = (selection[0].pos[0]*cropScale,
                  Window.size[1]*cropScale-selection[0].pos[1]*cropScale)
            x1, y1 = p1[0], p1[1]
        if selection[1] is not None:
            p2 = (selection[1].pos[0]*cropScale,
                  Window.size[1]*cropScale-selection[1].pos[1]*cropScale)
            x2, y2 = p2[0], p2[1]

        if p2 == None:
            center = (x1, y1)
            return

        a, b = abs(x1 - x2), abs(y1 - y2)
        distance = (a**2 + b**2)**0.5
        center = [(x1 + x2)/2, (y1 + y2)/2]
        angle = math.degrees(math.atan(a / b))

        crop = self.ic.curr.crop(center, distance/100*self.margin)
        self.crop = crop.rotate(angle if x1 < x2 else -angle)
        self.crop.show()

        # save crop to its CropperImage

    def showCrop(self):
        if self.crop is not None:
            self.crop.show()

    def updateSize(self):
        curr = self.ic.curr
        self.size = (curr.pil.width*self.scale,
                     curr.pil.height*self.scale)
        curr.kiv.size = self.size
        Window.size = self.size

    def updateIndexDisplay(self):
        d = self.displayedWidgets[1]  # todo: find d index
        d.text = str(self.ic.imageIndex)

    def incrementScale(self, d):
        self.oneClickCropScale += 1
        d.text = str(self.oneClickCropScale)

    def deincrementScale(self, d):
        self.oneClickCropScale = self.oneClickCropScale-1 if self.oneClickCropScale > 1 else 1
        d.text = str(self.oneClickCropScale)

    def build(self):
        ic = self.ic
        images = ic.getImages('uncropped')
        ic.setImage(images[ic.imageIndex], self.scale)
        self.updateSize()

        saveButton = Button(text='SAVE', font_size=14,
                            pos=(0, self.size[1]-50), size=(50, 50),
                            color=(255, 255, 255, 1),
                            background_color=(1, 150, 1, 1),
                            on_press=lambda s: self.ic.saveImage(self.crop))

        nextButton = Button(text='NEXT', pos=(50, self.size[1]-50),
                                 size=(50, 50), color=(255, 255, 255, 1),
                                 background_color=(255, 255, 255, 1),
                                 on_press=lambda s: self.next(ic))

        scaleButtonUp = Button(text='IN', pos=(100, self.size[1]-50),
                               size=(50, 50), color=(255, 255, 255, 1),
                               background_color=(255, 255, 255, 1),
                               on_press=lambda s:
                               self.deincrementScale(cropScaleDisplay))

        cropScaleDisplay = Label(text='3', pos=(
            125, self.size[1]-75), font_size=24, bold=True)

        scaleButtonDown = Button(text='OUT', pos=(200, self.size[1]-50),
                                 size=(50, 50), color=(255, 255, 255, 1),
                                 background_color=(255, 255, 255, 1),
                                 on_press=lambda s:
                                 self.incrementScale(cropScaleDisplay))

        
        indexDisplay = Label(text=str(ic.imageIndex), pos=(self.size[0]-75, self.size[1]-75),
                             font_size=24, bold=True)

        click = Click()
        click.ic = ic
        click.c = self


        self.displayedWidgets = [click, indexDisplay, saveButton, nextButton]
        if self.oneClick:
            self.displayedWidgets += [scaleButtonUp, scaleButtonDown, cropScaleDisplay]
        for widget in self.displayedWidgets:
            ic.add_widget(widget)

        ic.add_widget(self.ic.curr.kiv, 50)

        return ic


if __name__ == "__main__":
    Cropper().run()
