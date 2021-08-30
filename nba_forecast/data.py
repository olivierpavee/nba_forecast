#from sklearn.model_selection import train_test_split
#from google.cloud import storage
import pandas as pd


def get_data_using_pandas(name_dataset):

    if name_dataset == 'dataset1':
        df = pd.read_csv("gs://le-wagon-data/data/train_1k.csv", nrows=line_count)
    if name_dataset == 'dataset1':
        df = pd.read_csv("gs://le-wagon-data/data/train_1k.csv", nrows=line_count)
    if name_dataset == 'dataset1':
        df = pd.read_csv("gs://le-wagon-data/data/train_1k.csv", nrows=line_count)
    if name_dataset == 'dataset1':
        df = pd.read_csv("gs://le-wagon-data/data/train_1k.csv", nrows=line_count)
    return df
