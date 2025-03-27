import pandas as pd
import streamlit as st
import pickle
import requests

# Function to fetch movie poster from TMDb API
def fetch_poster(movie_title):
    api_key = ""  # Replace with your TMDb API key
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(search_url)
    data = response.json()
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_poster_url
    return None

# Function to recommend movies along with posters
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        poster_url = fetch_poster(movie_title)
        recommended_posters.append(poster_url)
    
    return recommended_movies, recommended_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    
    cols = st.columns(5)  # Creating columns for layout
    for col, movie, poster in zip(cols, recommendations, posters):
        with col:
            st.image(poster, use_container_width=True)
            st.write(movie)
