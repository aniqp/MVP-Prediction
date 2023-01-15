import streamlit as st
import pandas as pd
from web_scraping import *
import plotly.express as px
import time

#---------SETTINGS----------------#

page_icon = ":basketball:"
page_title = "MVP Predictor"
layout = "wide"

#---------------------#

st.set_page_config(page_title =page_title, page_icon = page_icon, layout=layout)
st.title(page_title + " " + page_icon)

col1, col2 = st.columns([0.3,1])
with col1:
    result = st.button("Predict MVPs ", help = "Predict the top 10 MVP candidates", on_click = get_top_10)
    if result:
        df = get_top_10()
        df.index += 1
        df.drop('predictions', axis = 1, inplace = True)
        st.write('')
        st.write('')
        st.write('')
        st.dataframe(df.style.format({'PTS':"{:.1f}", 'AST':"{:.1f}", 'TRB':"{:.1f}", 'W/L%': "{:.3f}"}))
with col2:
    result_2 = st.button("Refresh Data", help = "Scrapes the BasketballReference website to get the latest player data and cleans it")
    if result_2:
        with st.spinner("Refreshing Data"):
            combine_scrape()
        st.success('Done!')

    if result:
        df = get_top_10()
        df = df.round(1)
        fig = px.pie(df[['Player','predictions']], values = 'predictions', names = 'Player', title = 'Predicted Share Amount for MVP Candidates')
        # fig.layout.update(showlegend = False)
        st.plotly_chart(fig)


