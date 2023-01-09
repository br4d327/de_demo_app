import streamlit as st
import requests
from lyricsgenius import Genius
from transformers import pipeline
from bs4 import BeautifulSoup
import re

genius = Genius(st.secrets['TOKEN'])

web_root = 'https://genius.com/'
header=None

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ru")

def predict(text):
    return pipe(text)[0]["translation_text"]

def make_request(path):
    response = None
    tries = 0
    retries = 5
    session = requests.Session()
    while response is None and tries <= retries:
        tries += 1
        try:
            response = session.request('GET', path,
                                       timeout=5,
                                       params={},
                                       headers=header)
            response.raise_for_status()
        except Timeout as e:
            error = "Request timed out:\n{e}".format(e=e)
            if tries > retries:
                raise Timeout(error)
        except HTTPError as e:
            error = get_description(e)
            if response.status_code < 500 or tries > retries:
                raise HTTPError(response.status_code, error)
                
    return response.text

def parse_text(web_root):    # Scrape the song lyrics from the HTML
    html = BeautifulSoup(
        make_request(web_root).replace('<br/>', '\n'),
        "html.parser"
    )
    # Determine the class of the div
    div = html.find("div", class_=re.compile("^lyrics$|Lyrics__Container"))
    lyrics = div.get_text()

#     lyrics = re.sub(r'(\[.*?\])*', '', lyrics)
#     lyrics = re.sub('\n{2}', '\n', lyrics)  # Gaps between verses
    return lyrics.strip("\n")

def get_lyrics(lyrics):
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
    r = requests.get(f'https://genius.com/api/search/multi?q={song_name}')
    path = genius.song(r.json()['response']['sections'][0]['hits'][0]['result']['api_path'].split('/')[-1])
    
    web_root += path
    result = get_lyrics(parse_text(web_root))

    st.write('**Результаты перевода:**')
    st.write(result)
