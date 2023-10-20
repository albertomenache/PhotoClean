from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5 import QtCore, QtWidgets
import cv2
import numpy as np

class ImageViewer:
    def __init__(self, qlabel):
        self.qlabel_image = qlabel 
        self.qimage_scaled = QImage()
        self.qpixmap = QPixmap()

        self.zoomX = 1              # zoom factor w.r.t size of qlabel_image
        self.position = [0, 0]      # position of top left corner of qimage_label w.r.t. qimage_scaled
        self.panFlag = False        # to enable or disable pan

        self.qlabel_image.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

    '''def __connectEvents(self):
        # Mouse events
        self.qlabel_image.mousePressEvent = self.mousePressAction
        self.qlabel_image.mouseMoveEvent = self.mouseMoveAction
        self.qlabel_image.mouseReleaseEvent = self.mouseReleaseAction'''

    def onResize(self):
        ''' things to do when qlabel_image is resized '''
        self.qpixmap = QPixmap(self.qlabel_image.size())
        self.qpixmap.fill(QtCore.Qt.darkGray)
        self.qimage_scaled = self.qimage.scaled(self.qlabel_image.width() * self.zoomX, self.qlabel_image.height() * self.zoomX, QtCore.Qt.KeepAspectRatio)
        self.update()

    def loadImage(self, imagePath):
        ''' To load and display new image.'''
        result = None
        self.qimage = QImage(imagePath)
        self.qpixmap = QPixmap(self.qlabel_image.size())
        if not self.qimage.isNull():
            self.zoomX = 1
            self.position = [0, 0]
            self.qimage_scaled = self.qimage.scaled(self.qlabel_image.width(), self.qlabel_image.height(), QtCore.Qt.KeepAspectRatio)
            self.update()
            result = self.processImage(imagePath)
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
        self.qimage = QImage(img.data, width, height, bytesPerLine, qimg_format)
        self.qimage = self.qimage.rgbSwapped()
        self.qpixmap = QPixmap(self.qlabel_image.size())
        if not self.qimage.isNull():
            self.zoomX = 1
            self.position = [0, 0]
            self.qimage_scaled = self.qimage.scaled(self.qlabel_image.width(), self.qlabel_image.height(), QtCore.Qt.KeepAspectRatio)
            self.update()
        else:
            self.statusbar.showMessage('Cannot process this image! Try another one.', 5000)        
    
    def processImage(self, imagePath):
        img = cv2.imread(filename=imagePath)
        height, width = img.shape[0], img.shape[1]
        
        '''cv2.imshow('Blue', B)
        cv2.imshow('Green', G)
        cv2.imshow('Red', R)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''
        
        imgLarge = cv2.resize(img, None, fx = 2.0, fy = 2.0)
        #(gray, G, R) = cv2.split(imgLarge)
        mask = np.zeros((height*2, width*2, 1), np.uint8)
        gray = cv2.cvtColor(imgLarge, cv2.COLOR_BGR2GRAY)
        
        #gray, _G, _R = cv2.split(imgLarge)
        
        
        #ret,img2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        print (height, width)
        
        '''cv2.imshow('Grey', gray)
        cv2.imshow('dst', img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''
        
        if height > width:
            minLen = width * 2
            maxLen = height * 2
        else:
            minLen = height * 2
            maxLen = width * 2
            
        print (minLen)

        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=minLen-10, maxLineGap=50)
        #lines = cv2.HoughLinesP(edges, rho=0.02, theta=np.pi / 500,     threshold=10, minLineLength=minLen-10, maxLineGap=50)
        lineWidth = 20
        
        v = []
        h = []
        if lines is not None:
            for line in lines:
                if (line[0][0] == line[0][2]):
                    v.append(line[0][0])
                if (line[0][1] == line[0][3]):
                    h.append(line[0][1])
            if len(h) > 1:
                lineWidth = max(h)-min(h)
            if len(v) > 1:
                lineWidth = max(v)-min(v)

            for line in lines:
                #cv2.line(mask, (line[0][0]+lineWidth, maxLen), (line[0][2]+lineWidth, 0), 255, lineWidth*4, cv2.FILLED)
                if (line[0][0] == line[0][2]):
                    #cv2.line(mask, (line[0][0], int(maxLen/2)), (line[0][2], 0), 255, lineWidth, cv2.LINE_8)
                    cv2.line(mask, (line[0][0], maxLen), (line[0][2], 0), 255, lineWidth, cv2.LINE_8)
                    #cv2.line(mask, (line[0][0]-int(lineWidth), int(maxLen/2)), (line[0][2]-int(lineWidth), 0), 255, 2, cv2.LINE_8)
                    #cv2.line(mask, (line[0][0]-int(lineWidth), int(maxLen/2)), (line[0][2]-int(lineWidth), 0), 255, lineWidth*4, cv2.LINE_8)
                    #cv2.line(mask, (line[0][0]+int(lineWidth/2), int(maxLen/2)), (line[0][2]+int(lineWidth/2), 0), 255, lineWidth*4, cv2.LINE_8)
                    #cv2.line(imgLarge, (line[0][0]-int(lineWidth), maxLen), (line[0][2]-int(lineWidth), int(maxLen/2)), (0, 0, 0), 2, cv2.LINE_8)
                if (line[0][1] == line[0][3]):
                    cv2.line(mask, (maxLen, line[0][1]), (0, line[0][3]), 255, 14, cv2.FILLED)
                    #cv2.line(imgLarge, (maxLen, line[0][1]), (0, line[0][3]), (0, 0, 0), 14, cv2.FILLED)
                    
        print (v)
        #lineWidth = max(v)-min(v)
        print (lineWidth)

        mask = cv2.resize(mask, None, fx = 0.5, fy = 0.5)
        #imgLarge = cv2.resize(imgLarge, None, fx = 0.5, fy = 0.5)
        
        '''cv2.imshow('dst', mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''
        
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        output = cv2.inpaint(img, mask, lineWidth, flags=cv2.INPAINT_TELEA)
        #output = cv2.inpaint(output, mask, lineWidth*4, flags=cv2.INPAINT_TELEA)
        #output = cv2.inpaint(output, mask, 3, flags=cv2.INPAINT_TELEA)
        '''for i in range(height):
            for j in range(width):
                if mask[i, j].sum() > 0:
                    mask[i, j] = 0
                else:
                    mask[i, j] = 255 '''       
        #mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        #output = img + mask
        return output

        
    def update(self):
        ''' This function actually draws the scaled image to the qlabel_image.
            It will be repeatedly called when zooming or panning.
            So, I tried to include only the necessary operations required just for these tasks. 
        '''
        if not self.qimage_scaled.isNull():
            # check if position is within limits to prevent unbounded panning.
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
            
            if self.zoomX == 1:
                self.qpixmap.fill(QtCore.Qt.darkGray)

            # the act of painting the qpixamp
            painter = QPainter()
            painter.begin(self.qpixmap)
            painter.drawImage(QtCore.QPoint(px, py), self.qimage_scaled,
                    QtCore.QRect(self.position[0], self.position[1], self.qlabel_image.width(), self.qlabel_image.height()) )
            painter.end()

            self.qlabel_image.setPixmap(self.qpixmap)
        else:
            pass

    def mousePressAction(self, QMouseEvent):
        x, y = QMouseEvent.pos().x(), QMouseEvent.pos().y()
        #print(x,y)
        if self.panFlag:
            self.pressed = QMouseEvent.pos()    # starting point of drag vector
            self.anchor = self.position         # save the pan position when panning starts

    def mouseMoveAction(self, QMouseEvent):
        x, y = QMouseEvent.pos().x(), QMouseEvent.pos().y()
        if self.pressed:
            dx, dy = x - self.pressed.x(), y - self.pressed.y()         # calculate the drag vector
            self.position = self.anchor[0] - dx, self.anchor[1] - dy    # update pan position using drag vector
            self.update()                                               # show the image with udated pan position

    def mouseReleaseAction(self, QMouseEvent):
        self.pressed = None                                             # clear the starting point of drag vector
        
    def enablePan(self, value):
        self.panFlag = value

