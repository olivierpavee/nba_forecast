from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import LogisticRegression

def get_model(model_type):
    #build model depending of the parameter 'name_model' 
    # => offensive rate prediction / defensive rate prediction / risk factor computation
    if model_type == 'model_off':
        model = Ridge(
                    alpha = 1.2,
                    solver ='sag',
                    tol = 0.1
                    )

    elif model_type == 'model_def':
        model = RandomForestRegressor(
                    max_depth=1, 
                    min_samples_leaf=4, 
                    min_samples_split=5,
                    n_estimators=15
                    )
    elif model_type == 'model_risk':
        model = LogisticRegression(max_iter=300)

    return model
