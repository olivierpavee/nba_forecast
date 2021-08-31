import pandas as pd
import os
CURRENT_PATH = os.getcwd()

def get_data_using_pandas(name_dataset):

    if name_dataset == 'po2011':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/pick_order_2011.csv")

    elif name_dataset == 'po2021':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/pick_order_2021.csv")

    elif name_dataset == 'dataset_draft_2021':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/univ_data_2021.csv")

    elif name_dataset == 'train':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/common_dataset.csv")
    elif name_dataset == 'train_risk':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/risk_dataset.csv")
    
    return df

def filter_data(df,type):
    #returns a dataset with only the features needed (offensive ratio prediction or defensive ratio prediction)
    off_features = ['mp', 'gs_pct', 'last_uni_age', 'pos', 'per','ts_pct','fg3a_per_fga_pct','fta_per_fga_pct',\
                    'orb_pct','ast_pct','tov_pct','usg_pct','ows','obpm']

    def_features = ['mp', 'gs_pct', 'last_uni_age', 'pos', 'stl_pct','blk_pct','dws','drb_pct','dbpm']

    athletics_features = [  'body_fat_pct', 'hand_length', 'hand_width', 'height_wo_shoes',\
                            'height_w_shoes', 'standing_reach', 'weight', 'wingspan']
    
    risk_features = [ 'mp','per','ts_pct','efg_pct','fg3a_per_fga_pct','fta_per_fga_pct',
          'orb_pct','drb_pct','ast_pct','stl_pct','blk_pct','tov_pct','usg_pct','ows','dws','obpm','dbpm','years']

    if type == 'model_off':
        #return dataset with offensive and atheltics features (discard defensive features)
        df_off = df[off_features+athletics_features].copy()
        #convert numerical features to float64 to match KNN imputer params
        to_be_converted = [ 'gs_pct','mp','last_uni_age','hand_length','hand_width',\
                            'height_w_shoes','height_wo_shoes','standing_reach','wingspan']

        for column in to_be_converted:
            df_off[column] = df_off[column].astype('float64')

        return df_off

    elif type == 'model_def':
        #return dataset with defensive and atheltics features (discard offensive features)
        df_def = df[def_features+athletics_features].copy()
        df_def = pd.get_dummies(df)
        return df_def
    
    elif type == 'model_risk':
        #return dataset with features used for risk factor prediction
        df_risk = df[risk_features].copy()
        return df_risk

if __name__ == '__main__':
    df = get_data_using_pandas('train')
    print(df)