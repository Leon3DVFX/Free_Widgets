# Author: Leon3DVFX
# License: MIT

from PySide6 import QtWidgets, QtCore, QtGui

# Класс основной таймер
class IconTimer(QtCore.QObject):
    timeout = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._timer = QtCore.QTimer(self)
        self._timer.setTimerType(QtCore.Qt.TimerType.CoarseTimer)
        self._timer.timeout.connect(self.timeout.emit)

    def start(self, interval):
        self._timer.start(interval)

    def stop(self):
        self._timer.stop()

    def isActive(self):
        return self._timer.isActive()

# Класс виджет таймер - иконка + анимация
class IconTimerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, interval=1000, icon_path=None, height=16, pen_width = 1):
        super().__init__(parent)
        # Предварительная
        self.interval = max(1, int(interval))
        self.remaining_ms = float(self.interval)

        self.icon = QtGui.QPixmap(icon_path) if icon_path else None
        if self.icon is not None:
            self.icon = self.icon.scaledToHeight(
                height,
                mode=QtCore.Qt.TransformationMode.SmoothTransformation,
            )
        # Настройка пена (предварительно) TODO: Сделать настраиваемо
        self.pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 100), pen_width)

        self.tick = QtCore.QTimer(self)
        self.tick.setTimerType(QtCore.Qt.TimerType.PreciseTimer)
        self.tick.setInterval(15)
        self.tick.timeout.connect(self._on_tick)

        self.elapsed = QtCore.QElapsedTimer()
        self.elapsed.start()
        self.tick.start()
    # Отсчет до перерисовки
    def _on_tick(self):
        self.remaining_ms = max(0, self.interval - self.elapsed.elapsed())
        self.update()

        if self.remaining_ms == 0:
            self.tick.stop()
            self.update_icon()
    # Метод TimeOut таймера
    def update_icon(self):
        print("Time out")
        self.close()
    # Перерисовка виджета
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(self.pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        # Процедурный rect - пересчет
        size = max(8, min(self.width(), self.height()) - self.pen.width())
        rect = QtCore.QRect(
            (self.width() - size) // 2,
            (self.height() - size) // 2,
            size,
            size,
        )

        progress = self.remaining_ms / self.interval
        start_angle = -270 * 16
        span_angle = int(-360 * 16 * progress)
        painter.drawArc(rect, start_angle, -span_angle)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = IconTimerWidget(interval=1500, pen_width=15)
    win.resize(200,200)
    win.show()
    sys.exit(app.exec())