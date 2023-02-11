import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [450, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.zoom = 17
        self.coords = [37.530887, 55.703118]
        self.point = ""  # метка на карте
        self.map_file = "map.png"
        self.map_mode = "map"  # слой
        self.postal_code = False  # нужно ли отображать почтовый индекс
        self.full_address = []  # [полный адрес, почтовый индекс]
        self.initUI()

    def initUI(self):
        self.setFixedSize(*SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.updateImage()
        self.find_object("Москва, Московский Уголовный Розыск Петровки 38")

    def updateImage(self):
        response = requests.get("http://static-maps.yandex.ru/1.x/", params={
            "ll": f"{self.coords[0]},{self.coords[1]}",
            "size": f"{SCREEN_SIZE[0]},{SCREEN_SIZE[1]}",
            "z": self.zoom,
            "l": self.map_mode,
            "pt": self.point
        })

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.image.setPixmap(QPixmap(self.map_file))

    def change_mode(self):
        """Переключение слоев"""  # задача №4
        self.map_mode = ["map", "sat", "sat,skl"][
            (["map", "sat", "sat,skl"].index(self.map_mode) + 1) % 3]
        self.updateImage()

    def find_object(self, address, change_coords=True):
        """Поиск объекта"""  # задача №5, 8 и 9
        answer = requests.get("http://geocode-maps.yandex.ru/1.x/", params={
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": address,
            "format": "json"
        }).json()
        if answer:
            answer = answer["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            if change_coords:
                self.coords = list(map(float, answer["Point"]["pos"].split()))
            self.point = f"{answer['Point']['pos'].replace(' ', ',')},pm2rdm"
            self.full_address = [answer["metaDataProperty"]["GeocoderMetaData"]["text"],
                                 answer["metaDataProperty"]["GeocoderMetaData"][
                                     "Address"].get("postal_code", "отсутствует")]
            self.print_address()
            self.updateImage()

    def clear_point(self):
        """Стирает поставленную метку и адрес"""  # задача №7
        self.point = ""
        self.full_address = []
        self.updateImage()

    def print_address(self):  # для задачи №9
        if self.full_address:
            print(self.full_address[0] + (f", почтовый индекс: {self.full_address[1]}"
                                          if self.postal_code else ""))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.zoom + 1 < 22:
            self.zoom += 1
            self.updateImage()
        elif event.key() == Qt.Key_PageDown and self.zoom - 1 >= 0:
            self.zoom -= 1
            self.updateImage()
        # пока не сделано (из задачи №3)
        # elif event.key() == Qt.Key_Up and self.coords[1] < 85:
        #     self.coords[1] += self.scale
        #     self.updateImage()
        # elif event.key() == Qt.Key_Down and self.coords[1] > -85:
        #     self.coords[1] -= self.scale
        #     self.updateImage()
        # elif event.key() == Qt.Key_Right and self.coords[0] < 180:
        #     self.coords[0] += self.scale
        #     self.updateImage()
        # elif event.key() == Qt.Key_Left and self.coords[0] > -180:
        #     self.coords[0] -= self.scalef
        #     self.updateImage()
        elif event.key() in (81, 1049):  # Q, Й
            self.change_mode()
        elif event.key() in (67, 1057):  # C, С
            self.clear_point()
        elif event.key() in (70, 1040):  # F, А
            self.postal_code = not self.postal_code
            self.print_address()

    def mousePressEvent(self, event):  # задача №11, пока не сделано
        if event.button() == Qt.LeftButton:
            print(1)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
