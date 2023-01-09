import streamlit as st
from lyricsgenius import Genius
from transformers import pipeline
from tqdm import tqdm
from TOKEN import *

genius = Genius(TOKEN)

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
    
    lyrics = [r for r in lyrics if '[' not in r]
    print('translating_song')
    for row in tqdm(lyrics, desc='Translating song'):
        if '[' in row:
            st.write(row)
        else:
            st.write(predict(row))

st.title('Перевод песен Genius')
song_name = st.text_input('Введите название песни с Genius')
result = st.button('Перевести')

if result:
	st.write("перевод:")
	get_lyrics(song_name)
	st.write("Done.")
  
 