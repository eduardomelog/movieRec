!pip install surprise

import streamlit as st
import pandas as pd
from surprise import Dataset, KNNBasic

# Cargar datos y modelo
data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
movies_df = pd.read_csv('https://files.grouplens.org/datasets/movielens/ml-100k/u.item', sep='|', encoding='ISO-8859-1', 
                        header=None, usecols=[0, 1], names=['movie_id', 'title'])

sim_options = {
    'name': 'cosine',
    'user_based': True  # User-based filtering
}

model = KNNBasic(sim_options=sim_options)
model.fit(trainset)

st.title("Sistema de Recomendación de Películas")

user_id = st.number_input("Ingrese su ID de usuario", min_value=1, max_value=943, step=1)

if st.button("Recomendar"):
    inner_user_id = trainset.to_inner_uid(str(user_id))
    movies_watched = trainset.ur[inner_user_id]
    watched_titles = [movies_df[movies_df['movie_id'] == int(trainset.to_raw_iid(i[0]))]['title'].values[0] for i in movies_watched]
    
    movies_not_watched = [i for i in trainset.all_items() if i not in [j[0] for j in movies_watched]]
    predictions = [model.predict(str(user_id), trainset.to_raw_iid(i)) for i in movies_not_watched]
    recommendations = sorted(predictions, key=lambda x: x.est, reverse=True)[:10]
    
    recommended_titles = [movies_df[movies_df['movie_id'] == int(rec.iid)]['title'].values[0] for rec in recommendations]
    
    st.write("Películas que el usuario ha visto:")
    st.write(watched_titles)
    
    st.write("Películas recomendadas:")
    st.write(recommended_titles)
