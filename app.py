import streamlit as st
import pandas as pd
import numpy as np

# Load data
movies_df = pd.read_csv('https://files.grouplens.org/datasets/movielens/ml-100k/u.item', sep='|', encoding='ISO-8859-1', 
                        header=None, usecols=[0, 1], names=['movie_id', 'title'])
ratings_df = pd.read_csv('https://files.grouplens.org/datasets/movielens/ml-100k/u.data', sep='\t', encoding='ISO-8859-1', 
                         header=None, usecols=[0, 1, 2], names=['user_id', 'movie_id', 'rating'])

# Create a user-movie rating matrix
user_movie_matrix = ratings_df.pivot_table(index='user_id', columns='movie_id', values='rating')

# Function to generate recommendations
def get_recommendations(user_id, num_recommendations=5):
    if user_id in user_movie_matrix.index:
        user_ratings = user_movie_matrix.loc[user_id].dropna()
        similar_users = user_movie_matrix.corrwith(user_ratings).dropna()

        # Ensure only valid users are considered
        similar_users = similar_users[similar_users.index.isin(user_movie_matrix.index)].sort_values(ascending=False).head(10)

        recommended_movies = pd.Series(dtype='float64')

        for similar_user in similar_users.index:
            similar_user_ratings = user_movie_matrix.loc[similar_user].dropna()
            recommended_movies = pd.concat([recommended_movies, similar_user_ratings])

        recommended_movies = recommended_movies.groupby(recommended_movies.index).mean()
        recommended_movies = recommended_movies.drop(user_ratings.index, errors='ignore')
        recommended_movies = recommended_movies.sort_values(ascending=False).head(num_recommendations)

        return movies_df[movies_df['movie_id'].isin(recommended_movies.index)]
    else:
        return pd.DataFrame(columns=['title'])

# Streamlit App
st.title("Movie Recommendation System")

# Display the image at 70% of its original size
st.image('images/movies.png', width=int(0.7 * 700))  # Assuming original width is around 700px

user_id = st.number_input("Enter your user ID", min_value=1, max_value=943, step=1)

if st.button("Recommend"):
    recommendations = get_recommendations(user_id)
    if not recommendations.empty:
        st.write("Movies the user has watched (showing only the first 10):")
        watched_titles = movies_df[movies_df['movie_id'].isin(user_movie_matrix.loc[user_id].dropna().index)]['title'].head(10)
        st.write(watched_titles.tolist())
        
        st.write("Recommended movies:")
        st.write(recommendations['title'].tolist())
    else:
        st.write("No recommendations found for this user.")
