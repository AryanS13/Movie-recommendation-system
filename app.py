import streamlit as st
import pickle
import pandas as pd
import requests
from tmdbv3api import Movie
from requests.exceptions import Timeout
import time

TMDB_API_KEY = '537533250b86a80fe3e199d111e4c90e' #st.secrets["TMDB_API_KEY"]

movie = Movie()
my_bar = st.progress(0, text='')

st.button("Rerun")

def fetch_poster(movie_id):
    try:
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, TMDB_API_KEY), timeout=1)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except Timeout:
        print('Fetching movie timed out')
        return ""


def get_initials(movie_name):
    return movie_name[0] or 'Image Api is down'

def recommend(movie, movies_count=6):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:(movies_count+1)]

    recommended_movies = []
    recommended_movies_posters = []

    total_items = len(movies_list)

    for i, movie_info in enumerate(movies_list):
        progress_percentage = int((i + 1) / total_items * 100)
        my_bar.progress(progress_percentage, text='Fetching movies')

        # Assuming movies is your DataFrame containing movie information
        movie_id = movies.iloc[movie_info[0]].id

        recommended_movies.append(movies.iloc[movie_info[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Enter Movie Name Here ', movies['title'].values)

if st.button('Recommend'):
    my_bar.progress(0, text='Sit back! While we recommend some movies like ' + selected_movie_name)
    names, posters = recommend(selected_movie_name)
    my_bar.progress(100, text='Here are some recommended movies')

    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    with c1:
        st.text(names[0])
        if posters[0]:
            st.image(posters[0])
        else:
            st.subheader(get_initials(names[0]))
    with c2:
        st.text(names[1])
        if posters[1]:
            st.image(posters[1])
        else:
            st.subheader(get_initials(names[1]))
    with c3:
        st.text(names[2])
        if posters[2]:
            st.image(posters[2])
        else:
            st.subheader(get_initials(names[2]))
    with c4:
        st.text(names[3])
        if posters[3]:
            st.image(posters[3])
        else:
            st.subheader(get_initials(names[3]))
    with c5:
        st.text(names[4])
        if posters[4]:
            st.image(posters[4])
        else:
            st.subheader(get_initials(names[4]))
    with c6:
        st.text(names[5])
        if posters[5]:
            st.image(posters[5])
        else:
            st.subheader(get_initials(names[5]))

