import time
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class lcdScreen:
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

    def setText(self, textArray):
        self.clearDisplay()
        draw = ImageDraw.Draw(self.image)
        for i in range(len(textArray)):
            draw.text((1, i*8), textArray[i], font=self.font)
        self.display.image(self.image)
        self.display.show()

    def clearDisplay(self):
        draw = ImageDraw.Draw(self.image)
        draw.rectangle((0, 0, self.display.width, self.display.height), outline=255, fill=255)
        self.display.image(self.image)
        self.display.show()



if __name__ == "__main__":
    lcd = lcdScreen()

    text = ["Hello World!", 
    "Hello World!", 
    "Hello World!", 
    "Hello World!", 
    "Hello World!"]
    lcd.setText(text)

    time.sleep(1)

    text[1] = "text changed"
    text[2] = "this is a test"
    lcd.setText(text)
    time.sleep(1)

    lcd.clearDisplay()