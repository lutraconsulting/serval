from qgis.PyQt.QtCore import QSize, Qt, pyqtSignal
from qgis.PyQt.QtWidgets import (
    QAbstractSpinBox,
    QHBoxLayout,
    QWidget,
)
from qgis.gui import QgsDoubleSpinBox

from .utils import dtypes


class BandBox(QgsDoubleSpinBox):

    enter_hit = pyqtSignal()

    def __init__(self, parent=None):
        super(BandBox, self).__init__(parent=parent)
        self.setMinimumSize(QSize(50, 24))
        self.setMaximumSize(QSize(50, 24))
        self.setAlignment(Qt.AlignLeft)
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.setKeyboardTracking(False)
        self.setShowClearButton(False)
        self.setExpressionsEnabled(False)
        self.setStyleSheet("")

    def keyPressEvent(self, event):
        super(BandBox, self).keyPressEvent(event)
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.enter_hit.emit()


class BandBoxes(QWidget):

    enter_hit = pyqtSignal(list)

    def __init__(self, bands=None, data_types=None, nodata_values=None, parent=None):
        super(BandBoxes, self).__init__(parent=parent)
        self.bands = bands if bands else [1]
        self.data_types = data_types if data_types else [6]
        self.nodata_values = nodata_values
        self.sbox = None
        lout = QHBoxLayout()
        lout.setSpacing(1)
        self.setLayout(lout)
        self.create_spinboxes(self.bands, self.data_types, self.nodata_values)

    def remove_spinboxes(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()
        self.sbox = None

    def create_spinboxes(self, bands, data_types, nodata_values):
        self.remove_spinboxes()
        self.sbox = dict()
        self.bands = bands
        self.data_types = data_types
        self.nodata_values = nodata_values
        for nr in self.bands:
            dt = self.data_types[nr - 1]
            self.sbox[nr] = BandBox()
            self.sbox[nr].setMinimum(dtypes[dt]['min'])
            self.sbox[nr].setMaximum(dtypes[dt]['max'])
            self.sbox[nr].setDecimals(dtypes[dt]['dig'])
            self.sbox[nr].setExpressionsEnabled(True)
            self.layout().addWidget(self.sbox[nr])
            self.sbox[nr].enter_hit.connect(self.enter_key_pressed)

    def enable(self, enable=True):
        for nr in self.sbox:
            self.sbox[nr].setEnabled(enable)

    def set_values(self, values):
        for nr in self.sbox:
            new_val = self.nodata_values[nr - 1] if values[nr - 1] is None else values[nr - 1]
            self.sbox[nr].setValue(new_val)

    def get_values(self):
        values = []
        for nr in self.sbox:
            raw_val = self.sbox[nr].text().replace(",", ".")
            value = int(raw_val) if self.data_types[nr -1] < 6 else float(raw_val)
            values.append(value)
        return values

    def enter_key_pressed(self):
        self.enter_hit.emit(self.get_values())
