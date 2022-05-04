import os
from osgeo import gdal
import tempfile

dtypes = {
    0: {'name': 'UnknownDataType'}, 
    1: {'name': 'Byte', 'atype': 'B',
        'min': 0, 'max': 255, 'dig': 0},
    2: {'name': 'UInt16', 'atype': 'H',
        'min': 0, 'max': 65535, 'dig': 0},
    3: {'name': 'Int16', 'atype': 'h',
        'min': -32768, 'max': 32767, 'dig': 0},
    4: {'name': 'UInt32', 'atype': 'I',
        'min': 0, 'max': 4294967295, 'dig': 0},
    5: {'name': 'Int32', 'atype': 'i',
        'min': -2147483648, 'max': 2147483647, 'dig': 0},
    6: {'name': 'Float32', 'atype': 'f',
        'min': -3.4e38, 'max': 3.4e38, 'dig': 4},   # max digs 5
    7: {'name': 'Float64', 'atype': 'd',
        'min': -1.7e308, 'max': 1.7e308, 'dig': 4},  # max digs 12
    8: {'name': 'CInt16'}, 
    9: {'name': 'CInt32'}, 
    10: {'name': 'CFloat32'}, 
    11: {'name': 'CFloat64'}, 
    12: {'name': 'ARGB32'}, 
    13: {'name': 'ARGB32_Premultiplied'}
}


def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def icon_path(icon_filename):
    plugin_dir = os.path.dirname(__file__)
    return os.path.join(plugin_dir, 'icons', icon_filename)


def get_logger():
    import logging
    from datetime import date
    logger = logging.getLogger(f"Serval")
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter("{asctime}: {message} [{filename}]", datefmt="%Y-%m-%d %H:%M:%S", style="{")
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        try:
            os.mkdir(log_dir)
        except FileExistsError:
            pass
        logfilename = os.path.join(log_dir, f"serval_{date.today()}.log")
        fh = logging.FileHandler(logfilename)
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)
    return logger


def low_pass_filtered(block, row, col, nodata_value, nodata_mode=False):
    """
    Return low-pass filtered (3x3) value of raster cell from the block at (row, col).
    Cells at the edge of block are not filtered.
    Cells having originally nodata are not modified either.
    If nodata_mode is True, the nodata value will be return if any neighbor has nodata value. Otherwise, neighboring
    nodata cells are ignored.
    """
    org_val = block.value(row, col)
    if org_val == nodata_value:
        return nodata_value
    max_row = block.height() - 1
    max_col = block.width() - 1
    if row == 0 or row == max_row or col == 0 or col == max_col:
        # the cell is at the edge of block - return the original value
        return org_val
    vals = []
    for r in (row - 1, row, row + 1):
        for c in (col - 1, col, col + 1):
            val = block.value(r, c)
            if val == nodata_value:
                if nodata_mode:
                    # return nodata if any neighbor has nodata value
                    return nodata_value
                else:
                    continue
            vals.append(val)
    if len(vals) == 0:
        new_val = nodata_value
    else:
        new_val = sum(vals) / len(vals)
    return new_val


def check_gdal_driver_create_option(layer):
    """Check if GDAL can create dataset using the layer's GDAL driver - if yes, Serval can work with the raster."""
    try:
        dataset = gdal.Open(layer.dataProvider().dataSourceUri(), gdal.GA_ReadOnly)
        band = dataset.GetRasterBand(1)
        if band is None:
            return False
        temp_dir = tempfile.mkdtemp()
        test_path = os.path.join(temp_dir, "test")
        test_dataset = dataset.GetDriver().Create(test_path, 1, 1, band.DataType)
        return test_dataset is not None
    except RuntimeError:
        return False
