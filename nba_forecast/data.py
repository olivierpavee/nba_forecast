#from sklearn.model_selection import train_test_split
#from google.cloud import storage
import pandas as pd
import os
CURRENT_PATH = os.getcwd()

def get_data_using_pandas(name_dataset):

    if name_dataset == 'po2011':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/pick_order_2011.csv")

    if name_dataset == 'po2021':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/pick_order_2021.csv")

    if name_dataset == 'dataset_train':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/dataset_complet_X_y.csv")

    if name_dataset == 'dataset_draft_2021':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/univ_data_2021.csv")

    if name_dataset == 'dataset1':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/")

    return df
