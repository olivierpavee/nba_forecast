import streamlit as st
import datetime
import requests
import time
from load_css import local_css
from nba_forecast.app_utils import get_list_team, get_stat_team
import plotly.express as px
import plotly.graph_objects as go

#Chargement du style CSS
local_css("style.css")

if 'year_draft' not in st.session_state:
    st.session_state.year_draft = 0

if 'team_nba' not in st.session_state:
    st.session_state.team_nba = 'False'

if 'position' not in st.session_state:
    st.session_state.position = ''

# if 'team_nba' in st.session_state:
#     st.write(st.session_state.team_nba)

def YearDraftSelect(year):
    st.session_state.year_draft = year
    st.session_state.position = ''

#Chargement des DF avec le noms des équipes selon les années
#Chargement des titres
st.markdown('<center><h1 class="highlight black">Delphes Prediction</h1></center>', unsafe_allow_html=True)
st.markdown('<center>The Most Powerful NBA Predictor!</center>', unsafe_allow_html=True)
st.markdown('---', unsafe_allow_html=True)

# def main():
#Chargement du choix utilisateur
    #Image + titre

col3 = st.sidebar.columns([1])
#col1.image('https://pbs.twimg.com/media/EaAqhJEXgAAQuQ6?format=jpg&name=large', width=300)
#st.sidebar.image('img/boule_cristal.jpg', width=150)
#col2.markdown('<span class="highlight grey">For which year would you like a prediction?</span>', unsafe_allow_html=True)

    #Sélection d'une année
col1, col2 = st.sidebar.columns([1,1])
col1.button('2011', key='btn_2011', on_click=YearDraftSelect, args=(2011,))
col2.button('2021', key='btn_2021', on_click=YearDraftSelect, args=(2021,))

if st.session_state.year_draft == 2011:
    st.session_state.team_nba = st.sidebar.selectbox('Choose a team!', get_list_team(2011))
if st.session_state.year_draft == 2021:
    st.session_state.team_nba = st.sidebar.selectbox('Choose a team!', get_list_team(2021))


if st.session_state.team_nba not in ['2021 (Choose a team!)','2011 (Choose a team!)','False']:
    st.session_state.position = ''
    st.session_state.position = st.sidebar.selectbox('What position are you looking for?', ['Position', 'SF','BG','SG','PF','C'])
    team_acro = st.session_state.team_nba[-4:-1]
    year_draft = st.session_state.year_draft
    team_row_df = get_stat_team(team_acro, year_draft)
    #st.write(team_row_df)
    team_value = team_row_df.values.tolist()[0][:-1]
    team_label = team_row_df.columns.tolist()[:-1]
    fig_plotly = px.line_polar(team_row_df, r=team_value, theta=team_label, line_close=True)
    fig_plotly.update_traces(fill='toself')
    fig_plotly.update_layout(
                    polar = dict(
                        radialaxis = dict(tickvals=[0,1,2,3,4,5], showticklabels=False, ticks=''),
                        angularaxis = dict(showticklabels=True, ticks='')
                    )
)
    # fig_plotly = go.Figure(data=go.Scatterpolar(
    #                                     r=team_value,
    #                                     theta=team_label,
    #                                     fill='toself'
    # ))
    # fig_plotly.update_layout(
    #                     polar=dict(
    #                         radialaxis=dict(
    #                         visible=True
    #                         ),
    #                     ),
    #                     showlegend=False
    # )

    #herokuuuu COUOCUOCUOCUC


    st.plotly_chart(fig_plotly,use_container_width=True)

if st.session_state.position not in ['Position','']:
    with st.expander('Discover our predictions !'):
        st.write(st.session_state.team_nba)
        st.write(st.session_state.position)
        col3, col4 = st.columns([1,1])
        col5, col6 = st.columns([1,1])
        col7, col8 = st.columns([1,1])
        col9, col10 = st.columns([1,1])

        col3.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')
        col5.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')
        col7.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')
        col9.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

        col4.success('Top 1')
        col4.text('James Harden')
        col4.text('Def score :')
        col4.text('Off score :')

        # col5.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

        col6.success('Top 2')
        col6.text('James Harden')
        col6.text('Def score :')
        col6.text('Off score :')

        # col7.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

        col8.warning('Top 2')
        col8.text('James Harden')
        col8.text('Def score :')
        col8.text('Off score :')

        # col9.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

        col10.error('Top 5')
        col10.text('James Harden')
        col10.text('Def score :')
        col10.text('Off score :')



# if year_draft_2021:
#     team_nba = col2.selectbox('Select a team!', get_list_team(2021))
#     if team_nba:
#         recommandation(2021,team_nba)


# def recommandation():
#     with st.expander('Discover our predictions !'):
#         col3, col4 = st.columns([1,1])
#         col5, col6 = st.columns([1,1])
#         col7, col8 = st.columns([1,1])
#         col9, col10 = st.columns([1,1])

#         col3.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

#         col4.success('Top 1')
#         col4.text('James Harden')
#         col4.text('Def score :')
#         col4.text('Off score :')

#         col5.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

#         col6.success('Top 2')
#         col6.text('James Harden')
#         col6.text('Def score :')
#         col6.text('Off score :')

#         col7.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

#         col8.warning('Top 2')
#         col8.text('James Harden')
#         col8.text('Def score :')
#         col8.text('Off score :')

#         col9.image('https://www.basketball-reference.com/req/202106291/images/players/hardeja01.jpg')

#         col10.error('Top 5')
#         col10.text('James Harden')
#         col10.text('Def score :')
#         col10.text('Off score :')

# if lancement = True:
#     main()
#     lancement = False


# with st.empty():
#     for seconds in range(60):
#         st.write(f"⏳ {seconds} seconds have passed")
#         time.sleep(1)
#     st.write("✔️ 1 minute over!")
# #st.title('Delphes Prediction')

#st.text('The Most Powerful NBA Predictor!')




# pickup_date = st.date_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
# pickup_time = st.time_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
# pickup_datetime = f'{pickup_date} {pickup_time}'
# pickup_longitude = st.number_input('pickup longitude', value=40.7614327)
# pickup_latitude = st.number_input('pickup latitude', value=-73.9798156)
# dropoff_longitude = st.number_input('dropoff longitude', value=40.6413111)
# dropoff_latitude = st.number_input('dropoff latitude', value=-73.7803331)
# passenger_count = st.number_input('passenger_count', min_value=1, max_value=8, step=1, value=1)

# enter here the address of your flask api
# url = 'https://taxifare.lewagon.ai/predict'

# params = dict(
#     pickup_datetime=pickup_datetime,
#     pickup_longitude=pickup_longitude,
#     pickup_latitude=pickup_latitude,
#     dropoff_longitude=dropoff_longitude,
#     dropoff_latitude=dropoff_latitude,
#     passenger_count=passenger_count)

# response = requests.get(url, params=params)

# prediction = response.json()

# pred = prediction['prediction']

# pred
