import requests
import webbrowser
import cv2
import fitz
import os
from PIL import Image
import pytesseract
import docx
import numpy as np
import pandas as pd
from io import StringIO
def gazete_api(gazete_adi):
    resp = requests.get("http://nek.istanbul.edu.tr:4444/ekos/GAZETE/gazete.php", {"gazete" : gazete_adi})
    return resp.text
def harf_cevirme(kelime):
    harfler = {"ç" : "c", "ğ" : "g", "ı" : "i", "ö" : "o", "ş": "s", "ü" : "u"}
    kelime = kelime.lower()
    for i in kelime:
        if i in harfler.keys():
            kelime = kelime.replace(i, harfler[i])
    return kelime.replace(" ", "").replace("-" ,"")
gazete_adi = input("Hangi gazete?  ")
gazete_adi = harf_cevirme(gazete_adi)
gazete_html = gazete_api(gazete_adi)
gazete_html = gazete_html.split("\"")
bos_str = ""
yil = input("Hangi yılın sayısı?  ")
ay = input("Hangi ay? ")
gun = input("Hangi gün?  ")
yil = harf_cevirme(yil)
ay = harf_cevirme(ay)
gun = harf_cevirme(gun)
try:
    for i in gazete_html:
        if yil in i and ay in i:
            if len(gun) == 1:
                if "_" + gun == i[-7:-5]:
                    gazete_link = bos_str + i
                    break
            elif len(gun) == 2:
                if gun == i[-7:-5]:
                    gazete_link = bos_str + i
                    break
            else:
                gazete_link = bos_str + i
    if len(gun) != 0:
        response = requests.get(gazete_link)
        with open('gazete.pdf', 'wb') as f:
            f.write(response.content)
        print(gazete_link)
except:
    print("sayı yok")
doc = fitz.open("gazete.pdf")
sayfa = int(input("Hangi sayfa?  "))
sayfa -= 1
page = doc.loadPage(sayfa)
pix = page.getPixmap()
output = "resim.png"
pix.writePNG(output)
doc.close()
src = cv2.imread('resim.png')
scale_percent = 55
width = int(src.shape[1] * scale_percent / 100)
height = int(src.shape[0] * scale_percent / 100)
dsize = (width, height)
output = cv2.resize(src, dsize)
cv2.imwrite('kucukresim.png',output)
img = cv2.imread('kucukresim.png')
x_vector = []
y_vector = []
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        x_vector.append(x)
        y_vector.append(y)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness = 2)
        cv2.imshow("image", img)
        print(x,y)
cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)
cv2.waitKey(0)
coordinates = (int(min(x_vector)*100/55), int(min(y_vector)*100/55), int(max(x_vector)*100/55), int(max(y_vector)*100/55))
im = Image.open(r"resim.png")
im1 = im.crop(coordinates)
im1 = im1.resize((int(1.5*im1.size[0]),int(1.5*im1.size[1])))
im1 = im1.save("istenilenresim.png")
if os.path.exists("resim.png"):
    os.remove("resim.png")
if os.path.exists("gazete.pdf"):
    os.remove("gazete.pdf")
if os.path.exists("kucukresim.png"):
    os.remove("kucukresim.png")