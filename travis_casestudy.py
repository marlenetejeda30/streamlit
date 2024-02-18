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

main_path = "/users/mtejeda/Downloads/"

netflix= pd.read_csv(main_path+"ns.csv")



netflix['duration'] = np.where(netflix['duration'].isnull(),netflix['rating'],netflix['duration'])
netflix['duration']=netflix['duration'].str.replace('min|Seasons|Season',"",regex=True).astype(int)
netflix['rating']=np.where(netflix['rating'].str.contains("min"),"Unknown",netflix['rating'])

netflix['date_added']=pd.to_datetime(netflix['date_added'].str.strip())


earliest_date = netflix['date_added'].min()
latest_date = netflix['date_added'].max()


netflix['days_on_netflix'] = (latest_date-netflix['date_added']).dt.days


netflix.rename(columns={"listed_in":"Genre"},inplace=True)

explode_columns = ['Genre','country','director','cast']
netflix[explode_columns] = netflix[explode_columns].fillna("Unknown")

genres = netflix['Genre'].str.split(",").explode().str.strip()
country = netflix['country'].str.split(",").explode().str.strip()
director = netflix['director'].str.split(",").explode().str.strip()
cast = netflix['cast'].str.split(",").explode().str.strip()

exploded_df=pd.merge(genres,country,left_index=True,right_index=True).merge(director,left_index=True,right_index=True).merge(cast,left_index=True,right_index=True)

netflix_long = pd.merge(netflix.drop(explode_columns,axis=1),exploded_df,left_index=True,right_index=True)

movies = netflix[netflix['type']=="Movie"].copy()
movies_long = netflix_long[netflix_long['type']=="Movie"].copy()


movie_uniq_genres = movies_long['Genre'].value_counts()


movie_uniq_country = movies_long['country'].value_counts()

#Movie Director
movie_uniq_director = movies_long['director'].value_counts()

#Movie Actor
movie_uniq_actor = movies_long['cast'].value_counts()

tv = netflix[netflix['type']=="TV Show"].copy()
tv_long = netflix_long[netflix_long['type']=="TV Show"].copy()

tv_uniq_genres = tv_long['Genre'].value_counts()

tv_uniq_country = tv_long['country'].value_counts()

tv_uniq_director = tv_long['director'].value_counts()

tv_uniq_actor = tv_long['cast'].value_counts()



with st.sidebar: 
	selected = option_menu(
		menu_title = 'Navigation Pane',
		options = ['Abstract', 'Background Information', 'Data Cleaning','Exploratory Analysis','Discussion', 'Conclusion', 'Bibliography'],
		menu_icon = 'arrow-down-right-circle-fill',
		icons = ['bookmark-check', 'book', 'box', 'map', 'bar-chart', 'check2-circle'],
		default_index = 0,
		)
if selected=='Abstract':
    st.title("Netflix Case Study")
    
    st.markdown("Netflix, a leading streaming application, has become widely popular over the past years. Netflix has become a worldwide streaming service that has reached all audiences over the years. Here, we study Netflix’s implications on humans. Research shows that Netflix has been able to control people unintentionally in various aspects.")
    
    st.markdown("According to the article published by Annette Markham, Simona Stavrova, and Max Schlüter, investigating the circumstances of “Netflix, Imagined affordances, and the illusion of control” <sup>1</sup> , the authors outlined that Netflix allows free accessibility for users to watch a variety of award-winning original movies, and the platform can automatically recommend more movies to the users with the relevant genre as they consistently watch.",unsafe_allow_html=True)
    
    st.markdown("Nevertheless, Netflix nowadays is taking control over the movies’ authorities, meaning that the platform has the initial priority to check on these new movies that were just released and make changes to them. One of the most common changes that Netflix makes is limiting the movie content. The purpose of this behavior is to enhance users’ engagements on the platform overall. To make more people start having the intended behavior to subscribe to Netflix, the platform would rather delete scenes or episodes that might be too boring or have meaningless impacts on the audience or even include popular advertisements into the movies aggressively. Thus, Netflix’s profit benefits.")
    
    st.markdown("Furthermore, Netflix even shapes culture, especially during the pandemic period, massive bored shows were disseminated globally and made a huge implication on human behaviors after they were joined on Netflix. For example, the drama “Tiger King” that was released on Netflix in March 2020 not only received a sky-rocketed watch record of that season, but this drama also caused the decline of tigers in zoos. Based on the World Wildlife Fund, approximately 6% of the tigers were lived in zoos, but more tigers were captive while the drama “Tiger King” demonstrated the deep interconnection between humans and big cats <sup>2</sup> .",unsafe_allow_html=True)
    
    st.markdown("In this study, I intend to see how Netflix is affecting different countries and what genres are being widely watched. Additionally, I am also interested in the duration these shows and movies must gauge the audience interest. This would also help understand differences in how Netflix caters to different countries.")
    
    
    
    st.dataframe(netflix)

if selected=="Background Information":
    st.title("Background Information")
    
    st.markdown("Netflix, one of the biggest subscription-based online platforms has been accessed freely to customers in more than 190 countries since 2016. Nowadays, it has also become a widely circulates community, abundant of people enjoy subscribing on this platform. According to Statista, Netflix’s annual profit has increased consistently based on its platform subscription service. In various aspects, Netflix impacts humans’ identities and relationships in both positive and negative.")
    
    st.markdown("Firstly, Netflix serves as a mirror reflecting the diverse tapestry of human experiences, thus playing a pivotal role in shaping cultural identities. Through its expansive library of content spanning various genres, languages, and cultures, Netflix exposes viewers to narratives and perspectives they may not encounter otherwise. From critically acclaimed international films to groundbreaking original series, Netflix provides a platform for underrepresented voices, empowering individuals to see themselves reflected in the stories they consume. This representation fosters a sense of belonging and validation among marginalized communities, reaffirming their cultural identities and challenging societal norms.")
    
    st.markdown("Moreover, Netflix has revolutionized viewing habits, giving rise to the phenomenon of binge-watching and transforming the way individuals consume media. The on-demand nature of Netflix allows viewers to dictate when, where, and how they engage with content, liberating them from the constraints of traditional broadcast schedules. Binge-watching culture, characterized by the marathon viewing of entire seasons in one sitting, has become synonymous with the Netflix experience. While critics decry its potential negative impact on sleep patterns and productivity, binge-watching fosters a sense of immersion and escapism, enabling viewers to lose themselves in the narratives they love.")
    
    
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
    
    code_insert3='''explode_columns = ['Genre','country','director','cast']
netflix[explode_columns] = netflix[explode_columns].fillna("Unknown")
genres = netflix['Genre'].str.split(",").explode().str.strip()
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
       col1_genres = col1.multiselect('Select Up To Five Genres', movies_long["Genre"].unique(),max_selections=5,key=1)
       col1_countries= col1.multiselect('Select Up To Five Countries',movie_uniq_country.index,max_selections=5,key=2)
       col1_checkbox= col1.checkbox("Check For a Normalized Bar Chart")
       submitted=st.form_submit_button("Submit to produce bar chart")
       if submitted:
           Percent = None
           if col1_checkbox:
               Percent = "percent"
           genre_movies_fig=px.histogram(movies_long[(movies_long['Genre'].isin(col1_genres))&(movies_long['country'].isin(col1_countries))].drop_duplicates(subset=['show_id']),
                              x="Genre",
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
       col3_genres = col3.multiselect('Select Up To Five Genres', tv_long["Genre"].unique(),max_selections=5,key=3)
       col3_countries= col3.multiselect('Select Up To Five Countries',tv_uniq_country.index,max_selections=5,key=4)
       col3_checkbox= col3.checkbox("Check For a Normalized Bar Chart",key=5)
       submitted=st.form_submit_button("Submit to produce bar chart")
       if submitted:
           Percent = None
           if col1_checkbox:
               Percent = "percent"
           genre_tv_fig=px.histogram(tv_long[(tv_long['Genre'].isin(col3_genres))&(tv_long['country'].isin(col3_countries))].drop_duplicates(subset=['show_id']),
                              x="Genre",
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
       col5_genres = col5.multiselect('Select Up To Five Genres', movies_long["Genre"].unique(),max_selections=5,key=7)
       col5_countries= col5.multiselect('Select Up To Five Countries',movie_uniq_country.index,max_selections=5,key=8)
       submitted=st.form_submit_button("Submit to produce bar chart")
       
       if submitted:
           fig2=px.histogram(movies_long[(movies_long['Genre'].isin(col5_genres))&(movies_long['country'].isin(col5_countries))].drop_duplicates(subset=['show_id']),
                              x="Genre",
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
      col7_genres = col7.multiselect('Select Up To Five Genres', tv_long["Genre"].unique(),max_selections=5,key=9)
      col7_countries= col7.multiselect('Select Up To Five Countries',tv_uniq_country.index,max_selections=5,key=10)
      submitted=st.form_submit_button("Submit to produce bar chart")
      
      if submitted:
          fig3=px.histogram(tv_long[(tv_long['Genre'].isin(col7_genres))&(tv_long['country'].isin(col7_countries))].drop_duplicates(subset=['show_id']),
                             x="Genre",
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
      col9_genres = col9.multiselect('Select Up To Five Genres', movies_long["Genre"].unique(),max_selections=5,key=11)
      col9_countries= col9.multiselect('Select Up To Three Countries',movie_uniq_country.index,max_selections=3,key=12)
      col9_checkbox= col9.checkbox("Check For a Log Scale")
      submitted=st.form_submit_button("Submit to produce bar chart")
      
      if submitted:
          Logy=False
          if col9_checkbox:
              Logy = True
          fig4=px.box(movies_long[(movies_long['Genre'].isin(col9_genres))&(movies_long['country'].isin(col9_countries))].drop_duplicates(subset=['show_id']),
                             x="country",
                             y="days_on_netflix",
                             color="Genre",
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
       col11_genres = col11.multiselect('Select Up To Five Genres', tv_long["Genre"].unique(),max_selections=5,key=13)
       col11_countries= col11.multiselect('Select Up To Three Countries',tv_uniq_country.index,max_selections=3,key=14)
       col11_checkbox= col11.checkbox("Check For a Log Scale",key=15)
       submitted=st.form_submit_button("Submit to produce bar chart")
       
       if submitted:
           Logy=False
           if col11_checkbox:
               Logy = True
           fig5=px.box(tv_long[(tv_long['Genre'].isin(col11_genres))&(tv_long['country'].isin(col11_countries))].drop_duplicates(subset=['show_id']),
                              x="country",
                              y="days_on_netflix",
                              color="Genre",
                              hover_name="title",
                              hover_data=["release_year"],
                              log_y=Logy,
                              height=None,
                              width=None,
                              title="Days on Netflix by Selected Genres and Selected Countries for TV Shows")
           col12.plotly_chart(fig5)
    
       
if selected=="Discussion":
    st.title("Discussion")
    
    
    
    col1,col2=st.columns([3,5])
    fig1=px.pie(names=movie_uniq_country[0:5].index,values=movie_uniq_country[0:5], height=600,width=600)
    fig1.update_traces(textinfo='label+percent')
    col2.plotly_chart(fig1)
    
    col1.subheader('Exploring Top 5 Movie-Making Countries')
    col1.markdown("Here we can see that United states, United Kindom, and India have the most movies on Netflix. This makes sense because Netflix is a US streaming service company.")

    
    
    col3,col4=st.columns([3,5])
    fig2=px.pie(names=movie_uniq_genres[0:5].index,values=movie_uniq_genres[0:5], height=600,width=600)
    fig2.update_traces(textinfo='label+percent')
    col4.plotly_chart(fig2)
    
    col3.subheader('Exploring Top 5 Movie-Making Countries')
    col3.markdown("Here we can see that top Genres are Drama, International Movies, and Comedies. This makes sense because because as we saw in exploratory analyis, United States watches the most Drama movies.")

    
    
    col5,col6=st.columns([3,5])
    fig3=px.pie(names=tv_uniq_country[0:5].index,values=tv_uniq_country[0:5], height=600,width=600)
    fig3.update_traces(textinfo='label+percent')
    col6.plotly_chart(fig3)
    
    col5.subheader('Exploring Top 5 TV Show-Making Countries')
    col5.markdown("Here we can see that United states, United Kindom, and Japan have the most tv shows on Netflix.This makes sense because Netflix is a US streaming service company. However, there were several TV shows that were missing country data.")

   
    
    col7,col8=st.columns([3,5])
    fig4=px.pie(names=tv_uniq_genres[0:5].index,values=tv_uniq_genres[0:5], height=600,width=600)
    fig4.update_traces(textinfo='label+percent')
    col8.plotly_chart(fig4)
    
    col7.subheader('Exploring Top 5 TV Show Genres')
    col7.markdown("Here we can see that top TV shows genres are International TV Shows, TV Dramas, and TV Comedies.Interestingly International TV shows are more popular than TV Drama. Regardless of film type(tv/movies) the top 3 genre are Drama, international, and comedies.")
    
if selected=="Conclusion":
    st.title("Conclusion")
    
    st.markdown("In conclusion, it's interesting to see that most of the movies on Netflix come from the United States, United Kingdom, and India. Because Netflix is an American company,it's natural they'd have lots of American movies. And when it comes to the top movie genres, Drama, International Movies, and Comedies are the ones people can't get enough of. Drama especially, probably because it's so intense and relatable.")
    
    st.markdown("Shifting our focus to television content, we find a similar trend, with the majority of TV shows originating from the US, UK, and Japan. Nevertheless, the dominance of International TV Shows, TV Dramas, and TV Comedies underscores Netflix's commitment to diversity and inclusivity. Notably, the growing popularity of International TV Shows signifies a growing interest in global storytelling.")
    
    st.markdown("In summary, whether indulging in movies or binge-watching TV shows, it appears that Drama, International content, and Comedies remain perennial favorites among Netflix users worldwide.")
    
if selected=="Bibliography":
    st.title("Bibliography")
    
    st.markdown('[1] Markham, Annette, Simona Stavrova, and Max Schlüter."Netflix, imagined affordances, and the illusion of control." T. Plothe and AM Buck, Netflix at the Nexus. Content, Practice, and Production in the Age of Streaming Television (2019): 29-46.')

    st.markdown('[2]')
