import streamlit as st
from lyricsgenius import Genius
from transformers import pipeline

genius = Genius('MaqKi8XxAuUa3JIrN7IjtTfN4tWXz4qHbRwA7PQeIwZBO0cJI8Ridy4ilUFhpuG_')

@st.cache(allow_output_mutation=True)
def load_model():
    pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ru")
    return pipe

pipe = load_model() 
def predict(text):
    return pipe(text)[0]["translation_text"]


def get_lyrics(song_name):
    song = genius.search_song(song_name)
    lyrics = song.lyrics[song.lyrics.find('Lyrics')+6:]
    lyrics = lyrics.split('\n')
    res = ''
    for row in lyrics:
        st.progress(row)
        if '[' in row:
            res += row
            res += '\n'
        else:
            res += predict(row)
            res += '\n'
    return res

st.title('Перевод песен Genius')
song_name = st.text_input('Введите название песни с Genius')
result = st.button('Перевести')
if result:
    preds = get_lyrics(song_name)
    st.write('**Результаты перевода:**')
    st.write(preds)
