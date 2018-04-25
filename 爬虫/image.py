#!/home/cless/python2.7/bin/python2.7
# encoding:utf-8

from PIL import Image
## Installation for Opencv-python: 'python -m pip install opencv-python'
import cv2

def show(file_path):
    with Image.open(file_path) as img:
        #img.show()
        cv2.imshow(img)

if __name__ == '__main__':
    show('test.bmp')
