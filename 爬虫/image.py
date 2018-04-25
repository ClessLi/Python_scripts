#!/home/cless/python2.7/bin/python2.7
# encoding:utf-8

from PIL import Image
#from matplotlib import pyplot as plt


def show(file_path):
    with Image.open(file_path) as img:
        img.show()
        #plt.imshow(img)

if __name__ == '__main__':
    show('test.jpg')
