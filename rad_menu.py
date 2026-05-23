# Author: Leon3DVFX
# License: MIT

from PySide6 import QtWidgets, QtCore, QtGui

# Основной класс радиального меню
class RadialMenu(QtWidgets.QWidget):
    def __init__(self, parent=None, radius1=50, radius2=100, num_items=6):
        super().__init__(parent)
        # Убедимся, что радиус1 меньше радиуса2, иначе поменяем их местами
        if radius1 > radius2:
            self.radius1 = radius2
            self.radius2 = radius1
        else:
            self.radius1 = radius1
            self.radius2 = radius2
        self.num_items = num_items

