from qgis.core import *
from qgis.utils import plugins


@qgsfunction(args='auto', group='Serval', usesgeometry=True)
def nearest_feature_attr_value(vlayer_id, attr_name, feature, parent):
    """
    Find the nearest feature from given vector layer and return its attribute value.

    <h4>Syntax</h4><div class=\"syntax\">
    <code>
        <span class=\"functionname\">nearest_feature_attr_value</span> (
        <span class=\"argument\">vlayer_id</span>,
        <span class=\"argument\">attr_name</span> )
    </code>
    </div>

    <h4>Arguments</h4>
    <div class=\"arguments\">
        <table>
            <tr><td class=\"argument\">vlayer_id</td><td>linestring vector layer id  - get it from Map Layers group</td></tr>
            <tr><td class=\"argument\">attr_name</td><td>name of attribute with the value to get</td></tr>
        </table>
    </div>

    <h4>Examples</h4>
        <div class=\"examples\"><ul>
            <li>
                <code>nearest_feature_attr_value('lines_1e2812c5_1234_4ba4_81e1_64fd10af7acd', 'depth')</code>
                &rarr;
                <code>1234.56</code>
            </li>
        </ul></div>
    """
    plugin = plugins["Serval"]
    return plugin.nearest_feature_attr_value(feature, vlayer_id, attr_name)


@qgsfunction(args='auto', group='Serval', usesgeometry=True)
def nearest_pt_on_line_interpolate_z(vlayer_id, feature, parent):
    """
    Find the nearest feature from a linestring vector layer and interpolate z value at point closest to current geometry.

    <h4>Syntax</h4><div class=\"syntax\">
    <code>
        <span class=\"functionname\">nearest_pt_on_line_interpolate_z</span> ( <span class=\"argument\">vlayer_id</span> )
    </code>
    </div>

    <h4>Arguments</h4>
    <div class=\"arguments\">
        <table>
            <tr><td class=\"argument\">vlayer_id</td><td>linestring vector layer id  - get it from Map Layers group</td></tr>
        </table>
    </div>

    <h4>Examples</h4>
        <div class=\"examples\"><ul>
            <li>
                <code>nearest_pt_on_line_interpolate_z( 'lines_1e2812c5_62fb_4567_81e1_64fd10af7acd' )</code>
                &rarr;
                <code>123.45</code>
            </li>
        </ul></div>
    """
    plugin = plugins["Serval"]
    return plugin.nearest_pt_on_line_interpolate_z(feature, vlayer_id)


@qgsfunction(args='auto', group='Serval', usesgeometry=True)
def intersecting_features_attr_average(vlayer_id, attr_name, only_center, feature, parent):
    """
    For each cell selected, find features from the vector layer that intersects the cell and calculate arithmetic average of their attribute values.

    <h4>Syntax</h4><div class=\"syntax\">
    <code>
        <span class=\"functionname\">intersecting_features_attr_average</span> ( <span class=\"argument\">vlayer_id</span>,
        <span class=\"argument\">attr_name</span>,
        <span class=\"argument\">only_center</span> )
    </code>
    </div>

    <h4>Arguments</h4>
    <div class=\"arguments\">
        <table>
            <tr><td class=\"argument\">vlayer_id</td><td>a vector layer id  - get it from Map Layers group.</td></tr>
            <tr><td class=\"argument\">attr_name</td><td>name of attribute with the value to get.</td></tr>
            <tr><td class=\"argument\">only_center</td><td>boolean, if True only cell center is used to find intersecting features. If False, whole raster cell is used.</td></tr>
        </table>
    </div>

    <h4>Examples</h4>
        <div class=\"examples\"><ul>
            <li>
                <code>intersecting_features_attr_average( 'polygons_1e2812c5_62fb_1234_81e1_64fd10af7acd', 'height', False )</code>
                &rarr;
                <code>123.45</code>
            </li>
        </ul></div>
    """
    plugin = plugins["Serval"]
    return plugin.intersecting_features_attr_average(feature, vlayer_id, attr_name, only_center)


@qgsfunction(args='auto', group='Serval', usesgeometry=True)
def interpolate_from_mesh(mlayer_id, group, dataset, above_existing, feature, parent):
    """
    Interpolate value from mesh layer.

    <h4>Syntax</h4><div class=\"syntax\">
    <code>
        <span class=\"functionname\">interpolate_from_mesh</span> ( <span class=\"argument\">mlayer_id</span>,
        <span class=\"argument\">group</span>,
        <span class=\"argument\">dataset</span>,
        <span class=\"argument\">above_existing</span>)
    </code>
    </div>

    <h4>Arguments</h4>
    <div class=\"arguments\">
        <table>
            <tr><td class=\"argument\">mlayer_id</td><td>a mesh layer id  - get it from Map Layers group.</td></tr>
            <tr><td class=\"argument\">group</td><td> dataset group index, an integer.</td></tr>
            <tr><td class=\"argument\">dataset</td><td> dataset index in the group, an integer.</td></tr>
            <tr><td class=\"argument\">above_existing</td><td> if True, only take the interpolation result if it is greater than current raster value.</td></tr>
        </table>
    </div>

    <h4>Examples</h4>
        <div class=\"examples\"><ul>
            <li>
                <code>interpolate_from_mesh( 'mesh_1e2812c5_a34d_1234_81e1_64fd10af7acd', 0, 0, False )</code>
                &rarr;
                <code>151.45</code>
            </li>
        </ul></div>
    """
    plugin = plugins["Serval"]
    return plugin.interpolate_from_mesh(feature, mlayer_id, group, dataset, above_existing)
