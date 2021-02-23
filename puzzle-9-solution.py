#!/usr/bin/env python3

# At a minimum you may need to 'pip3 install Pillow' and 'pip3 install pyzbar'
# You will also need the zbar library

import base64
import gzip
from PIL import Image
import numpy as np
from pyzbar.pyzbar import decode
import os

# NOTE: MacOSX zbar apparently won't decode the QR correctly,
# this works on Linux CentOS 8.

# emojis at the end of the PNG were identified using:
# string --encoding=S puzzle-9.png
# Side note, MacOSX 'string' does not support --encoding=S

fsize = os.stat("puzzle-9.png").st_size
with open("puzzle-9.png") as f:
    # skip the real png data
    f.seek(328510)
    fdata = f.read()

uchars = list(fdata)

# table provided by the key image, but a little hard to decode visually
transform = dict()
transform[b'\U0001F601'.decode('raw_unicode_escape')]  ="x"
transform[b'\U0001F36B'.decode('raw_unicode_escape')]  ="m"
transform[b'\U0001F60A'.decode('raw_unicode_escape')]  ="5"
transform[b'\U0001F9D1'.decode('raw_unicode_escape')]  ="b"
transform[b'\U0001F49E'.decode('raw_unicode_escape')]  ="M"
transform[b'\U0001F603'.decode('raw_unicode_escape')]  ="v"
transform[b'\U00002763'.decode('raw_unicode_escape')]  ="P"
transform[b'\U0001F46B'.decode('raw_unicode_escape')]  ="d"
transform[b'\U0001F60D'.decode('raw_unicode_escape')]  ="B"
transform[b'\U0001F600'.decode('raw_unicode_escape')]  ="u"
transform[b'\U0001F493'.decode('raw_unicode_escape')]  ="L"
transform[b'\U0001F49B'.decode('raw_unicode_escape')]  ="T"
transform[b'\U0001F48F'.decode('raw_unicode_escape')]  ="f"
transform[b'\U0001F90D'.decode('raw_unicode_escape')]  ="Z"
transform[b'\U0001F618'.decode('raw_unicode_escape')]  ="C"
transform[b'\U0001F339'.decode('raw_unicode_escape')]  ="k"
transform[b'\U0001F3E9'.decode('raw_unicode_escape')]  ="n"
transform[b'\U0001F497'.decode('raw_unicode_escape')]  ="K"
transform[b'\U0001F48B'.decode('raw_unicode_escape')]  ="F"
transform[b'\U0001F606'.decode('raw_unicode_escape')]  ="y"
transform[b'\U0001F46D'.decode('raw_unicode_escape')]  ="c"
transform[b'\U0001F970'.decode('raw_unicode_escape')]  ="A"
transform[b'\U0001F91F'.decode('raw_unicode_escape')]  ="a"
transform[b'\U0001F468'.decode('raw_unicode_escape')]  ="h"
transform[b'\U0001F46C'.decode('raw_unicode_escape')]  ="e"
transform[b'\U0001F9E1'.decode('raw_unicode_escape')]  ="S"
transform[b'\U0001F61B'.decode('raw_unicode_escape')]  ="/"
transform[b'\U0001F495'.decode('raw_unicode_escape')]  ="N"
transform[b'\U0001F48D'.decode('raw_unicode_escape')]  ="t"
transform[b'\U0001F380'.decode('raw_unicode_escape')]  ="p"
transform[b'\U0001F491'.decode('raw_unicode_escape')]  ="i"
transform[b'\U0001F90E'.decode('raw_unicode_escape')]  ="X"
transform[b'\U0001F498'.decode('raw_unicode_escape')]  ="H"
transform[b'\U0001F60B'.decode('raw_unicode_escape')]  ="+"
transform[b'\U0001F49A'.decode('raw_unicode_escape')]  ="U"
transform[b'\U0001F605'.decode('raw_unicode_escape')]  ="z"
transform[b'\U0001F9F8'.decode('raw_unicode_escape')]  ="r"
transform[b'\U0001F381'.decode('raw_unicode_escape')]  ="q"
transform[b'\U0001F490'.decode('raw_unicode_escape')]  ="j"
transform[b'\U0001F5A4'.decode('raw_unicode_escape')]  ="Y"
transform[b'\U0001F499'.decode('raw_unicode_escape')]  ="V"
transform[b'\U0001F643'.decode('raw_unicode_escape')]  ="3"
transform[b'\U0001F48C'.decode('raw_unicode_escape')]  ="G"
transform[b'\U0001F63B'.decode('raw_unicode_escape')]  ="E"
transform[b'\U0001F923'.decode('raw_unicode_escape')]  ="0"
transform[b'\U0001F609'.decode('raw_unicode_escape')]  ="4"
transform[b'\U0001F469'.decode('raw_unicode_escape')]  ="g"
transform[b'\U0001F929'.decode('raw_unicode_escape')]  ="7"
transform[b'\U0001F49C'.decode('raw_unicode_escape')]  ="W"
transform[b'\U00002665'.decode('raw_unicode_escape')]  ="s"
transform[b'\U0001F525'.decode('raw_unicode_escape')]  ="o"
transform[b'\U0001F940'.decode('raw_unicode_escape')]  ="l"
transform[b'\U00002764'.decode('raw_unicode_escape')]  ="R"
transform[b'\U0001F49D'.decode('raw_unicode_escape')]  ="I"
transform[b'\U0001F642'.decode('raw_unicode_escape')]  ="2"
transform[b'\U0001F494'.decode('raw_unicode_escape')]  ="Q"
transform[b'\U0001F607'.decode('raw_unicode_escape')]  ="6"
transform[b'\U0001F61A'.decode('raw_unicode_escape')]  ="D"
transform[b'\U0001F602'.decode('raw_unicode_escape')]  ="1"
transform[b'\U0001F619'.decode('raw_unicode_escape')]  ="9"
transform[b'\U0001F617'.decode('raw_unicode_escape')]  ="8"
transform[b'\U0001F49F'.decode('raw_unicode_escape')]  ="O"
transform[b'\U0001F604'.decode('raw_unicode_escape')]  ="w"
transform[b'\U0001F496'.decode('raw_unicode_escape')]  ="J"
transform['='] = '='

tchar=list()
for char in uchars:
    tchar.append(transform[char])

converted_output = ''.join(tchar)

# 64 characters in the key and the trailing "=" hint at being base64 decoded
binary_output = base64.b64decode(converted_output)

# from 'file' we know this is gzipped
unzipped_output = gzip.decompress(binary_output)

decoded_again = unzipped_output.decode('utf-8')
# more emojis
# this looks like a lot of black and hearts
# zooming out a lot it starts to look like a QR code

# Let's convert that into an image at a size we can actually see
lines = decoded_again.split("\n")
x = len(lines)
y = len(lines[0])

# There are two unicode characters in the data once you get rid of the newlines
# a white and a black heart.  The following code can show that.
#blaa = list()
#for line in lines:
#    chars = list(line)
#    for i in range(len(chars)):
#        if chars[i] not in blaa:
#            blaa.append(chars[i])
#for bla in blaa:
#    print(bla, bla.encode('raw_unicode_escape'))

# Convert hearts into black/white pixels
heart_transform = dict()
heart_transform[b'\U0001F90D'.decode('raw_unicode_escape')] = (255,255,255)
heart_transform[b'\U0001F5A4'.decode('raw_unicode_escape')] = (0,0,0)

pixels = list()
for line in lines:
    if(len(line) > 1):
        tmplist = list()
        chars = list(line)
        for i in range(len(chars)):
            tmplist.append(heart_transform[chars[i]])
        pixels.append(tmplist)

array = np.array(pixels, dtype=np.uint8)
new_image = Image.fromarray(array)

# just in case you want to view the result.
#new_image.save('puzzle-9-qr.png')

result = decode(new_image)
resultdata = result[0].data.decode('utf-8')

# QR code results in the following:
#"Heartbroken? Did you try subtracting your hearbreak [brokenheart emoji]?  [bunch of other emojis]

# (spelling mistake of heartbreak is their's)
# taking the hint, we subtract the broken heart emoji from the others.
heartbroken = "\U0001f494"

my_out = list()
for i in resultdata:
    my_int = ord(i)-ord(heartbroken)
    if(my_int > 0):
        print(i,"-",heartbroken,"=",my_int,"=",chr(my_int))
        my_out.append(chr(my_int))

print(''.join(my_out))








