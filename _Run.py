import sys

import cv2
import numpy as np

from os import path
sys.path.append( path.dirname( path.abspath(__file__) ) )

from ConsoleColor import print, console
from pathlib import *

main=sys.argv.pop(0)
sizeW=1080

def print_skip(file):
    print("[yellow]skip[/yellow]",file)
def print_ok(file):
    print("[green]ok[/green]",file)

def resize(file):
    #print(file)
    #file=Path(file)
    #print(file)
    img_array = np.fromfile(file, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    h, w, c = img.shape
    #print("w: " + str(w) + ", h: " + str(h) + ", channel: " + str(c))
    edit=False
    
    if w>h:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        h, w, c = img.shape
        #print("w: " + str(w) + ", h: " + str(h) + ", channel: " + str(c))
        edit=True
        
    if w>sizeW:
        img = cv2.resize(img, tuple([sizeW,int(h*sizeW/w)]), interpolation=cv2.INTER_AREA)
        h, w, c = img.shape
        #print("w: " + str(w) + ", h: " + str(h) + ", channel: " + str(c))
        edit=True
    
    #cv2.imshow('src', src[int(500/(1920/y)):int(900/(1920/y)), int(400/(1280/x)):int(800/(1280/x))])
    #cv2.imshow('INTER_AREA', INTER_AREA[500:900, 400:800])
    #cv2.imshow('show', img)
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    
    if not edit:
        print_skip(file)
        #return
    
    result, encoded_img = cv2.imencode(".jpg", img)
    if result:
        Path( file.parent,'_result').mkdir(parents=True,exist_ok=True)
        print(file.name)
        with open(Path( file.parent,'_result',file.with_suffix(".jpg").name), mode='w+b') as f:
            encoded_img.tofile(f)
            print_ok(file)

#print(sys.argv)
for i in sys.argv:
    i=Path(i)
    if '_result' in i.parts:
        print_skip(i)
        continue
    elif i.is_dir():
        for f in i.glob("**/*.*"):
            f=Path(f)
            if '_result' in f.parts:
                print_skip(f)
                continue
            resize(f)
    else:
        resize(i)




