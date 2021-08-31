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

def filter_data(df,stat):
    #returns a dataset with only the features needed (offensive ratio prediction or defensive ratio prediction)
    off_features = ['last_uni_age', 'pos', 'per','ts_pct','fg3a_per_fga_pct','fta_per_fga_pct',\
                    'orb_pct','ast_pct','tov_pct','usg_pct','ows','obpm']

    def_features = ['last_uni_age', 'pos', 'stl_pct','blk_pct','dws','drb_pct','dbpm']

    athletics_features = [  'body_fat_pct', 'hand_length', 'hand_width', 'height_wo_shoes',\
                            'height_w_shoes', 'standing_reach', 'weight', 'wingspan']

    if stat == 'off':
        df = df[off_features+athletics_features]
        return df

    elif stat == 'def':
        #return dataset with defensive and atheltics features (discard offensive features)
        df = df[def_features+athletics_features]
        df = pd.get_dummies(df)
        return df[def_features+athletics_features]
