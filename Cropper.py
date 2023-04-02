import sys, os
import keyboard
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
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
    def setImage(self, img, scale):
        self.targetImage = img
        self.scale = 1/scale

    def saveImage(self, img):
        print("Saving Image")
        img[1].save(img[0][2:])

    def on_touch_down(self, touch):
        cropCenter = (touch.pos[0]*self.scale, 
                      Window.size[1]*self.scale-touch.pos[1]*self.scale)
        
        if cropCenter[0] < 100 and cropCenter[1] < 100:
            self.saveImage(self.lastCropped)
            return 
        
        cropScale = 3
        if len(sys.argv) > 2:
            cropScale = int(sys.argv[2])
        
        croppedImage = self.cropImage(self.targetImage, 
                                 cropCenter, cropScale)
        croppedImage[1].show()
        self.lastCropped = croppedImage

        print(touch)

    def cropImage(self, image, center, scale):
        crop = []
        axis = 0
        for i in range(0, 4):
            crop.append(center[axis] + 
                        (50 * scale * (-1 if i <= 1 else 1)))
            axis = 0 if axis is 1 else 1
        return (image[0], image[1].crop(crop))


class Keyboard(Widget):
    pass

    
class Cropper(App):
    def build(self):
        print(sys.argv)
        if len(sys.argv) > 1:
            imageIndex = int(sys.argv[1])
        else:
            imageIndex = 3

        i = Images()
        images = i.getImages('uncropped')
        self.pil = images[imageIndex]
        scale = 0.5
        size = (self.pil[1].width*scale, self.pil[1].height*scale)
        Window.size = size

        self.click = Click()
        self.click.setImage(self.pil, scale)
        i.add_widget(self.click)

        # def callback(instance):
        #     print('The button <%s> is being pressed' % instance.text)
        # saveButton = Button(text='Hello world', font_size=14)
        # saveButton.bind(on_press=callback)
        # i.add_widget(saveButton)

        # Display uncropped
        self.img = ImageKivy(source=self.pil[0])
        self.img.size = size
        i.add_widget(self.img)

        return i

if __name__ == "__main__":
    Cropper().run()