import streamlit as st
from nba_forecast.data import get_data_using_pandas




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
