from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge



def get_model(name_model):

    if name_model == 'Ridge':
        model = Ridge()

    elif name_model == 'off':
        model = RandomForestRegressor(
                    max_depth=1, 
                    min_samples_leaf=4, 
                    min_samples_split=5,
                    n_estimators=15
                    )

    return model
