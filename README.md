# Serval

Serval is a QGIS plugin for setting raster pixel value. Currently single banded rasters are supported.

## How to use

![Serval](https://raw.githubusercontent.com/erpas/serval/master/help/source/img/serval_example.png)

Any changes are immediately written to disk. Make a copy of your precious raster.

1. Choose a raster to modify (refresh the list if needed). The rasters list contains only **editable** rasters with a **projection assigned**.
1. Pick the plugin maptool. 
1. Click on a pixel.
1. Give it a new value and hit Enter (or the green arrow button).

That's it.

## Known issues

On Windows objects of GDAL Python API are not properly deleted on plugin unload when closing QGIS and that causes Python to crash.
See QGIS issue [#13061](http://hub.qgis.org/issues/13061).

## License

Serval is a free/libre software and is licensed under the GNU General Public License.