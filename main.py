import os
import sys
from PyQt5.QtCore import Qt
from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PIL import Image
import requests
from useful.geocoder import geocode


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)

        API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'
        coords = '134.854,-25.828'
        toponym = geocode(coords)
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        self.prev = 125
        self.map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": '6.25,6.25',
            "l": "map",
            'pt': ",".join([toponym_longitude, toponym_lattitude])
        }
        self.image(self.map_params)
        self.sizeSlider.valueChanged[int].connect(self.changeSize)

    def changeSize(self, value):
        a, b = [float(x) for x in self.map_params.get('spn').split(',')]
        if 0.05 <= a <= 20 and 0.05 <= b <= 20:
            a = value * 0.05
            b = value * 0.05
        self.prev = value
        self.map_params['spn'] = ','.join([str(x) for x in [a, b]])
        self.image(self.map_params)

    def image(self, map_params):
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.show_image()

    def show_image(self):
        self.pixmap = QPixmap(self.map_file)
        self.mapField.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.changeSize(self.prev - 1)
        elif event.key() == Qt.Key_PageUp:
            self.changeSize(self.prev + 1)

    # code

    def closeEvent(self, event):
        os.remove(self.map_file)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec_())
