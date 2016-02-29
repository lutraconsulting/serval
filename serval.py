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

class Serval:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.probeTool = QgsMapToolEmitPoint(self.canvas)
        self.probeTool.setCursor(QCursor(QPixmap(':plugins/icons/mIconColorPicker.svg'), hotX=2, hotY=22))
        self.drawTool = QgsMapToolEmitPoint(self.canvas)
        self.drawTool.setCursor(QCursor(QPixmap(':plugins/icons/mActionToggleEditing.svg'), hotX=2, hotY=22))
        self.pluginIsActive = False
        self.widget = None
        self.dockwidget = None

    def initGui(self):
        self.action=QAction(QIcon(":/plugins/icons/serval_icon.svg"), "Serval - set raster value tool", self.iface.mainWindow())
        self.iface.addToolBarIcon(self.action)
        QObject.connect(self.action, SIGNAL("triggered()"), self.activateTool)
        QgsMessageLog.logMessage("Gui loaded", 'Serval', QgsMessageLog.INFO)


    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        # disconnects
        self.widget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None
        self.pluginIsActive = False


    def unload(self):
        # properly close raster data if they exist
        try:
            for key, value in self.widget.bands.iteritems():
                self.widget.bands[key]['data'] = None
            self.widget.bands = None
            self.widget.gdal_raster = None
        except AttributeError:
            pass
        self.widget = None
        if not self.dockwidget is None:
            self.dockwidget.close()
            self.iface.removeDockWidget(self.dockwidget)
        self.iface.removeToolBarIcon(self.action)

    def activateTool(self):
        if not self.pluginIsActive:
            self.pluginIsActive = True
        if self.dockwidget == None:
            self.widget = ServalWidget(self.iface, self)
            self.widget.closingPlugin.connect(self.onClosePlugin)
            self.widget.raster = None
            self.probeTool.canvasClicked.connect(self.widget.pointClicked)
            self.drawTool.canvasClicked.connect(self.widget.pointClicked)
            self.dockwidget=QDockWidget("Serval - Set Raster Value" , self.iface.mainWindow() )
            self.dockwidget.setObjectName("Serval")
            self.dockwidget.setWidget(self.widget)
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)
        self.canvas.setMapTool(self.probeTool)
        self.dockwidget.show()
        self.widget.setActiveRaster()

