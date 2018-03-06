import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtCore import pyqtSlot

class App(QWidget):
    def init(self):
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        print("initUi")
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        button = QPushButton('Image processing', self)
        button.setToolTip('Image processing')
        button.move(0,70)
        self.label = QLabel('Image processing', self)
        self.label.setToolTip('Image processing')
        self.label.move(10,170)
        self.show()

        button.clicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        self.label.setText('Button Clicked')
        self.repaint()

    #loading qt image from opencv image
    def paintImage(self, img):
        height, width, channel = img.shape
        bytesPerLine = 3 * width

        self.label.setPixmap(QPixmap.fromImage(QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)));
        self.label.setFixedWidth(width)
        self.label.setFixedHeight(height)
        self.repaint()
        return

if __name__ == "__main__":
    qtapp = QApplication(sys.argv)
    app = App()
    app.init()
    sys.exit(qtapp.exec_())
