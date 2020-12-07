from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
)
from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsMapLayerComboBox


class LayerSelectDialog(QDialog):
    def __init__(self, parent=None, title=""):
        super(QDialog, self).__init__(parent)

        self.cbo = QgsMapLayerComboBox()
        self.cbo.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        lout = QVBoxLayout()
        lout.addWidget(self.cbo)
        lout.addWidget(self.btns)
        self.setLayout(lout)
        self.setWindowTitle("Choose layer for selection")
