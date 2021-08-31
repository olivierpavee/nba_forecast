import numpy as np

def compute_mse(y_pred, y_true):
    return np.array(((y_pred - y_true) ** 2).mean())
