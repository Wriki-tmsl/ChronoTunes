import streamlit as st
import os
import random
from pydub import AudioSegment

def load_audio_files(language):
    audio_files = {}
    for file in os.listdir("music_folder\music_folder"):
        if file.endswith(".wav"):
            if language == "Bengali Contemporary Songs" and file.startswith("cn_"):
                article_id = file.split(".")[0]
                audio_files[article_id] = file
            elif language == "Bengali Folk Songs" and file.startswith("fk_"):
                article_id = file.split(".")[0]
                audio_files[article_id] = file
            elif language == "Bengali_Devotional_Songs" and file.startswith("de_"):
                article_id = file.split(".")[0]
                audio_files[article_id] = file
            elif language == "Rabindra Sangeet" and file.startswith("rs_"):
                article_id = file.split(".")[0]
                audio_files[article_id] = file
    return audio_files

def play_audio(file):
    audio_bytes = open("music_folder/music_folder/" + file, "rb").read()
    st.audio(audio_bytes, format="audio/wav")

def create_playlist(language, playlist_size, cn_audio_files, fk_audio_files, de_audio_files, rs_audio_files):
    if language == "Bengali Contemporary Songs":
        audio_files = list(cn_audio_files.values())
    elif language == "Bengali Folk Songs":
        audio_files = list(fk_audio_files.values())
    elif language == "Bengali_Devotional_Songs":
        audio_files = list(de_audio_files.values())
    elif language == "Rabindra Sangeet":
        audio_files = list(rs_audio_files.values())

    random.shuffle(audio_files)
    playlist_files = audio_files[:playlist_size]

    playlist = AudioSegment.empty()
    for file in playlist_files:
        audio = AudioSegment.from_wav("music_folder/music_folder/" + file)
        playlist += audio

    output_path = "music_folder/music_folder/playlist.wav"
    playlist.export(output_path, format="wav")

    return output_path

def main():
    st.title("Chrono Tunes")

    # Retrieve query parameters
    query_params = st.experimental_get_query_params()
    #query_params =st.query_params()
    article_id = query_params.get("article_id", [None])[0]

    # Language selection
    language = st.selectbox("Language", ("Bengali Contemporary Songs", "Bengali Folk Songs","Bengali_Devotional_Songs","Rabindra Sangeet"))
    time = st.selectbox("Time", ("Morning","Afternoon","Evening","Night"))

    # Load audio files based on language selection
    audio_files = load_audio_files(language)

    # Loop/Shuffle mode selection
    mode = st.radio("Playback Mode", ("Loop", "Shuffle"), key="mode")

    # Playlist size selection
    playlist_size = st.slider("Playlist Size", min_value=5, max_value=20, value=10)

    # Create Playlist button
    if st.button("Create Playlist"):
        cn_audio_files = {k: v for k, v in audio_files.items() if v.startswith("cn_")}
        fk_audio_files = {k: v for k, v in audio_files.items() if v.startswith("fk_")}
        de_audio_files = {k: v for k, v in audio_files.items() if v.startswith("de_")}
        rs_audio_files = {k: v for k, v in audio_files.items() if v.startswith("rs_")}
        playlist_path = create_playlist(language, playlist_size, cn_audio_files, fk_audio_files, de_audio_files, rs_audio_files)

    # Toggle between Contemporary and Folk audio files
    cn_audio_files = {k: v for k, v in audio_files.items() if v.startswith("cn_")}
    fk_audio_files = {k: v for k, v in audio_files.items() if v.startswith("fk_")}
    de_audio_files = {k: v for k, v in audio_files.items() if v.startswith("de_")}
    rs_audio_files = {k: v for k, v in audio_files.items() if v.startswith("rs_")}

    # Find matching audio file based on query parameter "article_id"
    current_file = None
    if article_id:
        if language == "Bengali Contemporary Songs" and article_id in cn_audio_files:
            current_file = cn_audio_files[article_id]
        elif language == "Bengali Folk Songs" and article_id in fk_audio_files:
            current_file = fk_audio_files[article_id]
        elif language == "Bengali_Devotional_Songs" and article_id in de_audio_files:
            current_file = de_audio_files[article_id]
        elif language == "Rabindra Sangeet" and article_id in rs_audio_files:
            current_file = rs_audio_files[article_id]

    # Shuffle audio files if shuffle mode is selected
    if mode == "Shuffle":
        if language == "Bengali Contemporary Songs":
            audio_files = list(cn_audio_files.values())
            random.shuffle(audio_files)
        elif language == "Bengali Folk Songs":
            audio_files = list(fk_audio_files.values())
            random.shuffle(audio_files)
        elif language == "Bengali_Devotional_Songs":
            audio_files = list(de_audio_files.values())
            random.shuffle(audio_files)
        elif language == "Rabindra Sangeet":
            audio_files = list(rs_audio_files.values())
            random.shuffle(audio_files)
    else:
        if language == "Bengali Contemporary Songs":
            audio_files = list(cn_audio_files.values())
        elif language == "Bengali Folk Songs":
            audio_files = list(fk_audio_files.values())
        elif language == "Bengali_Devotional_Songs":
            audio_files = list(de_audio_files.values())
        elif language == "Rabindra Sangeet":
            audio_files = list(rs_audio_files.values())

    # Display audio files
    if len(audio_files) > 0:
        for i, file in enumerate(audio_files):
            if st.button(f"Play {file}", key=file):
                query_params["article_id"] = [file.split(".")[0]]
                st.experimental_set_query_params(**query_params)
                play_audio(file)
    else:
        st.warning("No audio files available.")

    # If requested file is not available, display a warning message
    if not current_file and article_id:
        st.warning(f"Warning: Audio file for article ID '{article_id}' not found.")

if __name__ == "__main__":
    main()