import streamlit as st
from nba_forecast.data import get_data_using_pandas
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import joblib
import os
import requests
from bs4 import BeautifulSoup

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

def reco_by_pos(year, team, pos):
    #retrieve file referencing NBA teams with their statistics of given year
    team_file = 'team_stats_' + str(year) + '.csv'
    teams_df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/{team_file}")

    #fetch stats of the team we are interested in
    team_stats = teams_df.loc[teams_df['Team'] == team]
    # print(team_stats)
    # print(team_stats.values.flatten().tolist())
    team_stats_list = team_stats.values.flatten().tolist()
    team_off_rating = team_stats_list[1]
    team_def_rating = team_stats_list[2]

    #retrieve dataframe of NBA players to be drafted that year
    player_file = 'dataset_' + str(year) + '.csv'                               #TO BE REVIEWED
    players_df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/{player_file}") #TO BE REVIEWED

    # print(players_df.head())

    #retrieve models
    model_off = joblib.load('model_off.joblib')
    model_def = joblib.load('model_def.joblib')
    model_risk = joblib.load('model_risk.joblib')

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


    #get models predictions for all dataset
    ratio_off_preds = model_off.predict(players_df[off_features+athletics_features])

    ratio_def_preds = model_def.predict(pd.get_dummies(players_df[def_features+athletics_features]))

    risk_proba = model_risk.predict_proba(players_df[risk_features])
    risk_proba = risk_proba[:,1:].reshape(-1)

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
    final_df = final_df[final_df['pos'] == str(pos)]
    # print(final_df[['player_name','ratio_off_preds','ratio_def_preds','risk_proba','fit_score']].sort_values(by='fit_score',ascending=False))

    #drop columns we don't need anymore and keep top five
    final_df = final_df.drop(columns=['ratio_off_preds', 'ratio_def_preds', 'years']).sort_values(by='fit_score', ascending=False).head(5)

    # print(final_df.to_dict('records'))
    # print(len(final_df.to_dict('records')))
    return final_df.to_dict('records')

def get_img_player(player_name,draft_year):

    player_name = '-'.join(player_name.lower().split(' '))

    if draft_year == 2011:
        result = get_player_draft_2011(player_name)
        #print(result)
        if result == None:
            return 'https://www.mecafroid.fr/images/virtuemart/typeless/photo-produit-indisponible-meca-froid_250x285.jpg'
        else:
            #print(requests.get('https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{result}.png').content)
            return f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{result}.png'


    if draft_year == 2021:
        try:
            r = requests.get(f'https://www.nba.com/draft/2021/prospects/{player_name}')
            soup = BeautifulSoup(r.content, "html.parser")
            return soup.find_all('img', class_='opacity-0')[0]['src']
        except:
            return 'https://www.mecafroid.fr/images/virtuemart/typeless/photo-produit-indisponible-meca-froid_250x285.jpg'


def get_player_draft_2011(player_name):
    list_player_draft_2011 = ['Kyrie Irving',
'Derrick Williams',
'Enes Kanter',
'Tristan Thompson',
'Jonas Valanciunas',
'Jan Vesely',
'Bismack Biyombo',
'Brandon Knight',
'Kemba Walker',
'Jimmer Fredette',
'Klay Thompson',
'Alec Burks',
'Markieff Morris',
'Marcus Morris Sr.',
'Kawhi Leonard',
'Nikola Vucevic',
'Iman Shumpert',
'Chris Singleton',
'Tobias Harris',
'Donatas Motiejunas',
'Nolan Smith',
'Kenneth Faried',
'Nikola Mirotic',
'Reggie Jackson',
'MarShon Brooks',
'Jordan Hamilton',
'JaJuan Johnson',
'Norris Cole',
'Cory Joseph',
'Jimmy Butler',
'Bojan Bogdanovic',
'Justin Harper',
'Kyle Singler',
'Shelvin Mack',
'Tyler Honeycutt',
'Jordan Williams',
'Trey Thompkins',
'Chandler Parsons',
'Jeremy Tyler',
'Jon Leuer',
'Darius Morris',
'Davis Bertans',
'Malcolm Lee',
'Charles Jenkins',
'Josh Harrellson',
'Andrew Goudelock',
'Travis Leslie',
'Keith Benson',
'Josh Selby',
'Lavoy Allen',
'Jon Diebler',
'Vernon Macklin',
'DeAndre Liggins',
#MIlan Macvan
"E'Twaun Moore",
#Chukwudiebere Maduabum
#Tanguy Ngombo
#Ater Majok
#Adam Hanga
'Isaiah Thomas']
    list_player_draft_2011_format = ['-'.join(x.lower().split(' ')) for x in list_player_draft_2011]
    player_name_format = '-'.join(player_name.lower().split(' '))

    if player_name_format in list_player_draft_2011_format:
        for idx, val in enumerate(list_player_draft_2011_format, start=202681):
            if val == player_name_format:
                return idx
    return None



if __name__ == "__main__":
    reco_by_pos(2011,'BOS','SF')
