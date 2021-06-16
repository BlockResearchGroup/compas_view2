from .bufferobject import BufferObject


class PointObject(BufferObject):
    """Object for displaying COMPAS point geometry."""

    def __init__(self, data, color=None, size=10, **kwargs):
        super().__init__(data, show_points=True, pointsize=size, **kwargs)
        self.color = color

    def _points_data(self):
        positions = [self._data]
        colors = [self.color or self.default_color_points]
        elements = [[0]]
        return positions, colors, elements

    @property
    def editables(self):
        return {
            "x": {"type": "number"},
            "y": {"type": "number"},
            "z": {"type": "number"},
        }
