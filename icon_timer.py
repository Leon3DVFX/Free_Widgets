# Author: Leon3DVFX
# License: MIT

from PySide6 import QtWidgets, QtCore, QtGui


# Класс для управления таймером, который будет использоваться для обновления иконки в трее
class IconTimer(QtCore.QObject):
    timeout = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._timer = QtCore.QTimer(self)
        self._timer.setTimerType(QtCore.Qt.TimerType.CoarseTimer)
        self._timer.timeout.connect(self.timeout.emit)

    # Запуск таймера с заданным интервалом (в миллисекундах)
    def start(self, interval):
        self._timer.start(interval)

    # Остановка таймера
    def stop(self):
        self._timer.stop()

    # Проверка, активен ли таймер
    def isActive(self):
        return self._timer.isActive()


# Виджет-таймера, который может быть использован для обновления иконки
class IconTimerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, interval=1000, icon_path=None, height=16):
        super().__init__(parent)
        self.timer = IconTimer(self)
        self.timer.timeout.connect(self.update_icon)
        self.icon = QtGui.QPixmap(icon_path) if icon_path else None
        self.icon.scaledToHeight(height, mode = QtCore.Qt.TransformationMode.SmoothTransformation)
        self.timer.start(interval)
        self.timer.timeout.connect(self.update_icon) # Подключаем сигнал таймера

    def update_icon(self):
        # Здесь можно добавить код для обновления иконки в трее
        pass
