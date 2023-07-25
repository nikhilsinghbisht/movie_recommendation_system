import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=16b6618418186b2e8b825735cc77cd8e&language=en-US'.format(movie_id))
    data=response.json()

    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])

    recommend_movies=[]
    recommend_movies_posters=[]
    for i in distances[0:31]:
        movie_id=movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies,recommend_movies_posters

def overview(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    i = distances[0]
    return temp.iloc[i[0]].overview , temp.iloc[i[0]].genres , temp.iloc[i[0]].cast , temp.iloc[i[0]].crew

movies_dict=pickle.load(open('movie1_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

temp_dict=pickle.load(open('temp.pkl','rb'))
temp=pd.DataFrame(temp_dict)

similarity=pickle.load(open('similarity1.pkl','rb'))

st.set_page_config(layout="wide")
st.title('Movie Recommender System')

#with open('style.css') as f:
#st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
selected_movie_name = st.selectbox('Select a Movie',movies['title'].values)


if st.button('search'):

    names, posters = recommend(selected_movie_name)
    genre, cast = [], []
    des, genre, cast, crew = overview(selected_movie_name)

    c1, c2, c3 = st.beta_columns(3)
    with c1:
        st.header(names[0])
        st.image(posters[0])

    with c2:
        st.subheader('Overview')
        st.write(des)

        st.subheader('Genres')
        for i in genre:
            st.write(i)

    with c3:

        st.subheader('Cast')
        for i in cast:
            st.write(i)

        st.subheader("Directer")
        st.write(crew[0])

    st.header('Recommended Movies')
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    col = [col1, col2, col3, col4, col5]
    k=0
    for i in range(0,6):
        for j in range(1, 6):
            with col[j - 1]:
                st.text(names[j+k])
                st.image(posters[j+k])
        k=k+5





