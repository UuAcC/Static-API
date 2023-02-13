import os
import sys
from io import BytesIO

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
        self.coords = '134.854,-25.828'
        self.map_find(self.coords)
        self.show_image()

        self.sizeSlider.valueChanged[int].connect(self.changeSize)
        
    def map_find(self, coords, size='5,5'):
        toponym = geocode(coords)
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        self.map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": size,
            "l": "map",
            'pt': ",".join([toponym_longitude, toponym_lattitude])
        }
        self.image(self.map_params)

    def changeSize(self, value):
        frame = [float(x) for x in self.map_params.get('spn').split(',')]
        for i in frame:
            i -= float(value) * 10
        self.map_params['spn'] = ','.join([str(x) for x in frame])
        self.map_find(self.coords, self.map_params['spn'])
        self.show_image()

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

    def show_image(self):
        self.pixmap = QPixmap(self.map_file)
        self.mapField.setPixmap(self.pixmap)

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
