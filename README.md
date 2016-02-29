# Serval

Serval is a QGIS plugin for setting raster cell values. 

**Warning**: Any changes are immediately written to disk. Make a copy of your precious raster.

## How to use

![Serval](https://raw.githubusercontent.com/erpas/serval/master/help/source/img/serval_rgb.png)

1. Select a raster in the layers panel.
1. Pick the plugin maptool (if Serval dock widget is not visible, turn it on in View > Panels)
1. Choose the plugin mode:
  * probing or
  * drawing

### Probing mode
When a raster cell is clicked bands values are shown in spin box(es). Change them and hit Enter. Done.

### Drawing mode
Set bands values and click raster cells that should get the values. For 3 bands rasters a color can be chosen from native QGIS color picker.

## Projections
Serval can work with the OTF reprojections. Nevertheless, it is advised that the raster and project CRS are the same. 

## NoData values
The plugin tries to get NoData value defined for each band. If it fails, the value of -9999 is defined and written as a new NoData value.

## Known issues

On Windows GDAL Python API objects (gdal_array namely) are not properly deleted on plugin unload when closing QGIS and that causes Python to crash. See QGIS issue [#13061](http://hub.qgis.org/issues/13061).

## License

Serval is a free/libre software and is licensed under the GNU General Public License.
