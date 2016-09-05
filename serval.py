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
from qgis.gui import *
from osgeo import gdal
from osgeo.gdalconst import *
from array import array
import os.path
from .utils import *
from .user_communication import UserCommunication
import os.path
import ConfigParser

gdal.ErrorReset()
gdal.UseExceptions()



class BandSpinBox(QgsDoubleSpinBox):
    """Spinbox class for raster band value"""
    def __init__(self, parent):
        super(BandSpinBox, self).__init__()
        self.parent = parent

    def keyPressEvent(self, event):
        b = self.property("bandNr")
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if is_number(self.text().replace(',','.')):
                self.setValue(float(self.text().replace(',','.')))
                self.parent.change_cell_value_key()
            else:
                self.parent.uc.bar_warn('Enter a number!')
        else:
            QgsDoubleSpinBox.keyPressEvent(self, event)
            
            
            
class Serval:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.plugin_dir = os.path.dirname(__file__)
        self.uc = UserCommunication(iface, 'Serval')
        self.menu = u'Serval'
        self.actions = []
        self.toolbar = self.iface.addToolBar(u'Serval')
        self.toolbar.setObjectName(u'Serval')
        self.setup_tools()
        self.mode = 'probe'
        self.bands = {}
        self.px, self.py = [0, 0]
        self.last_point = QgsPoint(0,0)
        self.undos = {}
        self.redos = {}
        
        self.mapRegistry = QgsMapLayerRegistry.instance()
        self.iface.currentLayerChanged.connect(self.set_active_raster)
        self.mapRegistry.layersAdded.connect(self.set_active_raster)
        self.canvas.mapToolSet.connect(self.check_active_tool)

        
    def setup_tools(self):
        self.probeTool = QgsMapToolEmitPoint(self.canvas)
        self.probeTool.setObjectName('SProbeTool')
        self.probeTool.setCursor(QCursor(QPixmap(os.path.join(
            os.path.dirname(__file__), 'icons/probe_tool.svg')), hotX=2, hotY=22))
        self.probeTool.canvasClicked.connect(self.point_clicked)
        self.drawTool = QgsMapToolEmitPoint(self.canvas)
        self.drawTool.setObjectName('SDrawTool')
        self.drawTool.setCursor(QCursor(QPixmap(os.path.join(
            os.path.dirname(__file__), 'icons/draw_tool.svg')), hotX=2, hotY=22))
        self.drawTool.canvasClicked.connect(self.point_clicked)
        self.gomTool = QgsMapToolEmitPoint(self.canvas)
        self.gomTool.setObjectName('SGomTool')
        self.gomTool.setCursor(QCursor(QPixmap(os.path.join(
            os.path.dirname(__file__), 'icons/gom_tool.svg')), hotX=5, hotY=19))
        self.gomTool.canvasClicked.connect(self.point_clicked)
        

    def initGui(self):
        self.add_action(
            os.path.join(self.plugin_dir,'icons/serval_icon.svg'),
            text=u'Show Serval Toolbar',
            add_to_menu=True,
            add_to_toolbar=False,
            callback=self.show_toolbar,
            parent=self.iface.mainWindow())
        
        self.probe_btn = self.add_action(
            os.path.join(self.plugin_dir,'icons/probe.svg'),
            text=u'Probing Mode',
            whats_this=u'Probing Mode',
            add_to_toolbar=True,
            callback=self.activate_probing,
            parent=self.iface.mainWindow())
        self.draw_btn = self.add_action(
            os.path.join(self.plugin_dir,'icons/draw.svg'),
            text=u'Drawing Mode',
            whats_this=u'Drawing Mode',
            add_to_toolbar=True,
            callback=self.activate_drawing,
            parent=self.iface.mainWindow())
        self.gom_btn = self.add_action(
            os.path.join(self.plugin_dir,'icons/gom.svg'),
            text=u'Set Raster Cell Value to NoData',
            whats_this=u'Set Raster Cell Value to NoData',
            add_to_toolbar=True,
            callback=self.activate_gom,
            parent=self.iface.mainWindow())
        self.def_nodata_btn = self.add_action(
            os.path.join(self.plugin_dir,'icons/define_nodata.svg'),
            text=u'Define/Change Raster NoData Value',
            whats_this=u'Define/Change Raster NoData Value',
            add_to_toolbar=True,
            callback=self.define_nodata,
            parent=self.iface.mainWindow())
            
        self.mColorButton = QgsColorButtonV2()
        icon1 = QIcon(os.path.join(self.plugin_dir,'icons/mIconColorBox.svg'))
        self.mColorButton.setIcon(icon1)
        self.mColorButton.setMinimumSize(QSize(40, 24))
        self.mColorButton.setMaximumSize(QSize(40, 24))
        self.mColorButton.colorChanged.connect(self.set_rgb_from_picker)
        self.toolbar.addWidget(self.mColorButton)
        
        self.setup_spin_boxes()
         
        self.undo_btn = self.add_action(
            os.path.join(self.plugin_dir,'icons/undo.svg'),
            text=u'Undo',
            whats_this=u'Undo',
            add_to_toolbar=True,
            callback=self.undo,
            parent=self.iface.mainWindow())
        self.redo_btn = self.add_action(
            os.path.join(self.plugin_dir,'icons/redo.svg'),
            text=u'Redo',
            whats_this=u'Redo',
            add_to_toolbar=True,
            callback=self.redo,
            parent=self.iface.mainWindow())
        self.show_help = self.add_action(
            os.path.join(self.plugin_dir,'icons/help.svg'),
            text=u'Help',
            whats_this=u'Help',
            add_to_toolbar=True,
            add_to_menu=True,
            callback=self.show_website,
            parent=self.iface.mainWindow())
            
        self.first_use()
        self.set_active_raster()
        self.check_undo_redo_btns()

    
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=False,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
            
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)
        return action


    def unload(self):
        # properly close raster data if they exist
        try:
            for key, value in self.bands.iteritems():
                self.bands[key]['data'] = None
                self.bands[key]['array'] = None
            self.bands = None
            self.gdal_raster = None
        except AttributeError:
            pass

        for action in self.actions:
            self.iface.removePluginMenu(
                u'Serval',
                action)
            self.iface.removeToolBarIcon(action)
        del self.mColorButton, self.b1SBox, self.b2SBox, self.b3SBox
        del self.toolbar


    def show_toolbar(self):
        if self.toolbar:
            self.toolbar.show()
            
    
    def check_active_tool(self, tool):
        try:
            if not tool.objectName() in ['SDrawTool', 'SProbeTool', 'SGomTool']:
                self.probe_btn.setChecked(False)
                self.draw_btn.setChecked(False)
                self.gom_btn.setChecked(False)
        except AttributeError:
            pass


    def activate_probing(self):
        self.mode = 'probe'
        self.canvas.setMapTool(self.probeTool)
        self.draw_btn.setChecked(False)
        self.probe_btn.setChecked(True)
        self.gom_btn.setChecked(False)
        
    
    def activate_drawing(self):
        self.mode = 'draw'
        self.canvas.setMapTool(self.drawTool)
        self.draw_btn.setChecked(True)
        self.probe_btn.setChecked(False)
        self.gom_btn.setChecked(False)
        

    def activate_gom(self):
        self.mode = 'gom'
        self.canvas.setMapTool(self.gomTool)
        self.draw_btn.setChecked(False)
        self.probe_btn.setChecked(False)
        self.gom_btn.setChecked(True)


    def setup_spin_boxes(self):
        self.b1SBox = BandSpinBox(self)
        self.b2SBox = BandSpinBox(self)
        self.b3SBox = BandSpinBox(self)
        sboxes = [self.b1SBox, self.b2SBox, self.b3SBox]
        for sbox in sboxes:
            sbox.setMinimumSize(QSize(60, 25))
            sbox.setMaximumSize(QSize(60, 25))
            sbox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
            sbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
            sbox.setKeyboardTracking(False)
            sbox.setShowClearButton(False)
            sbox.setExpressionsEnabled(False)
            sbox.setStyleSheet("")
            self.toolbar.addWidget(sbox)


    def point_clicked(self, point=None, button=None):
        # check if active layer is raster
        if self.raster == None:
            self.uc.bar_warn("Choose a raster to set a value", dur=3)
            return
        
        # check if coordinates trasformation is required
        cSrs = self.iface.mapCanvas().mapRenderer().destinationCrs()
        if point is None:
            pos = self.last_point
        elif not cSrs == self.raster.crs() and self.iface.mapCanvas().hasCrsTransformEnabled():
            srsTransform = QgsCoordinateTransform(cSrs, self.raster.crs())
            try:
                pos = srsTransform.transform(point)
            except QgsCsException, err:
                self.uc.bar_warn("Point coordinates transformation failed! Check the raster projection.", dur=5)
                return
        else:
            pos = QgsPoint(point.x(), point.y())
        
        # keep last clicked point
        self.last_point = pos
        
        # check if the point is within active raster bounds
        if pos.x() >= self.rbounds[0] and pos.x() <= self.rbounds[2]:
            self.px = int((pos.x() - self.gt[0]) / self.gt[1])
        else:
            self.uc.bar_info("Out of x bounds", dur=2)
            return

        if  pos.y() >= self.rbounds[1] and pos.y() <= self.rbounds[3]:
            self.py = int((pos.y() - self.gt[3]) / self.gt[5])
        else:
            self.uc.bar_info("Out of y bounds", dur=2)
            return
        
        # temporary tables for undo/redo values
        old_vals = []
        new_vals = []
        
        for nr in range(1, min(4, self.bandCount + 1)):
            # bands data type
            dt = self.bands[nr]['qtype']
            
            # self.bands[nr]['array1'] = self.bands[nr]['data'].ReadAsArray(self.px, self.py, 1, 1)
            # ReadAsArray crashes Python on QGIS closing on Windows
            # using workaround with ReadRaster
            scanline = self.bands[nr]['data'].ReadRaster(self.px, self.py, 1, 1, 1, 1, dt)
            self.bands[nr]['array'] = array(dtypes[dt]['atype'], scanline)
            value = self.bands[nr]['array'][0]
            
            # check if nodata is defined
            if self.mode == 'gom' and self.bands[nr]['nodata'] == None:
                msg = 'NODATA value is not defined for one of the raster\'s bands.\n'
                msg += 'Please define it in raster properties dialog!'
                self.uc.show_warn(msg)
                return
            
            # if in probing mode, set band's spinbox value
            if self.mode == 'probe':
                if is_number(value):
                    self.bands[nr]['sbox'].setValue(value)
                    self.bands[nr]['sbox'].setFocus()
                    self.bands[nr]['sbox'].selectAll()
                    
            # writing mode
            else:
                old_val = array(dtypes[dt]['atype'], [value])
                if self.mode == 'gom':
                    val = self.bands[nr]['nodata']
                else:
                    val = float(str(self.bands[nr]['sbox'].value()).replace(',', '.'))
                    
                val = int(val) if dt < 6 else float(val)
                new_val = array(dtypes[dt]['atype'], [val])
                              
                # add old and new band's values for undo/redo
                old_vals.append(old_val)
                new_vals.append(new_val)
        
        if not self.mode == 'probe':
            
            # store all bands' changes to undo list
            if self.raster.id() in self.undos.keys():
                self.undos[self.raster.id()].append([old_vals, new_vals, self.px, self.py])
            else:
                self.undos[self.raster.id()] = [[old_vals, new_vals, self.px, self.py]]
                self.redos[self.raster.id()] = []
                
            # write the new cell value(s)
            self.change_cell_value(new_vals)

        if self.bandCount > 2:
            self.mColorButton.setColor(QColor(
                self.bands[1]['sbox'].value(),
                self.bands[2]['sbox'].value(),
                self.bands[3]['sbox'].value()
            ))


    def set_rgb_from_picker(self, c):
        """Set bands spinboxes values after color change in the color picker"""
        self.bands[1]['sbox'].setValue(c.red())
        self.bands[2]['sbox'].setValue(c.green())
        self.bands[3]['sbox'].setValue(c.blue())


    def change_cell_value(self, vals, x=None, y=None):
        """Save new bands values to disk"""
        if not x:
            x = self.px
        else:
            pass
        if not y:
            y = self.py
        else:
            pass
            
        for nr in range(1, min(4, self.bandCount + 1)):
            # self.bands[nr]['data'].WriteArray(self.bands[nr]['array'], self.px, self.py)
            # WriteArray crashes Python on QGIS closing on Windows
            # using workaround with WriteRaster
            s = vals[nr-1]
            rbuf = s.tostring()
            self.bands[nr]['data'].WriteRaster(x, y, 1, 1, rbuf, buf_type=self.bands[nr]['qtype'])
            self.bands[nr]['data'] = None
            self.bands[nr] = None
        
        # save changes to the raster file
        self.gdal_raster = None 
        # refresh raster view
        self.raster.setCacheImage(None)
        self.raster.triggerRepaint()
        # prepare raster for next actions
        self.prepare_gdal_raster(True)
        self.check_undo_redo_btns()
        

    def change_cell_value_key(self):
        """Change cell value after user changes band's spinbox value and hits Enter key"""
        if self.last_point:
            pm = self.mode
            self.mode = 'draw'
            self.point_clicked()
            self.mode = pm
        
        
    def undo(self):
        if self.undos[self.raster.id()]:
            data = self.undos[self.raster.id()].pop()
            self.redos[self.raster.id()].append(data)
        else:
            return
        self.change_cell_value(data[0], data[2], data[3])
    
    
    def redo(self):
        if self.redos[self.raster.id()]:
            data = self.redos[self.raster.id()].pop()
            self.undos[self.raster.id()].append(data)
        else:
            return
        self.change_cell_value(data[1], data[2], data[3])
    
    
    def define_nodata(self):
        """Define and write a new NoData value to raster file"""
        if not self.raster:
            self.uc.bar_warn('Select a raster layer to define/change NoData value!')
            return
        
        # check if user defined additional NODATA value
        if self.rdp.userNoDataValues(1):
            note = '\nNote: there is a user defined NODATA value.\nCheck the raster properties (Transparency).'
        else:
            note = ''
        # first band data type
        dt = self.rdp.dataType(1)
        
        # current NODATA value
        if self.rdp.srcHasNoDataValue(1):
            cur_nodata = self.rdp.srcNoDataValue(1)
            if dt < 6:
                cur_nodata = '{0:d}'.format(int(float(cur_nodata)))
        else:
            cur_nodata = ''
        
        label = 'Define/change raster NODATA value.\n\n'
        label += 'Raster data type: {}.{}'.format(dtypes[dt]['name'], note)
        nd, ok = QInputDialog.getText(None, "Define NODATA Value",
            label, QLineEdit.Normal, str(cur_nodata))
        if not ok:
            return
        
        if not is_number(nd):
            self.uc.show_warn('Wrong NODATA value!')
            return
        
        new_nodata = int(nd) if dt < 6 else float(nd)
        
        # set the NODATA value for each band
        res = []
        for nr in range(1, min(4, self.bandCount + 1)):
            res.append(self.rdp.setNoDataValue(nr, new_nodata))
            self.rdp.setUseSrcNoDataValue(nr, True)
        
        if False in res:
            self.uc.show_warn('Setting new NODATA value failed!')
        else:
            self.uc.bar_info('Succesful setting new NODATA values!', dur=2)
        self.prepare_gdal_raster()
        self.raster.setCacheImage(None)
        self.raster.triggerRepaint()

        
        
    def check_undo_redo_btns(self):
        """Enable/Disable undo and redo buttons based on availability of undo/redo steps"""
        try:
            if len(self.undos[self.raster.id()]) == 0:
                self.undo_btn.setDisabled(True)
            else:
                self.undo_btn.setEnabled(True)
        except:
            self.undo_btn.setDisabled(True)
             
        try:
            if len(self.redos[self.raster.id()]) == 0:
                self.redo_btn.setDisabled(True)
            else:
                self.redo_btn.setEnabled(True)
        except:
            self.redo_btn.setDisabled(True)

    
    def set_active_raster(self):
        """Active layer has change - check if it is a raster layer and prepare it for the plugin"""
        # properly close previous raster data if exist
        try:
            for nr in self.bands.keys():
                self.bands[nr]['data'] = None
                self.bands = None
                self.gdal_raster = None
        except:
            pass
        
        # disable all toolbar actions except Help
        # (for vectors and unsupported rasters)
        for action in self.actions:
            action.setDisabled(True)
        self.show_help.setEnabled(True)
                
        layer = self.iface.activeLayer()
        
        # check if we can work with the raster
        if layer!=None and layer.isValid() and \
                layer.type() == 1 and \
                layer.dataProvider() and \
                (layer.dataProvider().capabilities() & 2) and \
                not layer.crs() is None:
            self.raster = layer
            self.rdp = layer.dataProvider()
            self.bandCount = layer.bandCount()
            
            # is data type supported?
            supported = True
            for nr in range(1, min(4, self.bandCount + 1)):
                if self.rdp.dataType(nr) == 0 or self.rdp.dataType(nr) > 7:
                    t = dtypes[self.rdp.dataType(nr)]['name']
                    supported = False
                
            if supported:
                # disable all toolbar actions (for vectors and unsupported rasters)
                for action in self.actions:
                    action.setEnabled(True)
                # if raster properties change get them (refeshes view)
                self.raster.rendererChanged.connect(self.prepare_gdal_raster)
                self.prepare_gdal_raster(True)

            # not supported data type
            else:
                msg = 'The raster data type is: {}.'.format(t)
                msg += '\nServal can\'t work with it, sorry!'
                self.uc.show_warn(msg)
                self.raster = None
                self.mColorButton.setDisabled(True)
                self.prepare_gdal_raster(False)
        
        # it is not a supported raster layer
        else:
            self.raster = None
            self.mColorButton.setDisabled(True)
            self.prepare_gdal_raster(False)
        
        self.check_undo_redo_btns()


    def prepare_gdal_raster(self, supported=True):
        """Open raster using GDAL if it is supported"""
        # reset bands' spinboxes
        sboxes = [self.b1SBox, self.b2SBox, self.b3SBox]
        for i, sbox in enumerate(sboxes):
            sbox.setProperty('bandNr', i+1)
            sbox.setDisabled(True)
            
        if supported:
            if self.bandCount > 2:
                self.mColorButton.setEnabled(True)
            else:
                self.mColorButton.setDisabled(True)           
            try:
                self.gdal_raster = gdal.Open(self.raster.source(), GA_Update)
            except:
                self.uc.show_warn("Can't open this raster for writing!")
                return
            
            # set projection if needed
            if self.gdal_raster.GetProjection() == '':
                msg = "The raster has no projection defined. Using the projection defined in the layer's properities."
                self.uc.bar_info(msg)
                proj_wkt = self.raster.crs().toWkt()
                self.gdal_raster.SetProjection(str(proj_wkt))

            self.gt = self.gdal_raster.GetGeoTransform()
            self.r_width = self.gdal_raster.RasterXSize
            self.r_height = self.gdal_raster.RasterYSize

            # raster bounds [xmin, ymin, xmax, ymax] in raster CRS
            self.rbounds = [
                self.gt[0],
                self.gt[3] + self.r_width * self.gt[4] + self.r_height * self.gt[5],
                self.gt[0] + self.r_width * self.gt[1] + self.r_height * self.gt[2],
                self.gt[3]
            ]
            # create raster bands dictionary
            self.bands = {}
            for nr in range(1, min(4, self.bandCount + 1)):
                self.bands[nr] = {}
                self.bands[nr]['sbox'] = sboxes[nr-1]
                self.bands[nr]['data'] = self.gdal_raster.GetRasterBand(nr)
                
                # NODATA
                if self.rdp.srcHasNoDataValue(nr): # source nodata value?
                    self.bands[nr]['nodata'] = self.rdp.srcNoDataValue(nr)
                    # use the src nodata
                    self.rdp.setUseSrcNoDataValue(nr, True)
                # no nodata defined in the raster source
                else:
                    # check if user defined any nodata values
                    if self.rdp.userNoDataValues(nr):
                        # get min nodata value from the first user nodata range
                        nd_ranges = self.rdp.userNoDataValues(nr)
                        self.bands[nr]['nodata'] = nd_ranges[0].min()
                    else:
                        # leave nodata undefined
                        self.bands[nr]['nodata'] = None
                
                # enable band's spinbox
                self.bands[nr]['sbox'].setEnabled(True)
                # get bands data type
                dt = self.bands[nr]['qtype'] = self.rdp.dataType(nr)
                # set spinboxes properties
                self.bands[nr]['sbox'].setMinimum(dtypes[dt]['min'])
                self.bands[nr]['sbox'].setMaximum(dtypes[dt]['max'])
                self.bands[nr]['sbox'].setDecimals(dtypes[dt]['dig'])
                

    def show_website(self):
        QDesktopServices.openUrl(QUrl('https://github.com/erpas/serval/wiki'))


    def first_use(self):
        meta = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'metadata.txt')
        ver = read_ini_par(meta, 'general', 'version')
        s = QSettings()
        first = s.value('Serval/version', '0')
        if first == '0':
            return
        elif not first == ver:
            self.uc.show_warn('Please, restart QGIS before using the Serval plugin!')
            s.setValue('Serval/version', ver)