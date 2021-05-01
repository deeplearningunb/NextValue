DEFAULT_DAYS = 5
DEFAULT_OPTIMIZER = "adam"
DEFAULT_LOSS = "mean_squared_error"
DEFAULT_EPOCHS = 300
DEFAULT_BATCH_SIZE = 96


class Layer:
    def __init__(self, units, dropout):
        self.units = units
        self.dropout = dropout


DEFAULT_LAYERS = [
    Layer(units=300, dropout=0.2)
]