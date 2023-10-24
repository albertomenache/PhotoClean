#!/usr/bin/env python

''' A basic GUi to use ImageViewer class to show its functionalities and use cases. '''

from PyQt5 import uic, QtWidgets
from imageviewer import ImageViewer
from cleaner import processImage
from PIL import Image
import sys, os
import style
import cv2
from pillow_heif import register_heif_opener

gui = uic.loadUiType("main.ui")[0]     # load UI file designed in Qt Designer
VALID_FORMAT = ('.BMP', '.GIF', '.JPG', '.JPEG', '.PNG', '.PBM', '.PGM', '.PPM', '.TIFF', '.XBM')  # Image formats supported by Qt
OTHER_FORMAT = ('.HEIC')

def getImages(folder):
    ''' Get the names and paths of all the images in a directory. '''
    image_list = []
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if file.upper().endswith(VALID_FORMAT):
                im_path = os.path.join(folder, file)
                image_obj = {'name': file, 'path': im_path, 'valid': True, 'result': None }
                image_list.append(image_obj)
            elif file.upper().endswith(OTHER_FORMAT):
                im_path = os.path.join(folder, file)
                image_obj = {'name': file, 'path': im_path, 'valid': False, 'result': None }
                image_list.append(image_obj)
                
    return image_list

class Iwindow(QtWidgets.QMainWindow, gui):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        register_heif_opener()
        self.feather = []

        self.cntr, self.numImages = -1, -1  # self.cntr have the info of which image is selected/displayed

        self.image_viewer = ImageViewer(self.qlabel_image)
        self.result_viewer = ImageViewer(self.qlabel_result)
        self.__connectEvents()
        self.showMaximized()

    def __connectEvents(self):
        self.open_folder.clicked.connect(self.selectDir)
        self.next_im.clicked.connect(self.nextImg)
        self.prev_im.clicked.connect(self.prevImg)
        self.save_im.clicked.connect(self.saveImg)
        self.feather_sb.valueChanged.connect(self.featherChanged)
        self.process_all.clicked.connect(self.processAll)
        self.qlist_images.itemClicked.connect(self.item_click)
        
    def startProcess(self, cntr):
        self.feather_sb.blockSignals(True)
        self.feather_sb.setValue(self.feather[cntr])
        self.feather_sb.blockSignals(False)
        self.items[cntr].setSelected(True)
        result = self.image_viewer.loadImage(self.logs[cntr]['path'], self.logs[cntr]['valid'], self.feather[cntr])
        if result is not None:
            self.result_viewer.showImage(result)
            self.logs[cntr]['result'] = result

    def selectDir(self):
        ''' Select a directory, make list of images in it and display the first image in the list. '''
        # open 'select folder' dialog box
        self.folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if not self.folder:
            QtWidgets.QMessageBox.warning(self, 'No Folder Selected', 'Please select a valid Folder')
            return
        
        images = getImages(self.folder)
        if len(images) > 0:
            self.logs = images.copy()
            self.numImages = len(self.logs)
            self.feather = [0] * self.numImages
            imageFolder = os.path.dirname(images[0]['path'])
            self.resultFolder = os.path.abspath(os.path.join(imageFolder, "result"))

            # make qitems of the image names
            self.items = [QtWidgets.QListWidgetItem(log['name']) for log in self.logs]
            self.qlist_images.clear()
            for item in self.items:
                self.qlist_images.addItem(item)
    
            # display first image and enable Pan 
            self.cntr = 0
            self.startProcess(self.cntr)
        
            # enable the next image button on the gui if multiple images are loaded
            if self.numImages > 1:
                self.next_im.setEnabled(True)

    def resizeEvent(self, _evt):
        if self.cntr >= 0:
            self.image_viewer.onResize()
            self.result_viewer.onResize()
            
    def featherChanged(self):
        if self.cntr >= 0:
            self.feather[self.cntr] = self.feather_sb.value()
            self.startProcess(self.cntr)

    def nextImg(self):
        if self.cntr < self.numImages -1:
            self.cntr += 1
            self.startProcess(self.cntr)
        else:
            QtWidgets.QMessageBox.warning(self, 'Sorry', 'No more Images!')

    def prevImg(self):
        if self.cntr > 0:
            self.cntr -= 1
            self.startProcess(self.cntr)
        else:
            QtWidgets.QMessageBox.warning(self, 'Sorry', 'No previous Image!')
            
    def saveImg(self):
        self.saveResult(self.cntr)
        
    def saveResult(self, idx):
        if self.logs[idx]['result'] is None:
            QtWidgets.QMessageBox.warning(self, 'Sorry', 'No Image to Save!')
            return 
        
        if not os.path.exists(self.resultFolder):
            try:
                os.makedirs(self.resultFolder) 
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, 'Sorry', "Failed to create folder %r.\n%s" %(self.resultFolder, e))
                return
            print("Directory '% s' created" % self.resultFolder)
        
        savedPath = os.path.join(self.resultFolder, os.path.split(self.logs[idx]['path'])[1])
        if os.path.isfile(savedPath):
            os.remove(savedPath)
            
        if not self.logs[idx]['valid']:
            pil_img = Image.fromarray(self.logs[idx]['result']) 
            pil_img.save(savedPath)
        else:
            cv2.imwrite(savedPath, self.logs[idx]['result'])    
        
    def processAll(self):
        for i in range(self.numImages):
            result = processImage(self.logs[i]['path'])
            if result is not None:
                self.logs[i]['result'] = result
                self.saveResult(i)         
    
    def item_click(self, item):
        self.cntr = self.items.index(item)
        self.startProcess(self.cntr)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(style.style)
    app.setPalette(QtWidgets.QApplication.style().standardPalette())
    _parentWindow = Iwindow(None)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()