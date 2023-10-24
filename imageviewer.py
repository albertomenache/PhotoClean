#!/usr/bin/env python

from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5 import QtCore, QtWidgets
from PIL import Image
from cleaner import processImage, PIL_to_qimage 

class ImageViewer:
    def __init__(self, qlabel):
        self.qlabel_image = qlabel 
        self.qimage_scaled = QImage()
        self.qpixmap = QPixmap()            
        self.position = [0, 0]
        self.prevImagePath = ""
        self.prevImage = None
        self.qlabel_image.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

    def onResize(self):
        ''' things to do when qlabel_image is resized '''
        self.qpixmap = QPixmap(self.qlabel_image.size())
        self.qpixmap.fill(QtCore.Qt.darkGray)
        self.qimage_scaled = self.qimage.scaled(self.qlabel_image.width(), self.qlabel_image.height(), QtCore.Qt.KeepAspectRatio)
        self.update()

    def loadImage(self, imagePath, valid=True, feather=0):
        ''' To load and display new image.'''      
        result = None
        
        if not self.prevImagePath == imagePath or self.qimage is None:
            if not valid:
                try:
                    pil_img = Image.open(imagePath)
                except Exception as e:
                    return
                self.qimage = PIL_to_qimage(pil_img)
            else:
                self.qimage = QImage(imagePath)
            
            self.qpixmap = QPixmap(self.qlabel_image.size())
            self.prevImage = None
            
        self.prevImagePath = imagePath
        
        if not self.qimage.isNull():
            self.position = [0, 0]
            self.qimage_scaled = self.qimage.scaled(self.qlabel_image.width(), self.qlabel_image.height(), QtCore.Qt.KeepAspectRatio)
            self.update()
            img, result = processImage(imagePath, valid, feather, self.prevImage)
            self.prevImage = img
        else:
            self.statusbar.showMessage('Cannot open this image! Try another one.', 5000)
            
        return result
            
    def showImage(self, img):
        ''' Display result image '''
                
        if img is None:
            return
        
        qimg_format = QImage.Format.Format_RGB888 if len(img.shape) == 3 else QImage.Format.Format_Indexed8
        height = img.shape[0]
        width = img.shape[1]

        if len(img.shape) == 3:
            bytesPerLine = 3 * width
        else:
            bytesPerLine = width

        try:
            self.qimage = QImage(img.data, width, height, bytesPerLine, qimg_format)
        except Exception as e:
            pass
        
        self.qimage = self.qimage.rgbSwapped()
        self.qpixmap = QPixmap(self.qlabel_image.size())
        if not self.qimage.isNull():
            self.zoomX = 1
            self.position = [0, 0]
            self.qimage_scaled = self.qimage.scaled(self.qlabel_image.width(), self.qlabel_image.height(), QtCore.Qt.KeepAspectRatio)
            self.update()
        else:
            self.statusbar.showMessage('Cannot process this image! Try another one.', 5000)
        
    def update(self):
        if not self.qimage_scaled.isNull():
            imW = self.qimage_scaled.width()
            imH = self.qimage_scaled.height()
            lbW = self.qlabel_image.width()
            lbH = self.qlabel_image.height()
            px, py = self.position
            px = px if (px <= self.qimage_scaled.width() - self.qlabel_image.width()) else (self.qimage_scaled.width() - self.qlabel_image.width())
            py = py if (py <= self.qimage_scaled.height() - self.qlabel_image.height()) else (self.qimage_scaled.height() - self.qlabel_image.height())
            px = px if (px >= 0) else 0
            py = py if (py >= 0) else 0
            
            self.position = (px, py)

            if lbW > imW:
                px = int((float)(lbW - imW) / 2.0)
            if lbH > imH:
                py = int((float)(lbH - imH) / 2.0)
            
            self.qpixmap.fill(QtCore.Qt.darkGray)

            painter = QPainter()
            painter.begin(self.qpixmap)
            painter.drawImage(QtCore.QPoint(px, py), self.qimage_scaled,
                    QtCore.QRect(self.position[0], self.position[1], self.qlabel_image.width(), self.qlabel_image.height()) )
            painter.end()

            self.qlabel_image.setPixmap(self.qpixmap)
        else:
            pass
