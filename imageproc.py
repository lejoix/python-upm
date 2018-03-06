import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QImage, QPixmap

class ImageProcessing:
    cv = cv2
    def __init__(self):
        self.cv = cv2
        return

    def rotate(self, image, rotation):
        rows,cols,ch = image.shape
        M = self.cv.getRotationMatrix2D((cols/2, rows/2), rotation, 1)
        dest = self.cv.warpAffine(image, M, (cols, rows))

        return dest

    def gradient(self, img):
        laplacian = self.cv.Laplacian(img,cv2.CV_64F)
        sobelx = self.cv.Sobel(img,cv2.CV_64F,1,0, 5)
        sobely = self.cv.Sobel(img,cv2.CV_64F,0,1, 5)

        plt.subplot(2,2,1),plt.imshow(img, 'gray')
        plt.title('Original'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,2,2),plt.imshow(laplacian, 'gray')
        plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,2,3),plt.imshow(sobelx, 'gray')
        plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,2,4),plt.imshow(sobely, 'gray')
        plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])
        plt.show()

    def loadImage(self, img):
        return self.cv.imread(img, 1)

    def saveImage(self, img, path):
        self.cv.imwrite(path, img)


def mainLoop():
    # Load an color image in grayscale
    imgproc = ImageProcessing()
    dst = imgproc.loadImage('lena.png')
    imgproc.cv.imshow('image', dst)

    k = 0

    #loop wait for keys
    while k != 27:
        k = imgproc.cv.waitKey(0)
        #rotate right
        if k == ord('r'):
            dst = imgproc.rotate(dst, -90)
            imgproc.cv.imshow('image', dst)
        #rotateleft
        elif k == ord('l'):
            dst = imgproc.rotate(dst, +90)
            imgproc.cv.imshow('image', dst)
        #showgradient
        elif k == ord('g'):
            imgproc.gradient(dst)
            imgproc.cv.imshow('image', dst)
        #save transformed image
        elif k == ord('s'): # wait for 's' key to save and exit
            imgproc.saveImage(dst, 'image.png')
            k = 27

    #exit
    imgproc.cv.destroyAllWindows()
    sys.exit(1)

if __name__ == "__main__":
    mainLoop()
