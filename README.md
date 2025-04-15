# Spotifyrr

Perfect — thanks for sharing the repo! Based on the contents of [https://github.com/johanUX3/Spotifyrr](https://github.com/johanUX3/Spotifyrr), here’s a clean and detailed `README.md` file tailored for your project:

---

```markdown
# Spotifyrr 🎧

Spotifyrr is a simple and clean **Streamlit web app** that lets you download tracks from a public Spotify playlist. Just paste the playlist link and let the app handle the rest — scraping song metadata and downloading the audio directly.

---

## 🚀 Features

- 🔗 Paste a public Spotify playlist link and fetch all tracks
- 🎵 Download songs from the playlist (audio)
- 📁 Saves all songs into a `downloads` folder
- 🧼 Clean, minimal Streamlit UI

---

## 🛠️ Requirements

Before running the app, make sure to:

1. Have **Python 3.7+** installed
2. Install the required dependencies (see below)
3. Create a folder named `downloads` in the root directory — this must be **empty** and will be used to store the downloaded songs

---

## 📦 Installation

```bash
git clone https://github.com/johanUX3/Spotifyrr.git
cd Spotifyrr
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

If `requirements.txt` is missing or incomplete, you can manually install the dependencies:

```bash
pip install streamlit spotipy pytube
```

> Note: You may also need `ffmpeg` for some audio operations. Install via your package manager (`brew install ffmpeg`, `sudo apt install ffmpeg`, or download from https://ffmpeg.org/download.html).

---

## ▶️ How to Run the App

After installing dependencies and creating the `downloads` folder:

```bash
streamlit run app.py
```

The app will open in your default browser. Paste any **public Spotify playlist URL**, and hit the **Download** button!

---

## 📁 Folder Structure

```
Spotifyrr/
├── app.py
├── requirements.txt
└── downloads/   <-- make sure this folder exists and is empty
```

---

## ⚠️ Disclaimer

This project is intended for **educational and personal use only**. Downloading copyrighted content without permission may violate Spotify's terms of service and copyright laws.

---

## 📬 Contributions

PRs and suggestions are welcome! If you find bugs or want to enhance features, feel free to fork and submit a pull request.

---

## 📄 License

MIT License © [johanUX3](https://github.com/johanUX3)

```

---

Let me know if you'd like to:
- Add screenshots or a demo GIF
- Include optional `env` configuration (e.g. if Spotify API keys are used)
- Polish it further for deployment (e.g. Streamlit sharing)

Want me to commit this README to your repo too?
