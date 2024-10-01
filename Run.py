import sys
import cv2
import numpy as np

from multiprocessing import Pool
from multiprocessing import Process

from os import path
sys.path.append( path.dirname( path.abspath(__file__) ) )

from ConsoleColor import print, console
from pathlib import *

sizeW=1080

def print_skip(file,sz1=1,sz2=0):
    #print("[yellow]skip[/yellow]",file)
    return f"[yellow]skip[/yellow] {file} {int(sz1/1024)} {int(sz2/1024)} {int((sz1-sz2)/1024)}"
def print_ok(file,sz1=1,sz2=0):
    #print("[green]ok[/green]",file)
    return f"[green]ok[/green] {file} {int(sz1/1024)} {int(sz2/1024)} {int((sz1-sz2)/1024)}"
def print_fail(file):
    #print("[green]ok[/green]",file)
    return f"[red]fail[/red] {file}"

def resize(file):
    #print(file)
    #file=Path(file)
    #print(file)
    img_array = np.fromfile(file, np.uint8)
    #print(type(img_array))
    sz1=img_array.size
    #print(sz1)
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
    
    #if not edit:
    #    return print_skip(file)
        #return
    
    #result, encoded_img = cv2.imencode(".jpg", img)
    result, encoded_img = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    #print(type(encoded_img))
    Path( file.parent,'_result').mkdir(parents=True,exist_ok=True)
    if result:
        
        sz2=encoded_img.size
        #print(sz2)
        if sz1>sz2:
            with open(Path( file.parent,'_result',file.with_suffix(".jpg").name), mode='w+b') as f:
                encoded_img.tofile(f)
            return print_ok(file,sz1,sz2)            
        else:
            with open(Path( file.parent,'_result',file.name), mode='w+b') as f:
                img_array.tofile(f)
            return print_skip(file,sz1,sz2)
    else:
        with open(Path( file.parent,'_result',file.name), mode='w+b') as f:
            img_array.tofile(f)
        return print_fail(file)
        
    
def testf(x):
    return x*x
            
if __name__ == '__main__':

    main=sys.argv.pop(0)
    
    #print(sys.argv)
    ar=[]
    result=[]
    for i in sys.argv:
        i=Path(i)
        if '_result' in i.parts:
            #result.append(print_skip(i))
            print_skip(i)
            continue
        elif i.is_dir():
            for f in i.glob("**/*.*"):
                f=Path(f)
                if '_result' in f.parts:
                    #result.append(print_skip(f))
                    print_skip(f)
                    continue
                #resize(f)
                ar.append(f)
        else:
            #resize(i)
            ar.append(i)
    
    #print(ar)
    with Pool() as p:
        #p.map(print_ok, ar)
        result+=p.map(resize, ar)
    for i in result:
        print(i)
        
        
    #data = [1, 2, 3, 4, 5]
    #
    #with Pool(5) as p:
    #    print(p.map(testf, [1, 2, 3]))

