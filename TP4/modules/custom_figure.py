from TP4.modules.base.base_plot import BasePlot


class GenericPlot(BasePlot):
    """
    BasicBarPlot class implementation
    """

    def __init__(self, **params):
        """
        Constructor of BasicBarPlot class

        :param colors : str
            color of the bars
        :param params: inherited args
        """
        super().__init__(**params)
