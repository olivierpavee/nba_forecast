import streamlit as st
from nba_forecast.data import get_data_using_pandas
import pandas as pd
import joblib
import os

CURRENT_PATH = os.getcwd()

def get_list_team(year):
    if year == 2011:
        dataFrame = get_data_using_pandas('po2011')
    if year == 2021:
        dataFrame = get_data_using_pandas('po2021')

    dataFrame['team_to_select'] = dataFrame.apply(lambda row:f"{row.team_name} ({row.team})", axis=1)
    return dataFrame['team_to_select'].sort_values().tolist()

def recommandation(year, team):
    prediction_table = st.expander('Discover our predictions !')
    with prediction_table:
        st.text(year)
        st.text(team)
        col3, col4 = st.columns([1,1])
        col5, col6 = st.columns([1,1])
        col7, col8 = st.columns([1,1])
        col9, col10 = st.columns([1,1])

        col3.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

        col4.success('Top 1')
        col4.text('James Harden')
        col4.text('Def score :')
        col4.text('Off score :')

        col5.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

        col6.success('Top 2')
        col6.text('James Harden')
        col6.text('Def score :')
        col6.text('Off score :')

        col7.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

        col8.warning('Top 2')
        col8.text('James Harden')
        col8.text('Def score :')
        col8.text('Off score :')

        col9.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

        col10.error('Top 5')
        col10.text('James Harden')
        col10.text('Def score :')
        col10.text('Off score :')

    return prediction_table

def reco_by_pos(year, team, pos):
    #retrieve file referencing NBA teams with their statistics of given year
    team_file = 'team_stats_' + str(year) + '.csv'
    teams_df = pd.read_csv(f"{CURRENT_PATH}/nba_forecast/data/{team_file}")

    #fetch stats of the team we are interested in
    team_stats = teams_df.loc[teams_df['Team'] == team]
    print(team_stats)
    print(team_stats.values.flatten().tolist())
    team_stats_list = team_stats.values.flatten().tolist()
    team_off_rating = team_stats_list[1]
    team_def_rating = team_stats_list[2]

    #retrieve dataframe of NBA players to be drafted that year
    # player_file = 
    pass

if __name__ == "__main__":
    reco_by_pos(2011,'BOS','C')