import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 600]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.scale = 0.002
        self.coords = [37.530887, 55.703118]
        self.map_file = "map.png"
        self.initUI()

    def updateImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?&bbox={self.coords[0] - self.scale},{self.coords[1] - self.scale}~{self.coords[0] + self.scale},{self.coords[1] + self.scale}&l=map"
        # f"http://static-maps.yandex.ru/1.x/?ll={','.join(map(str, self.coords))}&spn={self.scale},{self.scale}&l=map"
        response = requests.get(map_request)
        print(self.scale)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.image.setPixmap(QPixmap(self.map_file))

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 600)
        self.updateImage()

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        # пока не сделано
        if event.key() == Qt.Key_PageUp and self.scale - 0.001 > 0:
            self.scale -= 0.001
            self.updateImage()
        elif event.key() == Qt.Key_PageDown and self.scale + 0.001 <= 90:
            self.scale += 0.001
            self.updateImage()
        elif event.key() == Qt.Key_Up and self.coords[1] + self.scale * 2 < 85:
            self.coords[1] += self.scale * 2
            self.updateImage()
        elif event.key() == Qt.Key_Down and self.coords[1] - self.scale * 2 > -85:
            self.coords[1] -= self.scale * 2
            self.updateImage()
        elif event.key() == Qt.Key_Right and self.coords[0] + self.scale * 2 < 180:
            self.coords[0] += self.scale * 2
            self.updateImage()
        elif event.key() == Qt.Key_Left and self.coords[0] - self.scale * 2 > -180:
            self.coords[0] -= self.scale * 2
            self.updateImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
