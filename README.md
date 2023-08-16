# Serval

Serval is a QGIS plugin for raster editing. 
It provides convenient tools for modifying (small) raster parts and is _not_ intended to process entire images - 
use Raster Calculator for this.
Users can select some portions of a raster and apply one of the following modifications to selected cells:
* set a constant value, including NoData,
* apply a QGIS expression value,
* apply 3x3 low-pass filter,
* undo / redo.

Raster cell selection tools include:
* line selection with configurable width,
* polygon selection,
* loading selection from a vector map layer.

Multi-band rasters are fully supported - users can modify each band separately, or as RGB in case of 3/4-bands rasters.

Probing raster tool and drawing tool (changing single cell value) are also available.

For more details, see [User Manual](./Serval/docs/user_manual.md). The [wiki page](https://github.com/lutraconsulting/serval/wiki) is now outdated. To be updated soon...

> Serval is a plugin for editing any type of raster layer, but if you want to edit thematic or categorical rasters,
> there is a specific plugin for that called [ThRasE](https://smbyc.github.io/ThRasE).

## License

Serval is a free/libre software and is licensed under the [GNU General Public License](./Serval/license.md).
