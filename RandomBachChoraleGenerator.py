import streamlit as st
from music21 import *
import os
import base64
from typing import NamedTuple
import random

# "struct" for Lyrics
class Lyric(NamedTuple):
    lyric: str
    beat: float
    quarterLength: float

# Helper function that converts tenor part from bass clef -> tenor clef
def change_tenor_clef(score):
    try:
        score.parts['Tenor'].measure(0).clef = clef.Treble8vbClef()
    except AttributeError as e:
        score.parts['Tenor'].measure(1).clef = clef.Treble8vbClef()

# helper function to have pdf renderer in website
def displayPDF(base64_pdf):
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# helper function to get the lyrics from the soprano part
def get_lyrics(part):
    lyrics = []

    for n in part.recurse().getElementsByClass('Note'):
        if n.lyric == None and (n.beat).is_integer() == False:
            pass
        else:
            lyrics.append(Lyric(n.lyric, int(n.beat), n.quarterLength))
    
    return lyrics

# helper function to add the lyrics to all other parts
def add_lyrics(score):
    lyrics = get_lyrics(score.parts['Soprano'])

    parts = ['Alto', 'Tenor', 'Bass']
    

    for p in parts:
        idx = 0
        for n in score.parts[p].recurse().getElementsByClass('Note'):
            curr_lyric = lyrics[idx]
            
            if n.beat == curr_lyric.beat:
                n.lyric = curr_lyric.lyric

                if n.quarterLength > curr_lyric.quarterLength and (curr_lyric.quarterLength).is_integer():
                    idx += 2
                else:
                    idx += 1

def remove_lyrics(score):
    for n in score.parts['Soprano'].recurse().getElementsByClass('Note'):
        n.lyric = None

st.write("# Random Bach Chorale Generator")
st.write("_Use this page to randomly generate PDFs of scores for JS Bach chorales._")
st.write("**NOTE: Some lyrics are not functional. Please toggle lyrics at your discretion. Bug being worked on.**")

bwv_num = st.number_input(label='Enter BWV # for Bach Chorale', step=1, value=250)

lyrics_bool = st.checkbox('Include Lyrics', value=True)

if st.button('Randomize!'):
    bwv_num = random.randint(250, 438)

s = corpus.parse('bach/bwv' + str(bwv_num))
change_tenor_clef(s)

if lyrics_bool:
    add_lyrics(s)
else:
    remove_lyrics(s)

s.write('musicxml.pdf', fp='out.pdf')

# Opening file from file path for preview AND for download
with open('out.pdf', "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

# TODO: Add a working download button
        
#st.download_button(label='DOWNLOAD SCORE', data=base64_pdf, file_name='test.pdf', mime='application/octet-stream')

displayPDF(base64_pdf)

