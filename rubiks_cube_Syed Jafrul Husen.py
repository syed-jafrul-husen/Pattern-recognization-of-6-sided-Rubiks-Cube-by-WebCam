#import time
from collections import defaultdict 
import tkinter
from tkinter import *
window = tkinter.Tk()
import time
from tkinter.font import Font
from PIL import Image, ImageTk

from PIL import ImageTk, Image
from tkinter import filedialog


from pathlib import Path
from skimage.io import imread
from skimage.transform import resize
import matplotlib.pyplot as plt
import cv2
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
from PIL import Image
import sys
from skimage.io import imread, imshow
from skimage.color import rgb2gray,gray2rgb,rgb2hsv
from skimage.util import img_as_float64
#from skimage import data, color
from skimage.transform import  resize






window.title("Rubik Cube 6 sides pattern recognization!!")
window.geometry("1000x600")
window.configure(bg='cyan')

f1 = Font(family="Blackadder ITC",size=30)
Label(window,text='Rubik Cube 6 sides pattern recognization',fg='black',bg='cyan',font=f1).pack(side=TOP)




c = Canvas(window,height=1100,width=680,bg='gray')
c.pack(expand=YES, fill=BOTH)



window.resizable(width=True, height=True)



sequence = ['Front','Left','Right','Top','Down','Back']


def image_read(img_counter):
    cam = cv2.VideoCapture(0)
    s = "Capture {} side of the rubik cube...."+sequence[img_counter] 
    cv2.namedWindow(s)     
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Capture Image", frame)    
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "rubik_cube_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            cam.release()
            cv2.destroyAllWindows()        
            break        
    cam.release()
    cv2.destroyAllWindows()
    return img_name

six_image_crop = []
six_path = []

for i in range(6):
    title = "select only rubik cube to crop...." 
    #boolean indicating whether cropping is being performed or not
    refPt = []
    cropping = False
    def click_and_crop(event, x, y, flags, param):
        global refPt, cropping
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            cropping = True
        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
             #(x, y) coordinates and indicate that, the cropping operation is finished
            refPt.append((x, y))
            cropping = False
            # draw a rectangle
            cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
            cv2.imshow("image", image)
    path = image_read(i)
    # load the image, clone it, and setup the mouse callback function
    image = cv2.imread(path)
    clone = image.copy()
    cv2.namedWindow(title)
    cv2.setMouseCallback(title, click_and_crop)
    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow(title, image)
        key = cv2.waitKey(1) & 0xFF
        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = clone.copy()
        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            cv2.destroyAllWindows()
            break
    # if there are two reference points, then crop the region of interest
    # from teh image and display it
    if len(refPt) == 2:
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        #cv2.imshow("ROI", roi)
        img_name2 = "crop_rubik_cube_{}.jpg".format(i)
        six_path.append(img_name2)
        cv2.imwrite(img_name2, roi)
        cv2.waitKey(0)
    # close all open windows
    cv2.destroyAllWindows()





def extended_SLIC_solution():
    result = []
    arr = []
    for src in range(6):
        img = cv2.imread(six_path[src])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        img = resize(img, (400,400),anti_aliasing=True)
        imshow(img)
        
        r = (int)(img.shape[0]/3)
        c = (int)(img.shape[1]/3)
        print(r,c)
        
        
        ans = []
        img  = rgb2hsv(img)
        for i in range(1,4,1):
            for j in range(1,4,1):
                x = (int)(r*i-(r/2))
                y = (int)(c*j-(c/2))
                cnt = 0
                for t in range(-10,10,1):
                    for t2 in range(-10,10,1):
                        cnt = cnt + img[x+t,y+t2,0]
                       
                cnt = (int)((cnt/400)*1000)
                ans.append(cnt)
                arr.append(cnt)
        
        result.append(ans)
        #imshow(img)
    #imshow(img)
    arr.sort()
    for i in range(6):
        for j in range(9):
            if result[i][j]>=arr[0] and result[i][j]<=arr[8]:
                result[i][j] = 0
            elif result[i][j]>=arr[9] and result[i][j]<=arr[17]:
                result[i][j] = 1
            elif result[i][j]>=arr[18] and result[i][j]<=arr[26]:
                result[i][j] = 2
            elif result[i][j]>=arr[27] and result[i][j]<=arr[35]:
                result[i][j] = 3
            elif result[i][j]>=arr[36] and result[i][j]<=arr[44]:
                result[i][j] = 4
            elif result[i][j]>=arr[45] and result[i][j]<=arr[53]:
                result[i][j] = 5
    for i in range(6):
        print(sequence[i])
        print(result[i][0],result[i][1],result[i][2])
        print(result[i][3],result[i][4],result[i][5])
        print(result[i][6],result[i][7],result[i][8])
        print()
    return result


def solution():
    c2 = 4
    result = extended_SLIC_solution()
    for i in range(9):
        cnt = -1
        for j in range(3):
            for k in range(3):
                cnt = cnt+1
                if result[i][cnt]==0:
                    color = 'blue'
                elif result[i][cnt]==1:
                    color = 'yellow'
                elif result[i][cnt]==2:
                    color = 'orange'
                elif result[i][cnt]==3:
                    color = 'white'
                elif result[i][cnt]==4:
                    color = 'green'
                else:
                    color = 'red'
                
                algorithm = Label(c, text='       X    ',bg=color).grid(row=c2,column=k+4)
                #print(c2,k+4)
            c2 = c2 + 1
        #c2 = c2+1
        algorithm = Label(c, text='         ',bg='gray').grid(row=c2,column=6) 
        c2 = c2 + 1
        

    

algorithm = Label(c, text='                   ', fg='black', bg='deep sky blue',font='bold').grid(row=1,column=0)
algorithm = Label(c, text='                  ', fg='black', bg='deep sky blue',font='bold').grid(row=1,column=2)


result = tkinter.Button(c, text='solution',font='bold',bg='sky blue',activebackground='cyan', command=solution).grid(row=1,column=1)

window.mainloop()