# -*- coding: utf-8 -*-

import streamlit as st
import requests
from PIL import Image
import io
import os

path_vid = 'vids/'
path_lab = 'labels/'

def get_gifs_from_backend(uploaded_gif, gif_description):
    data = {"gif_description": gif_description}
    files = {
        "uploaded_gif": uploaded_gif
    }
    response = requests.post("http://127.0.0.1:5000/endpoint", data=data, files=files)
    res = response.json().get("res", "false")
    return res

def find_sim(text):
    data = {'text': text}
    response = requests.post("http://127.0.0.1:5000/find", data=data)
    gifs = response.json().get("videos", [])
    return gifs

def clear_inputs():
    st.session_state["fl_upload"] = None
    st.session_state["desc_gif"] = ""

text_input = st.text_input("send text prep:")

uploaded_gif = st.file_uploader("load gif/mp4:", type=["gif", 'mp4'], key='fl_upload')

gif_description = st.text_input("gif text:", key='desc_gif')

if st.button("send"):
    if gif_description and uploaded_gif:
        st.write("sending...")
        res = get_gifs_from_backend(uploaded_gif, gif_description)
        st.write(res)
        clear_inputs()
    else:
        st.write("please type text or load GIF.")
elif st.button('find'):
    if text_input:
        try:
            vid_relev = find_sim(text_input)
            for pot_video in vid_relev:
                st.video(os.path.join(path_vid, pot_video), autoplay=True, muted=True)
        except(Exception) as ex:
            print(ex)