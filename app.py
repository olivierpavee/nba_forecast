import streamlit as st
import datetime
import requests
import time
from load_css import local_css

local_css("style.css")


st.markdown('<center><h1 class="highlight black">Delphes Prediction</h1></center>', unsafe_allow_html=True)
st.markdown('<center>The Most Powerful NBA Predictor!</center>', unsafe_allow_html=True)
st.markdown('---', unsafe_allow_html=True)

col1, col2 = st.columns(2)

#col1.header("")
col1.image('https://pbs.twimg.com/media/EaAqhJEXgAAQuQ6?format=jpg&name=large', width=300)

col2.markdown('<h2 class="highlight grey">Choose your team:</h2>', unsafe_allow_html=True)
team_nba = col2.selectbox('Select', ['Houston','Lakers','Chicago Bulls'])

col21, col22 = st.columns([1,1])
year_draft_2011 = col2.button('2011')
year_draft_2021 = col2.button('2021')

st.text(year_draft_2011)
st.text(year_draft_2021)


with st.expander('Discover our predictions !'):
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
