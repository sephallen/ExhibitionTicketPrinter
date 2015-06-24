import aalib
import Image
import PIL.ImageOps
from escpos import *
import pygame
import pygame.camera
from pygame.locals import *
import os

ticketNumber = 1

def printingProcess():
    global ticketNumber

    pygame.init()
    pygame.camera.init()
    cam = pygame.camera.Camera("/dev/video1",(480,640))
    cam.start()
    # To fix image always being one behind run get_image twice
    image = cam.get_image()
    image = cam.get_image()
    pygame.image.save(image,'photo.jpg')
    cam.stop()

    screen = aalib.AsciiScreen(width=42, height=10)

    imageinv = Image.open('photo.jpg')
    inverted_image = PIL.ImageOps.invert(imageinv)
    inverted_image.save('photoinv.jpg')

    image = Image.open('photoinv.jpg').convert('L').resize(screen.virtual_size)

    screen.put_image((0, 0), image)
    asciiimage = screen.render()
    # print asciiimage

    """ (POS-58 Thermal Printer) """
    Epson = printer.Usb(0x0416,0x5011,4,0x81,0x02)
    # Print text
    Epson.set("CENTER", "A", "bold", 2, 2)
    Epson.text("Digital\n")
    Epson.text("Underground\n")
    Epson.set("CENTER", "A", "normal", 1, 1)
    Epson.text("Digital Media Design BA (Hons)\n")
    Epson.text("Bournemouth University\n")
    Epson.set("CENTER", "B", "normal", 1, 1)
    Epson.text("\n")
    Epson.text("Fare: ALL ACCESS \x9cFREE\n")
    Epson.text("Valid from: 17th - 18th July\n")
    Epson.text("Location: Christchurch Annex CAG03 - CAG06\n")
    Epson.text("\n")
    Epson.text(asciiimage)
    Epson.text("\n")
    Epson.text("\n")
    if response:
        Epson.text(response)
    Epson.text("\n")
    Epson.text("\n")
    Epson.text("http://digitalunderground.co\n")
    Epson.text("Ticket Number: ")
    Epson.text(str(ticketNumber))
    ticketNumber += 1
    # Cut paper
    Epson.cut()

while True:
    response = raw_input("Type your name and press ENTER for your ticket: ")
    printingProcess()
