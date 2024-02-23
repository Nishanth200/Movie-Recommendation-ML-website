import streamlit as st
import pickle
import requests

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown("""
<style>
section {
  background: #bdc3c7; 
  background: -webkit-linear-gradient(to right, #bdc3c7, #2c3e50); 
  background: linear-gradient(to right, #bdc3c7, #2c3e50); 
}
</style>
    """, unsafe_allow_html=True)

movies_list = movies_list['title'].values

st.title("Cine Suggest")
st.write('A blend of “cinema” and “suggest,” emphasizing personalized movie recommendations.')

selected_movie_name = st.selectbox('Select the movie you watched recently!', movies_list)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": st.secrets['auth_token']
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    return 'https://image.tmdb.org/t/p/w185/'+data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),
                        reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movies_poster


if st.button('Recommend'):
    names, poster = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])
