import pyqtgraph as pg
import numpy as np

class CustomAxis(pg.AxisItem):
    def __init__(self, ydict, *arg, **kwarg):
        super(CustomAxis, self).__init__(*arg, **kwarg)
        self.y_values = np.asarray(ydict.keys())
        self.y_string = ydict.values()

    def tickStrings(self, values, scale, spacing):
        res = super(CustomAxis, self).tickStrings(values, scale, spacing)
        return res

