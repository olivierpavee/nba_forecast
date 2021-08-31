from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder, MinMaxScaler
from nba_forecast.data import get_data_using_pandas, filter_data
from nba_forecast.model import get_model
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import VarianceThreshold
from metrics import compute_mse
import joblib

class Trainer():
    def __init__(self, model_type):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.model_type = model_type
        self.pipeline = None

        data = get_data_using_pandas('train')
        self.X = filter_data(data,model_type)        

        if model_type == 'model_off':            
            self.y = data['ratio_off']
        elif model_type == 'model_def':
            self.y = data['ratio_def']
        elif model_type == 'model_risk':
            #TO BE DONE
            self.y = []

        self.model = get_model(model_type)

    def set_pipeline(self):
        """defines the pipeline as a class attribute"""
        #PIPELINE MODELE DEF
        if self.model_type == 'model_def':
            self.pipeline = Pipeline([
                ('rob_scaler', RobustScaler()),
                ('random_forest',self.model)
            ])

        #PIPELINE MODELE OFF
        elif self.model_type == 'model_off':
            preproc_categorical = Pipeline([
                ('simple_imp', SimpleImputer(strategy="most_frequent")),
                ('one_hot_enc', OneHotEncoder(handle_unknown="ignore"))
            ])

            numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
            feat_numerical = sorted(self.X.select_dtypes(include=numerics).columns)

            preproc_numerical = Pipeline([
                ('knn_imp', KNNImputer(missing_values=0.0)),
                ('minmax', MinMaxScaler())
            ])

            preproc_transformer = ColumnTransformer([
                ('preproc_num', preproc_numerical, feat_numerical),
                ('preproc_cat', preproc_categorical, ['pos'])
                ], remainder="drop")
            
            variance_threshold_pipe = VarianceThreshold(threshold=0.01)

            self.pipe = Pipeline([
                ('preproc', preproc_transformer),
                ('var', variance_threshold_pipe),
                ('ridge', self.model)
            ])

        elif self.model_type == 'model_risk':
            #TO BE DONE
            pass

    def run(self):
        """set and train the pipeline"""
        self.set_pipeline(self.model)
        self.pipeline.fit(self.X, self.y)

    def evaluate(self, X_test, y_test):
        """evaluates the pipeline on df_test and return the RMSE"""
        y_pred = self.pipeline.predict(X_test)
        rmse = compute_mse(y_pred, y_test)
        return rmse

    def save_model(self):
        """ Save the trained model into a model.joblib file """
        filename = 'model.joblib'
        joblib.dump(self.pipeline, filename)