import numpy as np

def compute_rmse(y_pred, y_true):
    return np.sqrt(((y_pred - y_true) ** 2).mean())

def compute_mse(y_pred, y_true):
    return np.array(((y_pred - y_true) ** 2).mean())
