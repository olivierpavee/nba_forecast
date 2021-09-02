from pandas.core.dtypes.missing import isna
import streamlit as st
from nba_forecast.data import get_data_using_pandas
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import joblib
import os
import math

CURRENT_PATH = os.getcwd()

def get_list_team(year):
    if year == 2011:
        dataFrame = get_data_using_pandas('po2011')
    if year == 2021:
        dataFrame = get_data_using_pandas('po2021')

    dataFrame['team_to_select'] = dataFrame.apply(lambda row:f"{row.team_name} ({row.team})", axis=1)
    return dataFrame['team_to_select'].sort_values().tolist()


def get_stat_team(team_name, year_draft):
        scaler = MinMaxScaler()
        if year_draft == 2011:
            dataFrame = get_data_using_pandas('team_stats_2011').drop(['off_rank','def_rank'], axis=1)
        if year_draft == 2021:
            dataFrame = get_data_using_pandas('team_stats_2021').drop(['off_rank','def_rank'], axis=1)

        dataFrame['def_rtg'] = 1/dataFrame['def_rtg']
        dataFrame['attendance'] = dataFrame['attendance'].apply(lambda x:x.replace(',',''))

        features = list(dataFrame)[1:]
        scaled_values = scaler.fit_transform(dataFrame.drop(['Team'], axis=1))

        scaled_df = pd.DataFrame(scaled_values, columns=features)
        scaled_df["Team"] = dataFrame["Team"]
        #print(scaled_df)

        scaled_df.rename(columns={"expected_winrate": "Expected Winrate", "attendance": "Attendance", "pace": "Pace", "def_rtg": "Defense", "off_rtg": "Attack"}, inplace=True)

        row = scaled_df[scaled_df['Team'] == team_name]
        return row

def get_teams(year):
    #retrieve file referencing NBA teams with their statistics of given year
    team_file = 'team_stats_' + str(year) + '.csv'
    return pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/{team_file}")

def get_players(year):
    #retrieve dataframe of NBA players to be drafted that year 
    player_file = 'dataset_' + str(year) + '.csv'                               
    return pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/{player_file}") 


def get_team_ratings(df,team):
    #fetch stats of the team we are interested in
    team_stats = df.loc[df['Team'] == team]
    # print(team_stats)
    # print(team_stats.values.flatten().tolist())
    team_stats_list = team_stats.values.flatten().tolist()

    # team_off_rating = team_stats_list[1]
    # team_def_rating = team_stats_list[2]
    return team_stats_list[1], team_stats_list[2]


def split_dataframe(players_df):
    #define features for each model
    off_features = ['mp', 'gs_pct', 'last_uni_age', 'pos', 'per','ts_pct','fg3a_per_fga_pct','fta_per_fga_pct',\
                    'orb_pct','ast_pct','tov_pct','usg_pct','ows','obpm']

    def_features = ['mp', 'gs_pct', 'last_uni_age', 'pos', 'stl_pct','blk_pct','dws','drb_pct','dbpm']

    athletics_features = [  'body_fat_pct', 'hand_length', 'hand_width', 'height_wo_shoes',\
                            'height_w_shoes', 'standing_reach', 'weight', 'wingspan']
    
    risk_features = [ 'mp','per','ts_pct','fg3a_per_fga_pct','fta_per_fga_pct',
          'orb_pct','drb_pct','ast_pct','stl_pct','blk_pct','tov_pct','usg_pct','ows','dws','obpm','dbpm','years']

    #convert features to meet pipelines requirements
    to_be_converted = [ 'gs_pct','mp','last_uni_age','hand_length','hand_width',\
                            'height_w_shoes','height_wo_shoes','standing_reach','wingspan']
    for column in to_be_converted:
        players_df[column] = players_df[column].astype('float64')

    off_df = players_df[off_features+athletics_features]
    def_df = pd.get_dummies(players_df[def_features+athletics_features])
    risk_df = players_df[risk_features]

    return off_df, def_df, risk_df


def reco_by_pos(year, team, pos='*'):
    #retrieve file referencing NBA teams with their statistics of given year
    teams_df = get_teams(year)
    team_off_rating, team_def_rating = get_team_ratings(teams_df,team)

    #fetch stats of the team we are interested in
    players_df = get_players(year)
    # print(players_df.head())

    #retrieve models
    model_off = joblib.load('model_off.joblib')
    model_def = joblib.load('model_def.joblib')
    model_risk = joblib.load('model_risk.joblib')

    #get our three dataframes for predictions
    off_df, def_df, risk_df = split_dataframe(players_df)

    #get models predictions for all dataset
    ratio_off_preds = model_off.predict(off_df)
    ratio_def_preds = model_def.predict(def_df)
    risk_proba = model_risk.predict_proba(risk_df)[:,1:].reshape(-1)


    #build dataframe with scores
    displayed_features = ['player_name','school_name','uni_off_score','uni_def_score','height_w_shoes','weight', 'pos', 'years']
    final_df = players_df[displayed_features]

    #intermediate columns for fit score computation (dropped at the end of treatment)
    final_df['ratio_off_preds'] = ratio_off_preds
    final_df['ratio_def_preds'] = ratio_def_preds
    final_df['risk_proba'] = risk_proba

    #compute fit score
    final_df['fit_score']=( final_df['ratio_off_preds'] * final_df['uni_off_score'] * team_off_rating\
                        + final_df['ratio_def_preds'] * final_df['uni_def_score'] * team_def_rating )\
                             * final_df['risk_proba'] / (final_df['years']**(1/3))

    #keep only desired position
    if pos != '*':
        final_df = final_df[final_df['pos'] == str(pos)]

    #drop columns we don't need anymore and keep top five
    final_df = final_df.drop(columns=['ratio_off_preds', 'ratio_def_preds', 'years']).sort_values(by='fit_score', ascending=False).head(5)

    print(final_df)
    return final_df.to_dict('records')

def mock_draft(year):
    pick_order_position=[('CLE','PG'), ('MIN','PF'), ('UTA','SG'), ('DET','SF'), ('TOR','SF'), ('WAS','PF'), ('SAC','SG'),
        ('CHO','PG'), ('MIL','SG'), ('GSW','SG'), ('PHO','PF'), ('HOU','SF'), ('IND','SF'), ('PHI','C'), ('NYK','SG'),
        ('POR','PG'), ('DEN','PF'), ('OKC','PG'), ('BOS','SG'), ('DAL','SF'), ('BRK','PF'), ('CHI','PG'),('SAS','PG'),
        ('MIA','SF'), ('LAC','*'), ('LAL','PG'), ('IND','PF'), ('MEM','PG'), ('ORL','SG'), ('NOP','C')
    ]


    teams_df = get_teams(year)
    players_df = get_players(year)
    draft_2011 = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/draft_2011.csv")    
    draft_2011.columns = ['player_name', 'pick rank', 'year', 'college', 'ws', 'url', 'height (cm)',
       'weight (lb)', 'uni_url', 'player_id']
    players_df = players_df.merge(draft_2011[['player_name','pick rank','ws']], how='inner' ,on='player_name')

    #retrieve models
    model_off = joblib.load('model_off.joblib')
    model_def = joblib.load('model_def.joblib')
    model_risk = joblib.load('model_risk.joblib')

    draft = []
    for team,pos in pick_order_position:
        
        team_off_rating, team_def_rating = get_team_ratings(teams_df,team)
        off_df, def_df, risk_df = split_dataframe(players_df)
        
        ratio_off_preds = model_off.predict(off_df)
        ratio_def_preds = model_def.predict(def_df)
        risk_proba = model_risk.predict_proba(risk_df)[:,1:].reshape(-1)
        
        displayed_features = ['player_name','school_name','uni_off_score','uni_def_score','height_w_shoes','weight', 'pos', 'years',
                                'pick rank', 'ws']
        final_df = players_df[displayed_features].copy()

        #intermediate columns for fit score computation (dropped at the end of treatment)
        final_df['ratio_off_preds'] = ratio_off_preds
        final_df['ratio_def_preds'] = ratio_def_preds
        final_df['risk_proba'] = risk_proba
        #compute fit score
        final_df['fit_score']=( final_df['ratio_off_preds'] * final_df['uni_off_score'] * team_off_rating\
                        + final_df['ratio_def_preds'] * final_df['uni_def_score'] * team_def_rating )\
                        * final_df['risk_proba'] / (final_df['years']**(1/3))
        
        if pos != '*':
            final_df = final_df[final_df['pos'] == str(pos)]

        final_df = final_df.drop(columns=['ratio_off_preds', 'ratio_def_preds', 'years']).sort_values(by='fit_score', ascending=False).head(1)
        name = final_df['player_name'].iloc[0]
        pick_rank = final_df['pick rank'].iloc[0]
        if math.isnan(final_df['ws'].iloc[0]) :
            ws = 0.0
        else:
            ws = final_df['ws'].iloc[0]

        draft.append(
            {   
                'Team': team,
                'Player': name,
                'pick_rank':pick_rank,
                'ws':ws
            }
        )

        #remove player from initial dataframe for new pick
        players_df = players_df.drop(players_df[players_df['player_name'] == name].index)
    
    return draft

if __name__ == "__main__":
    # reco_by_pos(2011,'BOS', 'SF')
    mock_draft(2011)
