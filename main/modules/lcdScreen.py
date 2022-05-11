import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class lcdScreen:
    # constructor
    def __init__(self):

        # Initialize SPI bus
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # Initialize display
        dc = digitalio.DigitalInOut(board.D23)  # data/command
        cs1 = digitalio.DigitalInOut(board.CE1)  # chip select CE1 for display
        reset = digitalio.DigitalInOut(board.D24)  # reset
        self.display = adafruit_pcd8544.PCD8544(spi, dc, cs1, reset, baudrate= 1000000)
        self.display.bias = 4
        self.display.contrast = 60
        self.display.invert = True
        
        #  Clear the display.  Always call show after changing pixels to make the display update visible!
        self.display.fill(0)
        self.display.show()

        # Load default font.
        self.font = ImageFont.load_default()
        #font=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 10)

        # Get drawing object to draw on image
        self.image = Image.new('1', (self.display.width, self.display.height)) 
        draw = ImageDraw.Draw(self.image)

        # Draw a white filled box to clear the image.
        draw.rectangle((0, 0, self.display.width, self.display.height), outline=255, fill=255)

    # set the text to display, takes an array of strings, each line on the display is one string in the array
    def setText(self, textArray):
        self.clearDisplay()
        draw = ImageDraw.Draw(self.image)
        for i in range(len(textArray)):
            draw.text((1, i*8), textArray[i], font=self.font)
        self.display.image(self.image)
        self.display.show()
    
    # set an image on the display, takes a path to the image
    def setImage(self, imagePath):
        self.clearDisplay()
        image = Image.open(imagePath).resize((self.display.width, self.display.height), Image.ANTIALIAS).convert('1')

        self.display.image(image)
        self.display.show()

    # clear display
    def clearDisplay(self):
        draw = ImageDraw.Draw(self.image)
        draw.rectangle((0, 0, self.display.width, self.display.height), outline=255, fill=255)
        self.display.image(self.image)
        self.display.show()