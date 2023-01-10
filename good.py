import streamlit as st
from lyricsgenius import Genius
from transformers import pipeline
from tqdm import tqdm
#from TOKEN import *
import os

# Функции
# Загрузка модели
@st.cache(allow_output_mutation=True)
def load_model():
    return pipeline("translation", model="Helsinki-NLP/opus-mt-en-ru")

# Перевод
def predict(text):
    return pipe(text)[0]["translation_text"]

# Вывод текста
def get_lyrics(song_name):
    buffer_rows = {}
    song = genius.search_song(song_name)
    subh = 'Песня: ' + song.artist + ' - ' + song.title
    st.header(subh)

    lyrics = song.lyrics[song.lyrics.find('Lyrics') + 6:]
    lyrics = lyrics.split('\n')

    with st.container():
        col1, col2 = st.columns(2)
        with col1: st.subheader('Оригинал')
        with col2: st.subheader('Перевод')

    row_af = ''
    for row in tqdm(lyrics, desc='Translating song'):
        with st.container():
            col1, col2 = st.columns(2)
            if row != '':
                if row[0] != '[':
                    if row[-1] == ']':
                        row_af = row[row.find('['):]
                        row = row[:row.find('[')]

                    if row not in buffer_rows:
                        buffer_rows[row] = predict(row)

                    with col1: st.write(row)
                    with col2: st.write(buffer_rows[row])
                else:
                    with col1: st.write(row)
                    with col2: st.write(row)

            if row_af != '':
                with col1: st.write(row_af)
                with col2: st.write(row_af)
                row_af = ''

# Проверка поля ввода
def cheak_input(input_str):
    if input_str != '':
        get_lyrics(song_name)
        st.write("Готово.")
    else:
        st.error('Поле пустое')

# Токен
TOKEN = os.environ['TOKEN']
genius = Genius(TOKEN)

# Загрузка модели в pipeline
pipe = load_model()

print('Model ready')

# Вывод на сайте
st.title('Перевод песен Genius')
song_name = st.text_input('Введите название песни с Genius')
result = st.button('Перевести')
#print(predict('grape'))

# Вывод на сайт текста песни и перевод к ней
if result:
    cheak_input(song_name)

