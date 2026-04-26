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
    def __init__(self, parent=None, interval=1000, icon_path=None, height=16, pen_width = 1,
                 pen_color=QtGui.QColor(255, 255, 255, 100), ring_gap=2):
        super().__init__(parent)
        # Предварительная настройка таймера
        self.interval = max(1, int(interval))
        self.remaining_ms = float(self.interval)
        self._icon_height = max(1, int(height))
        self.ring_gap = max(0, int(ring_gap))
        # Только размеры виджета и полная прозрачность
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self._icon_source = QtGui.QPixmap(icon_path) if icon_path else QtGui.QPixmap()
        self.icon = QtGui.QPixmap()

        # Настройка пена (предварительно) TODO: Сделать настраиваемо
        self.pen = QtGui.QPen(pen_color, max(1, int(pen_width)))
        widget_size = self._icon_height + (2 * self.ring_gap) + (2 * self.pen.width())
        self.resize(widget_size, widget_size)
        self._rescale_icon()

        self.tick = QtCore.QTimer(self)
        self.tick.setTimerType(QtCore.Qt.TimerType.PreciseTimer)
        self.tick.setInterval(15)
        self.tick.timeout.connect(self._on_tick)

        self.elapsed = QtCore.QElapsedTimer()
        self.elapsed.start()
        self.tick.start()

    def _arc_rect(self):
        half_pen = self.pen.widthF() / 2.0
        return QtCore.QRectF(self.rect()).adjusted(half_pen, half_pen, -half_pen, -half_pen)

    def _rescale_icon(self):
        if self._icon_source.isNull():
            self.icon = QtGui.QPixmap()
            return

        available_height = self._arc_rect().height() - self.pen.widthF() - (2 * self.ring_gap)
        target_height = max(1, int(round(min(self._icon_height, available_height))))
        self.icon = self._icon_source.scaledToHeight(
            target_height,
            mode=QtCore.Qt.TransformationMode.SmoothTransformation,
        )

    def resizeEvent(self, event):
        self._rescale_icon()
        super().resizeEvent(event)
    # Отсчет до перерисовки
    def _on_tick(self):
        self.remaining_ms = max(0, self.interval - self.elapsed.elapsed())
        self.update()

        if self.remaining_ms == 0:
            self.tick.stop()
            self.time_out()
    # Метод TimeOut таймера
    def time_out(self):
        print("Time out")
        self.close()

    # Перерисовка виджета
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing
            | QtGui.QPainter.RenderHint.SmoothPixmapTransform
        )
        painter.setPen(self.pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        rect = self._arc_rect()
        # Процедурный rect - пересчет
        if not self.icon.isNull():
            icon_x = int(round(rect.center().x() - (self.icon.width() / 2)))
            icon_y = int(round(rect.center().y() - (self.icon.height() / 2)))
            painter.drawPixmap(icon_x, icon_y, self.icon)

        progress = self.remaining_ms / self.interval
        start_angle = -270 * 16
        span_angle = int(-360 * 16 * progress)
        painter.drawArc(rect, start_angle, -span_angle)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = IconTimerWidget(interval=3000, pen_width=3, pen_color=QtGui.QColor(243, 75, 105, 150), height=50,
                          ring_gap=0,
                          icon_path=r"C:\Users\User\Desktop\icons_test\icons\py_active.png")
    win.show()
    win.show()
    sys.exit(app.exec())
