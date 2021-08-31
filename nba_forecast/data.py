import pandas as pd
import os
CURRENT_PATH = os.getcwd()

def get_data_using_pandas(name_dataset):

    if name_dataset == 'po2011':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/pick_order_2011.csv")
        df = df.append({'pick_order':'99','team':'Choose a team!','team_name':2011}, ignore_index=True)

    elif name_dataset == 'po2021':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/pick_order_2021.csv")
        df = df.append({'pick_order':'99','team':'Choose a team!','team_name':2021}, ignore_index=True)

    elif name_dataset == 'dataset_draft_2021':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/univ_data_2021.csv")

    elif name_dataset == 'train':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/common_dataset.csv")

    elif name_dataset == 'team_stats_2021':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/team_stats_2021.csv")

    elif name_dataset == 'team_stats_2011':
        df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/team_stats_2011.csv")

    return df

def filter_data(df,type):
    #returns a dataset with only the features needed (offensive ratio prediction or defensive ratio prediction)
    off_features = ['gs_pct', 'last_uni_age', 'pos', 'per','ts_pct','fg3a_per_fga_pct','fta_per_fga_pct',\
                    'orb_pct','ast_pct','tov_pct','usg_pct','ows','obpm']

    def_features = ['gs_pct', 'last_uni_age', 'pos', 'stl_pct','blk_pct','dws','drb_pct','dbpm']

    athletics_features = [  'body_fat_pct', 'hand_length', 'hand_width', 'height_wo_shoes',\
                            'height_w_shoes', 'standing_reach', 'weight', 'wingspan']
    
    risk_features = [ 'mp','per','ts_pct','efg_pct','fg3a_per_fga_pct','fta_per_fga_pct',
          'orb_pct','drb_pct','ast_pct','stl_pct','blk_pct','tov_pct','usg_pct','ows','dws','obpm','dbpm','years']

    if type == 'model_off':
        #return dataset with offensive and atheltics features (discard defensive features)
        df = df[off_features+athletics_features]
        #convert numerical features to float64 to match KNN imputer params
        to_be_converted = [ 'gs_pct','mp','nb_year_uni','hand_length','hand_width',\
                            'height_w_shoes','height_wo_shoes','standing_reach','wingspan']
        for column in to_be_converted:
            df[column] = df[column].astype('float64')

        return df

    elif type == 'model_def':
        #return dataset with defensive and atheltics features (discard offensive features)
        df = df[def_features+athletics_features]
        df = pd.get_dummies(df)
        return df
    
    elif type == 'model_risk':
        #return dataset with features used for risk factor prediction
        df = df[risk_features]
        return df

if __name__ == '__main__':
    df = get_data_using_pandas('train')
    print(df)
