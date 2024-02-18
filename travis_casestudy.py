#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:10:19 2024

@author: mtejeda
"""
import pandas as pd
import plotly.express as px
pd.options.plotting.backend = "plotly"
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

main_path = ""

netflix= pd.read_csv(main_path+"ns.csv")



netflix['duration'] = np.where(netflix['duration'].isnull(),netflix['rating'],netflix['duration'])
netflix['duration']=netflix['duration'].str.replace('min|Seasons|Season',"",regex=True).astype(int)
netflix['rating']=np.where(netflix['rating'].str.contains("min"),"Unknown",netflix['rating'])

netflix['date_added']=pd.to_datetime(netflix['date_added'].str.strip())


earliest_date = netflix['date_added'].min()
latest_date = netflix['date_added'].max()


netflix['days_on_netflix'] = (latest_date-netflix['date_added']).dt.days




explode_columns = ['listed_in','country','director','cast']
netflix[explode_columns] = netflix[explode_columns].fillna("Unknown")

genres = netflix['listed_in'].str.split(",").explode().str.strip()
country = netflix['country'].str.split(",").explode().str.strip()
director = netflix['director'].str.split(",").explode().str.strip()
cast = netflix['cast'].str.split(",").explode().str.strip()

exploded_df=pd.merge(genres,country,left_index=True,right_index=True).merge(director,left_index=True,right_index=True).merge(cast,left_index=True,right_index=True)

netflix_long = pd.merge(netflix.drop(explode_columns,axis=1),exploded_df,left_index=True,right_index=True)

movies = netflix[netflix['type']=="Movie"].copy()
movies_long = netflix_long[netflix_long['type']=="Movie"].copy()


movie_uniq_genres = movies_long['listed_in'].value_counts()


movie_uniq_country = movies_long['country'].value_counts()

#Movie Director
movie_uniq_director = movies_long['director'].value_counts()

#Movie Actor
movie_uniq_actor = movies_long['cast'].value_counts()

tv = netflix[netflix['type']=="TV Show"].copy()
tv_long = netflix_long[netflix_long['type']=="TV Show"].copy()

tv_uniq_genres = tv_long['listed_in'].value_counts()

tv_uniq_country = tv_long['country'].value_counts()

tv_uniq_director = tv_long['director'].value_counts()

tv_uniq_actor = tv_long['cast'].value_counts()



with st.sidebar: 
	selected = option_menu(
		menu_title = 'Navigation Pane',
		options = ['Abstract', 'Background Information', 'Data Cleaning','Exploratory Analysis','Analysis', 'Conclusion', 'Bibliography'],
		menu_icon = 'arrow-down-right-circle-fill',
		icons = ['bookmark-check', 'book', 'box', 'map', 'bar-chart', 'check2-circle'],
		default_index = 0,
		)
if selected=='Abstract':
    st.title("Netflix Case Study")
    
    st.markdown("Write an introduction of the datasest")
    
    st.dataframe(netflix)

if selected=="Background Information":
    st.title("Background Information")
    
    st.markdown("Write an background information of the datasest")
    
if selected=="Data Cleaning":
    st.title('Data Cleaning')
    
    st.markdown("Explain what this code means")

    code_insert='''netflix['duration'] = np.where(netflix['duration'].isnull(),netflix['rating'],netflix['duration'])
netflix['duration']=netflix['duration'].str.replace('min|Seasons|Season',"",regex=True).astype(int)

'''
    st.code(code_insert,language='python')
    
    st.markdown("Explain what this code means")
    st.code('''netflix['rating']=np.where(netflix['rating'].str.contains("min"),"Unknown",netflix['rating'])''', language='python')

    st.markdown("Explain what this code means")
    code_insert2='''netflix['date_added']=pd.to_datetime(netflix['date_added'].str.strip())
earliest_date = netflix['date_added'].min()
latest_date = netflix['date_added'].max()
netflix['days_on_netflix'] = (latest_date-netflix['date_added']).dt.days
'''
    st.code(code_insert2,language='python')
    
    st.markdown("Explain what this code means")
    
    code_insert3='''explode_columns = ['listed_in','country','director','cast']
netflix[explode_columns] = netflix[explode_columns].fillna("Unknown")
genres = netflix['listed_in'].str.split(",").explode().str.strip()
country = netflix['country'].str.split(",").explode().str.strip()
director = netflix['director'].str.split(",").explode().str.strip()
cast = netflix['cast'].str.split(",").explode().str.strip()
'''
    st.code(code_insert3,language='python')
    
    st.markdown("Explain what this code means")
    
    code_insert4= '''exploded_df=pd.merge(genres,country,left_index=True,right_index=True).merge(director,left_index=True,right_index=True).merge(cast,left_index=True,right_index=True)
netflix_long = pd.merge(netflix.drop(explode_columns,axis=1),exploded_df,left_index=True,right_index=True)'''
    
    st.code(code_insert4,language='python')
    
    st.markdown("Here are the first 5 rows of cleaned dataset")
    st.dataframe(netflix_long.head())
    
    st.markdown("We also seperated Netflix dataset into two different datasets(Movie and TV shows)")
    
    
if selected=="Exploratory Analysis":

   st.title('Exploratory Analysis')
   
   
   
   st.subheader('Exploring Movies by Genre and Countries')
   
   col1,col2=st.columns([4,5])
   with st.form("Select up to 5 genres for US Movies and Countries"):      
       col1_genres = col1.multiselect('Select Up To Five Genres', movies_long["listed_in"].unique(),max_selections=5,key=1)
       col1_countries= col1.multiselect('Select Up To Five Countries',movie_uniq_country.index,max_selections=5,key=2)
       col1_checkbox= col1.checkbox("Check For a Normalized Bar Chart")
       submitted=st.form_submit_button("Submit to produce bar chart")
       if submitted:
           Percent = None
           if col1_checkbox:
               Percent = "percent"
           genre_movies_fig=px.histogram(movies_long[(movies_long['listed_in'].isin(col1_genres))&(movies_long['country'].isin(col1_countries))].drop_duplicates(subset=['show_id']),
                              x="listed_in",
                              color="country",
                              barmode="group",
                              histnorm=Percent,
                              title="Selected Genres by Selected Countries for Movies")
           genre_movies_fig.update_traces(marker_line_width=2)
           genre_movies_fig.update_xaxes(categoryorder='mean descending')
           col2.plotly_chart(genre_movies_fig)


   st.subheader('Exploring TV Show by Genre and Countries')
   
   col3,col4=st.columns([4,5])
   
   with st.form("Select up to 5 genres for TV Shows and Countries"):      
       col3_genres = col3.multiselect('Select Up To Five Genres', tv_long["listed_in"].unique(),max_selections=5,key=3)
       col3_countries= col3.multiselect('Select Up To Five Countries',tv_uniq_country.index,max_selections=5,key=4)
       col3_checkbox= col3.checkbox("Check For a Normalized Bar Chart",key=5)
       submitted=st.form_submit_button("Submit to produce bar chart")
       if submitted:
           Percent = None
           if col1_checkbox:
               Percent = "percent"
           genre_tv_fig=px.histogram(tv_long[(tv_long['listed_in'].isin(col3_genres))&(tv_long['country'].isin(col3_countries))].drop_duplicates(subset=['show_id']),
                              x="listed_in",
                              color="country",
                              barmode="group",
                              histnorm=Percent,
                              title="Selected Genres by Selected Countries for TV Shows")
           genre_tv_fig.update_traces(marker_line_width=2)
           genre_tv_fig.update_xaxes(categoryorder='mean descending')
           col4.plotly_chart(genre_tv_fig)

   st.subheader('Exploring Movies by Genre, Countries,and Duration')
   
   col5,col6=st.columns([4,5])
   
   with st.form("Select up to 5 genres for Movies,Countries, and Duration"):      
       col5_genres = col5.multiselect('Select Up To Five Genres', movies_long["listed_in"].unique(),max_selections=5,key=7)
       col5_countries= col5.multiselect('Select Up To Five Countries',movie_uniq_country.index,max_selections=5,key=8)
       submitted=st.form_submit_button("Submit to produce bar chart")
       
       if submitted:
           fig2=px.histogram(movies_long[(movies_long['listed_in'].isin(col5_genres))&(movies_long['country'].isin(col5_countries))].drop_duplicates(subset=['show_id']),
                              x="listed_in",
                              y="duration",
                              histfunc="avg",
                              barmode="group",
                              color="country",
                              title="Selected Genres and Selected Countries by Average Duration for Movies")
           fig2.update_traces(marker_line_width=2)
           fig2.update_xaxes(categoryorder='mean descending')
           col6.plotly_chart(fig2)
     
   st.subheader('Exploring TV shows by Genre, Countries,and Duration')
   
   col7,col8=st.columns([4,5])
   
   with st.form("Select up to 5 genres for TV Shows,Countries, and Duration"):
      col7_genres = col7.multiselect('Select Up To Five Genres', tv_long["listed_in"].unique(),max_selections=5,key=9)
      col7_countries= col7.multiselect('Select Up To Five Countries',tv_uniq_country.index,max_selections=5,key=10)
      submitted=st.form_submit_button("Submit to produce bar chart")
      
      if submitted:
          fig3=px.histogram(tv_long[(tv_long['listed_in'].isin(col7_genres))&(tv_long['country'].isin(col7_countries))].drop_duplicates(subset=['show_id']),
                             x="listed_in",
                             y="duration",
                             histfunc="avg",
                             barmode="group",
                             color="country",
                             title="Selected Genres and Selected Countries by Average Duration for TV Shows")
          fig3.update_traces(marker_line_width=2)
          fig3.update_xaxes(categoryorder='mean descending')
          col8.plotly_chart(fig3)
          
   st.subheader('Exploring Movies by Genre, Countries,and Days on Netflix')
   col9,col10=st.columns([4,5])
   
   with st.form("Select up to 5 genres for Movies,Countries, and Days on Netflix"):
      col9_genres = col9.multiselect('Select Up To Five Genres', movies_long["listed_in"].unique(),max_selections=5,key=11)
      col9_countries= col9.multiselect('Select Up To Three Countries',movie_uniq_country.index,max_selections=3,key=12)
      col9_checkbox= col9.checkbox("Check For a Log Scale")
      submitted=st.form_submit_button("Submit to produce bar chart")
      
      if submitted:
          Logy=False
          if col9_checkbox:
              Logy = True
          fig4=px.box(movies_long[(movies_long['listed_in'].isin(col9_genres))&(movies_long['country'].isin(col9_countries))].drop_duplicates(subset=['show_id']),
                             x="country",
                             y="days_on_netflix",
                             color="listed_in",
                             hover_name="title",
                             hover_data=["release_year"],
                             log_y=Logy,
                             height=None,
                             width=None,
                             title="Days on Netflix by Selected Genres and Selected Countries for Movies")
          col10.plotly_chart(fig4)
   
   st.subheader('Exploring TV Shows by Genre, Countries,and Days on Netflix')
   col11,col12=st.columns([4,5])
   
   with st.form("Select up to 5 genres for TV Shows,Countries, and Days on Netflix"):
       col11_genres = col11.multiselect('Select Up To Five Genres', tv_long["listed_in"].unique(),max_selections=5,key=13)
       col11_countries= col11.multiselect('Select Up To Three Countries',tv_uniq_country.index,max_selections=3,key=14)
       col11_checkbox= col11.checkbox("Check For a Log Scale",key=15)
       submitted=st.form_submit_button("Submit to produce bar chart")
       
       if submitted:
           Logy=False
           if col11_checkbox:
               Logy = True
           fig5=px.box(tv_long[(tv_long['listed_in'].isin(col11_genres))&(tv_long['country'].isin(col11_countries))].drop_duplicates(subset=['show_id']),
                              x="country",
                              y="days_on_netflix",
                              color="listed_in",
                              hover_name="title",
                              hover_data=["release_year"],
                              log_y=Logy,
                              height=None,
                              width=None,
                              title="Days on Netflix by Selected Genres and Selected Countries for TV Shows")
           col12.plotly_chart(fig5)
    
       
if selected=="Analysis":
    st.title("Analysis")
    
    

if selected=="Conclusion":
    st.title("Conclusion")
    
    
if selected=="Bibliography":
    st.title("Bibliography")
