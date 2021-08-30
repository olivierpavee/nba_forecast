from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge



def get_model(name_model):

    if name_model == 'Ridge':
        model = Ridge()

    return model
