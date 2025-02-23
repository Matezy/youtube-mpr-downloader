import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

# Az asztali "zenék" mappa elérési útja
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
download_folder = os.path.join(desktop, "zenék")

# Ha a mappa nem létezik, hozza létre
os.makedirs(download_folder, exist_ok=True)

requests_list = []

@app.route("/", methods=["GET"])
def home():
    return "YouTube MP3 Downloader API is running!"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    if "youtube_url" in data:
        youtube_url = data["youtube_url"]
        requests_list.append(youtube_url)
        return jsonify({"message": "Link mentve!"}), 200
    return jsonify({"error": "Hiányzó youtube_url"}), 400

@app.route("/get_links", methods=["GET"])
def get_links():
    if requests_list:
        return jsonify({"youtube_url": requests_list.pop(0)})
    return jsonify({"youtube_url": None})

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    if "youtube_url" in data:
        youtube_url = data["youtube_url"]
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"), # Ide menti az MP3-at
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        return jsonify({"message": "Letöltés kész!", "path": download_folder}), 200
    return jsonify({"error": "Hiányzó youtube_url"}), 400

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
