import streamlit as st
from nba_forecast.data import get_data_using_pandas
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

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
