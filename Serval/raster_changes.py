from qgis.PyQt.QtCore import QObject


class RasterChange(object):
    """Class for storing a change made to raster, i.e. raster blocks before and after the change."""

    def __init__(self, active_bands, row, col, old_blocks, new_blocks):
        self.active_bands = active_bands  # list of bands for the change
        self.row = row  # top left row and col of the blocks with changes
        self.col = col
        self.old_blocks = old_blocks  # list of blocks for each raster band
        self.new_blocks = new_blocks

    def get_undo(self):
        return self.active_bands, self.row, self.col, self.old_blocks

    def get_redo(self):
        return self.active_bands, self.row, self.col, self.new_blocks


class RasterChanges(QObject):
    """Class for managing changes made to a raster."""

    def __init__(self, nr_to_keep=3):
        super(RasterChanges, self).__init__()
        self.undos = []  # list of RasterChange objects
        self.redos = []
        self.nr_to_keep = nr_to_keep

    def clear(self):
        self.undos = []
        self.redos = []

    def add_change(self, change):
        keep = max(0, self.nr_to_keep - 1)
        self.undos = self.undos[-keep:]
        self.undos.append(change)
        self.redos = []

    def undo(self):
        last_change = self.undos.pop()
        keep = max(0, self.nr_to_keep - 1)
        self.redos = self.redos[-keep:]
        self.redos.append(last_change)
        return last_change.get_undo()

    def redo(self):
        last_change = self.redos.pop()
        self.undos.append(last_change)
        return last_change.get_redo()

    def nr_undos(self):
        return len(self.undos)

    def nr_redos(self):
        return len(self.redos)
