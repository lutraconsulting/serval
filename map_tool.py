# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import QCursor, QPixmap

from qgis.gui import QgsMapTool

tool_cursor = [
    "17 17 3 1",
    "# c None",
    "a c #000000",
    ". c #ffffff",
    "#######.a.#######",
    "#######.a.#######",
    "#######.a.#######",
    "#######.a.#######",
    "#################",
    "#################",
    ".....#######.....",
    "aaaaa#######aaaaa",
    ".....#######.....",
    "#################",
    "#################",
    "#######.a.#######",
    "#######.a.#######",
    "#######.a.#######",
    "#######.a.#######"
]

class RasterMapTool(QgsMapTool):

    def __init__(self, canvas, button):
        QgsMapTool.__init__(self,canvas)
        self.canvas = canvas
        self.cursor = QCursor(QPixmap(tool_cursor), 1, 1)
        self.button = button

    def activate(self):
        QgsMapTool.activate(self)
        self.canvas.setCursor(self.cursor)
        self.button.setCheckable(True)
        self.button.setChecked(True)

    def deactivate(self):
        if not self:
            return
        self.emit( SIGNAL("deactivate") )
        self.button.setCheckable(False)
        QgsMapTool.deactivate(self)

    def setCursor(self,cursor):
        self.cursor = QCursor(cursor)

    # def canvasMoveEvent(self,event):
    #     self.emit( SIGNAL("moved"), QPoint(event.pos().x(), event.pos().y()) )

    def canvasPressEvent(self,event):
        self.emit( SIGNAL("pressed"), QPoint(event.pos().x(), event.pos().y()) )