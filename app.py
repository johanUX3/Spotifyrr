import streamlit as st
import subprocess
import os
import uuid
import glob
import time
from mutagen.mp3 import MP3

# Spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# OPTIONAL: Load credentials from .env
from dotenv import load_dotenv
load_dotenv()


# 🔐 Get Spotify API credentials from environment variables
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Check if credentials are set
if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    st.error("Spotify API credentials are missing! Please check your .env file.")
    st.stop()

# 🎧 Setup Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))


DOWNLOADS_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

st.set_page_config(page_title="Spotify Playlist Downloader", page_icon="🎵")
st.title("🎵 Spotify Playlist Downloader")

# --- USER INPUT ---
playlist_url = st.text_input("Enter Spotify Playlist URL")
folder_name_input = st.text_input("Optional: Name the download folder")

# --- GET PLAYLIST INFO FUNCTION ---
def get_playlist_info(playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    playlist = sp.playlist(playlist_id)

    tracks = []
    for item in playlist["tracks"]["items"]:
        track = item["track"]
        name = track["name"]
        artist = track["artists"][0]["name"]
        duration_sec = track["duration_ms"] // 1000
        tracks.append({
            "title": name,
            "artist": artist,
            "duration": duration_sec
        })

    return {
        "name": playlist["name"],
        "image": playlist["images"][0]["url"] if playlist["images"] else None,
        "tracks": tracks
    }

# --- DISPLAY PLAYLIST INFO ---
if playlist_url.startswith("https://open.spotify.com/playlist/"):
    try:
        playlist_info = get_playlist_info(playlist_url)
        st.image(playlist_info["image"], width=300)
        st.subheader(f"🎶 {playlist_info['name']}")
        st.write(f"Tracks: {len(playlist_info['tracks'])}")
        
        total_secs = sum(t["duration"] for t in playlist_info["tracks"])
        st.write(f"Estimated total duration: {total_secs//60} min {total_secs%60} sec")
        st.table([{ "Track": t["title"], "Artist": t["artist"], "Duration (s)": t["duration"] } for t in playlist_info["tracks"]])
    except Exception as e:
        st.error("Failed to fetch playlist info.")
        st.stop()

# --- DOWNLOAD TRIGGER ---
if st.button("Download Playlist"):
    if not playlist_url:
        st.error("Please enter a valid Spotify playlist URL.")
    else:
        folder_name = folder_name_input.strip() or str(uuid.uuid4())
        folder_name = "".join(c for c in folder_name if c.isalnum() or c in ('-', '_'))
        folder_path = os.path.join(DOWNLOADS_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        st.info("⏳ Downloading started...")

        try:
            process = subprocess.Popen(
                ["spotdl", "--output", folder_path, playlist_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            bar = st.progress(0)
            song_table = st.empty()
            song_status = []
            downloaded = 1
            total_tracks = len(playlist_info["tracks"])

            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    line = line.strip()
                    for track in playlist_info["tracks"]:
                        if track["title"].lower() in line.lower():
                            song_status.append({"Status": "✅ Downloaded", "Title": track["title"]})
                            downloaded += 1
                            bar.progress(int(downloaded / total_tracks * 100))
                            song_table.table(song_status)

            st.success("✅ All songs downloaded!")
            audio_files = glob.glob(os.path.join(folder_path, "*.mp3"))

            # Display audio players
            if audio_files:
                st.subheader("🎶 Play Downloaded Songs:")
                for file in audio_files:
                    st.audio(file)
                    st.caption(os.path.basename(file))
            else:
                st.warning("No MP3s found in download folder.")

        except Exception as e:
            st.error(f"Download failed: {e}")
