# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Serval
                                 A QGIS plugin
 Set Raster Values
                              -------------------
        begin                : 2015-12-30
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Radosław Pasiok
        email                : rpasiok@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMapToolEmitPoint
from serval_widget import ServalWidget
import resources

tool_cursor = [
    "16 16 3 1",
    "# c None",
    "a c #000000",
    ". c #ffffff",
    "######.aa.######",
    "######.aa.######",
    "######.aa.######",
    "######.aa.######",
    "######.aa.######",
    "################",
    ".....######.....",
    "aaaaa######aaaaa",
    "aaaaa######aaaaa",
    ".....######.....",
    "################",
    "######.aa.######",
    "######.aa.######",
    "######.aa.######",
    "######.aa.######",
    "######.aa.######",
]

class Serval:
    def __init__(self, iface):
        self.iface = iface
        self.canvas=self.iface.mapCanvas()
        self.pointTool = QgsMapToolEmitPoint(self.canvas)
        self.pointTool.setCursor(QCursor(QPixmap(tool_cursor), 1, 1))

    def initGui(self):
        self.action=QAction(QIcon(":/plugins/icons/icon.svg"), "Serval", self.iface.mainWindow())
        self.iface.addToolBarIcon(self.action)
        QObject.connect(self.action, SIGNAL("triggered()"), self.activateTool)

        self.widget = ServalWidget(self.iface)
        self.widget.raster = None
        self.pointTool.canvasClicked.connect(self.widget.pointClicked)

        self.dockwidget=QDockWidget("Serval - Set Raster Value" , self.iface.mainWindow() )
        self.dockwidget.setObjectName("Serval")
        self.dockwidget.setWidget(self.widget)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)

        self.widget.populateRastersCbo()
        QgsMessageLog.logMessage("Gui loaded", 'Serval', QgsMessageLog.INFO)

    def unload(self):
        self.widget.gdal_raster = None
        self.dockwidget.close()
        del self.widget
        self.iface.removeDockWidget(self.dockwidget)
        self.iface.removeToolBarIcon(self.action)

    def activateTool(self):
        self.canvas.setMapTool(self.pointTool)

