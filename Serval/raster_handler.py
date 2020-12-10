import math

from qgis.core import (
    QgsCoordinateTransform,
    QgsCsException,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsProject,
    QgsRasterBlock,
    QgsRectangle,
    QgsSpatialIndex,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import pyqtSignal, QObject
from .utils import get_logger, dtypes, low_pass_filtered
from .raster_changes import RasterChange


class RasterHandler(QObject):
    """Raster layer handler."""

    raster_changed = pyqtSignal(object)

    def __init__(self, layer, uc=None, debug=False):
        super(RasterHandler, self).__init__()
        self.layer = layer
        self.uc = uc
        self.logger = get_logger() if debug else None
        self.provider = layer.dataProvider()
        self.bands_nr = self.layer.bandCount()
        self.bands_range = range(1, self.bands_nr + 1)
        self.active_bands = [1]
        self.project = QgsProject.instance()
        self.crs_transform = None if self.project.crs() == self.layer.crs() else \
            QgsCoordinateTransform(self.project.crs(), self.layer.crs(), self.project)
        self.data_types = None
        self.nodata_values = None
        self.pixel_size_x = self.layer.rasterUnitsPerPixelX()
        self.pixel_size_y = self.layer.rasterUnitsPerPixelY()
        self.raster_cols = self.layer.width()
        self.raster_rows = self.layer.height()
        self.layer_extent = self.provider.extent()
        self.min_x = self.layer_extent.xMinimum()
        self.min_y = self.layer_extent.yMinimum()
        self.max_x = self.layer_extent.xMaximum()
        self.max_y = self.layer_extent.yMaximum()
        self.origin_x = self.min_x
        self.origin_y = self.max_y
        self.first_pixel_x = self.min_x + self.pixel_size_x / 2.  # x coord of upper left pixel center
        self.first_pixel_y = self.max_y - self.pixel_size_y / 2.  # y
        self.cell_centers = None  # dict of coordinates of currently selected cells centers {(row, col): (x, y)}
        self.cell_exp_val = None  # dict of evaluated expressions for cells centers {(row, col): value}
        self.cell_pts_layer = None  # point memory layer with selected cells centers
        self.selecting_geoms = None  # dictionary of selecting geometries {id: geometry}
        self.spatial_index = None  # spatial index of selecting geometries extents
        self.block_row_min = None  # range of indices of the raster block to modify
        self.block_row_max = None
        self.block_col_min = None
        self.block_col_max = None
        self.selected_cells = None  # list of selected cells as tuples of global indices (row, cell)
        self.selected_cells_feats = None  # {(row, cell): feature}
        self.total_geometry = None
        self.all_touched_cells = None
        self.exp_field_idx = None
        self.get_data_types()
        self.get_nodata_values()

    def get_data_types(self):
        self.data_types = []
        for nr in self.bands_range:
            self.data_types.append(self.provider.dataType(nr))

    def write_supported(self):
        msg = ""
        supported = True
        for nr in self.bands_range:
            if self.provider.dataType(nr) == 0 or self.provider.dataType(nr) > 7:
                msg = f"{dtypes[self.provider.dataType(nr)]['name']} (band {nr})"
                supported = False
        return supported, msg

    def get_nodata_values(self):
        self.nodata_values = []
        for nr in self.bands_range:
            if self.provider.sourceHasNoDataValue(nr):
                self.nodata_values.append(self.provider.sourceNoDataValue(nr))
                self.provider.setUseSourceNoDataValue(nr, True)
            # no nodata defined in the raster source
            else:
                # check if user defined any nodata values
                if self.provider.userNoDataValues(nr):
                    # get min nodata value from the first user nodata range
                    nd_ranges = self.provider.userNoDataValues(nr)
                    self.nodata_values.append(nd_ranges[0].min())
                else:
                    # leave nodata undefined
                    self.nodata_values.append(None)

    def select(self, geometries, all_touched_cells=True, transform=True):
        """
        For the geometries list, find selected cells.
        If all_touched_cells is True, all cells touching a geometry will be selected.
        Otherwise, a geometry must intersect a cell center to select it.
        """
        if self.logger:
            self.logger.debug(f"Selecting cells for geometries: {[g.asWkt() for g in geometries]}")
        self.selecting_geoms = dict()
        self.selected_cells = []
        self.spatial_index = QgsSpatialIndex()
        self.total_geometry = QgsGeometry()
        dxy = 0.001
        geoms = []
        for nr, geom in enumerate(geometries):
            if not geom.isGeosValid():
                continue
            sgeom = QgsGeometry(geom)
            if self.crs_transform and transform:
                try:
                    res = sgeom.transform(self.crs_transform)
                    if not res == QgsGeometry.Success:
                        raise QgsCsException(repr(res))
                except QgsCsException as err:
                    msg = "Raster transformation failed! Check the raster projection settings."
                    if self.uc:
                        self.uc.bar_warn(msg, dur=5)
                    msg += repr(err)
                    if self.logger:
                        self.logger.warning(msg)
                    return

            self.selecting_geoms[nr] = sgeom
            self.spatial_index.addFeature(nr, sgeom.boundingBox())
            geoms.append(sgeom)
        self.total_geometry = QgsGeometry.unaryUnion(geoms)
        if self.logger:
            self.logger.debug(f"Total selecting geometry bbox: {self.total_geometry.boundingBox()}")
        self.block_row_min, self.block_row_max, self.block_col_min, self.block_col_max = \
            self.extent_to_cell_indices(self.total_geometry.boundingBox())

        half_pix_x = self.pixel_size_x / 2.
        half_pix_y = self.pixel_size_y / 2.
        self.cell_centers = dict()
        for row in range(self.block_row_min, self.block_row_max + 1):
            for col in range(self.block_col_min, self.block_col_max + 1):
                pt_x = self.first_pixel_x + col * self.pixel_size_x
                pt_y = self.first_pixel_y - row * self.pixel_size_y
                if all_touched_cells:
                    bbox = QgsRectangle(pt_x - half_pix_x, pt_y - half_pix_y,
                                        pt_x + half_pix_x, pt_y + half_pix_y)
                else:
                    bbox = QgsRectangle(pt_x, pt_y, pt_x + dxy, pt_y + dxy)
                sel_inter = self.spatial_index.intersects(bbox)
                for sel_geom_id in sel_inter:
                    g = self.selecting_geoms[sel_geom_id]
                    if g.intersects(bbox):
                        self.selected_cells.append((row, col))
                        self.cell_centers[(row, col)] = (pt_x, pt_y)
        if self.logger:
            self.logger.debug(f"Nr of cells selected: {len(self.selected_cells)}")

    def create_cell_pts_layer(self):
        """For current block extent, create memory point layer with a feature in each selected cell."""
        crs_str = self.layer.crs().toProj()
        fields_def = "field=x:double&field=y:double&field=row:int&field=col:int"
        self.cell_pts_layer = QgsVectorLayer(f"Point?crs={crs_str}&{fields_def}", "x", "memory")
        fields = self.cell_pts_layer.dataProvider().fields()
        feats = []
        for row_col, xy in self.cell_centers.items():
            row, col = row_col
            x, y = xy
            feat = QgsFeature(fields)
            feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x, y)))
            feat["row"] = row
            feat["col"] = col
            feats.append(feat)
        self.cell_pts_layer.dataProvider().addFeatures(feats)
        self.selected_cells_feats = dict()  # {(row, cell): feat}
        for feat in self.cell_pts_layer.getFeatures():
            self.selected_cells_feats[(feat["row"], feat["col"])] = feat.id()

    def write_block(self, const_values=None, low_pass_filter=False):
        """
        Construct raster block for each band, apply the values and write to file.
        If const_values are given (a list of const values for each band) they are used for each selected cell.
        In other case the memory layer with values calculated for each cell selected will be used.
        Alternatively, selected cells values can be filtered using low-pass 3x3 filter.
        """
        if self.logger:
            vals = f"const values ({const_values})" if const_values else "expression values."
            self.logger.debug(f"Writing blocks with {vals}")
        if not self.provider.isEditable():
            res = self.provider.setEditable(True)
            if not res:
                if self.uc:
                    self.uc.show_warn('QGIS can\'t modify this type of raster')
                return None
        if self.logger:
            self.logger.debug("Calculating block origin coordinates...")
        b_orig_x, b_orig_y = self.index_to_point(self.block_row_min, self.block_col_min)
        cols = self.block_col_max - self.block_col_min + 1
        rows = self.block_row_max - self.block_row_min + 1
        b_end_x = b_orig_x + cols * self.pixel_size_x
        b_end_y = b_orig_y - rows * self.pixel_size_y
        block_bbox = QgsRectangle(b_orig_x, b_end_y, b_end_x, b_orig_y)
        if self.logger:
            self.logger.debug(f"Block bbox: {block_bbox.toString()}")
            self.logger.debug(f"Nr of cells in the block: rows={rows}, cols={cols}")
        old_blocks = []
        new_blocks = []
        cell_values = dict()
        if const_values is None and not low_pass_filter:
            for feat in self.cell_pts_layer.getFeatures():
                cell_values[feat.id()] = feat.attribute(self.exp_field_idx)
        for band_nr in self.active_bands:
            block = self.provider.block(band_nr, block_bbox, cols, rows)
            new_blocks.append(block)
            block_data = block.data().data()
            old_block = QgsRasterBlock(self.data_types[band_nr - 1], cols, rows)
            old_block.setData(block_data)
            for abs_row, abs_col in self.selected_cells:
                row = abs_row - self.block_row_min
                col = abs_col - self.block_col_min
                if const_values:
                    idx = band_nr - 1 if len(self.active_bands) > 1 else 0
                    new_val = const_values[idx]
                elif low_pass_filter:
                    # the filter is applied for cells inside the block only
                    if block.height() < 3 or block.width() < 3:
                        # the selected block is too small for filtering -> keep the old value
                        new_val = None
                    else:
                        new_val = low_pass_filtered(old_block, row, col, self.nodata_values[band_nr - 1])
                else:
                    # set the expression value
                    feat_id = self.selected_cells_feats[(abs_row, abs_col)]
                    if cell_values[feat_id] is not None:
                        new_val = None if math.isnan(cell_values[feat_id]) or \
                                      cell_values[feat_id] is None else cell_values[feat_id]
                    else:
                        new_val = None
                new_val = old_block.value(row, col) if new_val is None else new_val
                set_res = block.setValue(row, col, new_val)
                if self.logger:
                    self.logger.debug(f"Setting block value for band {band_nr}, row {row}, col: {col}: {set_res}")
            old_blocks.append(old_block)
            band_res = self.provider.writeBlock(block, band_nr, self.block_col_min, self.block_row_min)
            if self.logger:
                self.logger.debug(f"Writing block for band {band_nr}: {band_res}")
        self.provider.setEditable(False)
        change = RasterChange(self.active_bands, self.block_row_min, self.block_col_min, old_blocks, new_blocks)
        self.raster_changed.emit(change)
        return True

    def write_block_undo(self, data):
        """Write blocks from the undo / redo stack."""
        if self.logger:
            self.logger.debug(f"Writing blocks from undo")
        if not self.provider.isEditable():
            res = self.provider.setEditable(True)
        bands, row_min, col_min, blocks = data
        for band_nr in bands:
            idx = band_nr - 1 if len(bands) > 1 else 0
            block = blocks[idx]
            band_res = self.provider.writeBlock(block, band_nr, col_min, row_min)
            if self.logger:
                self.logger.debug(f"Writing undo/redo block for band {band_nr}: {band_res}")
        self.provider.setEditable(False)

    def extent_to_cell_indices(self, extent):
        """Return x and y raster cell indices ranges for the extent."""
        col_min, row_max = self.point_to_index((extent.xMinimum(), extent.yMinimum()))
        col_max, row_min = self.point_to_index((extent.xMaximum(), extent.yMaximum()))
        if self.logger:
            self.logger.debug(f"Cell ranges for extent {extent.toString(precision=3)} = row_min: {row_min}, " +
                              f"row_max: {row_max}, col_min: {col_min}, col_max: {col_max}")
        return row_min, row_max, col_min, col_max

    def index_to_point(self, row, col, upper_left=True):
        """Return cell upper left corner or cell center coordinates."""
        x0 = self.origin_x if upper_left else self.first_pixel_x
        y0 = self.origin_y if upper_left else self.first_pixel_y
        x, y = x0 + col * self.pixel_size_x, y0 - row * self.pixel_size_y
        if self.logger:
            self.logger.debug(f"Coords for ({row}, {col}) = ({x}, {y}) (x, y)")
        return x, y

    def point_to_index(self, coords):
        """
        Return raster cell indices for the coordinates.
        If it falls outside of the layer extent, then the first or last index is returned.
        """
        if self.origin_x <= coords[0] <= self.max_x:
            x_offset = coords[0] - self.origin_x
            col = math.floor(x_offset / self.pixel_size_x)
        elif coords[0] < self.origin_x:
            col = 0
        else:
            col = self.raster_cols - 1

        if self.min_y <= coords[1] <= self.origin_y:
            y_offset = self.origin_y - coords[1]
            row = math.floor(y_offset / self.pixel_size_y)
        elif coords[1] > self.origin_y:
            row = 0
        else:
            row = self.raster_rows - 1

        return col, row
