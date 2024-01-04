import streamlit as st
import pandas as pd
import pickle
import requests

# Define the fetch_poster function
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()

    # Check if 'poster_path' is available in the response
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    else:
        st.warning("No poster available for this movie.")
        return None

# Function to recommend movies by genre
def recommend_by_movie(selected_movie):
    if selected_movie not in movies['title'].values:
        st.write(f"Error: Movie '{selected_movie}' not found in the dataset.")
        return []

    # Get the genre of the selected movie
    selected_movie_genre = movies[movies['title'] == selected_movie]['genres'].values[0]

    # Filter movies by the selected genre (excluding the selected movie)
    genre_movies = movies[(movies['genres'].str.contains(selected_movie_genre)) & (movies['title'] != selected_movie)]

    # Reset index for proper sampling
    genre_movies = genre_movies.reset_index(drop=True)

    # Randomly shuffle the movies and select the top 5
    recommended_movies = genre_movies.sample(5)

    return recommended_movies['title'].tolist(), recommended_movies.index.tolist()

# Load movies data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title('MOVIE RECOMMENDER SYSTEM')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_indices = recommend_by_movie(selected_movie_name)

    for name, index in zip(recommended_movie_names, recommended_movie_indices):
        st.write(name)

        # Fetch the poster path using the index as movie_id
        poster_path = fetch_poster(index)

        if poster_path is not None:
            st.image(poster_path)
