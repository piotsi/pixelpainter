import sys
import numpy as np
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QCursor, QMouseEvent
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QStyleFactory,
    QGroupBox,
    QRadioButton,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paint")
        self.windowSizex, self.windowSizey = 700, 520
        self.toolbarHeight = 40
        self.pixelSize = 10
        self.setStyleSheet("background-color: white;")
        self.xPixelSize = int(self.windowSizex / self.pixelSize)
        self.yPixelSize = int((self.windowSizey - self.toolbarHeight) / self.pixelSize)
        self.setFixedSize(self.windowSizex, self.windowSizey)
        QApplication.setStyle(QStyleFactory.create("Fusion"))

        self.last_pos = None

        self.canvasR = np.full((self.xPixelSize, self.yPixelSize), 255)
        self.canvasG = np.full((self.xPixelSize, self.yPixelSize), 255)
        self.canvasB = np.full((self.xPixelSize, self.yPixelSize), 255)

        self.r = 255
        self.g = 255
        self.b = 255

        # TODO: add new widgets here

        self.mousePosLabel = QLabel(self)
        self.mousePosLabel.resize(self.windowSizex / 2, self.toolbarHeight)
        self.mousePosLabel.setAlignment(Qt.AlignCenter)
        self.mousePosLabel.setStyleSheet(
            "background-color: rgb({}, {}, {}); font-size: 20px".format(255, 255, 255)
        )

        self.colorPalleteLabel = QLabel(self)
        self.colorPalleteLabel.resize(self.windowSizex / 2, self.toolbarHeight)
        self.colorPalleteLabel.move(self.windowSizex / 2, 0)
        self.colorPalleteLabel.setAlignment(Qt.AlignCenter)
        self.colorPalleteLabel.setStyleSheet(
            "background-color: rgb({}, {}, {}); font-size: 20px".format(
                self.r, self.g, self.b
            )
        )
        self.colorPalleteLabel.setText("Color Pallette")

        self.show()
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        for y in range(self.yPixelSize):
            for x in range(self.xPixelSize):
                painter.setBrush(
                    QColor(self.canvasR[x, y], self.canvasG[x, y], self.canvasB[x, y])
                )
                painter.setPen(Qt.NoPen)
                painter.drawRect(
                    x * self.pixelSize,
                    (y + int(self.toolbarHeight / self.pixelSize)) * self.pixelSize,
                    self.pixelSize,
                    self.pixelSize,
                )

    def mouseMoveEvent(self, event):
        self.current_pos = event.pos()
        self.mousePosLabel.setText(
            "{0}, {1}".format(self.current_pos.x(), self.current_pos.y())
        )
        if event.button() == Qt.LeftButton:
            print("clck")
            relativeX = int(self.current_pos.x() / self.pixelSize)
            relativeY = int(
                (self.current_pos.y() - self.toolbarHeight) / self.pixelSize
            )
            self.canvasR[relativeX, relativeY] = self.r
            self.canvasG[relativeX, relativeY] = self.g
            self.canvasB[relativeX, relativeY] = self.b
            self.repaint()

    def mousePressEvent(self, event):
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R and self.r != 0:
            self.r -= 5
        elif event.key() == Qt.Key_T and self.r != 255:
            self.r += 5
        elif event.key() == Qt.Key_G and self.g != 0:
            self.g -= 5
        elif event.key() == Qt.Key_H and self.g != 255:
            self.g += 5
        elif event.key() == Qt.Key_B and self.b != 0:
            self.b -= 5
        elif event.key() == Qt.Key_N and self.b != 255:
            self.b += 5
        elif event.key() == Qt.Key_K:
            self.r = self.g = self.b = 0
        elif event.key() == Qt.Key_W:
            self.r = self.g = self.b = 255
        elif event.key() == Qt.Key_C:
            self.canvasR = np.full((self.xPixelSize, self.yPixelSize), 255)
            self.canvasG = np.full((self.xPixelSize, self.yPixelSize), 255)
            self.canvasB = np.full((self.xPixelSize, self.yPixelSize), 255)
            self.repaint()

        self.colorPalleteLabel.setStyleSheet(
            "background-color: rgb({}, {}, {}); font-size: 20px".format(
                self.r, self.g, self.b
            )
        )


if __name__ == "__main__":
    window = QApplication(sys.argv)
    app = App()
    sys.exit(window.exec_())
