from flask import Flask, request, Response, render_template, flash
import os
import yt_dlp
import re
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = os.getenv('KEY')

def sanitize_filename(filename):
    # Remove invalid characters and limit the length
    return re.sub(r'[<>:"/\\|?*]', '_', filename)[:255]

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        link = request.form.get("link", "").strip()
        if not link:
            flash("Please enter a valid YouTube link.")
            return render_template("index.html")

        try:
            ydl_opts = {
                'format': 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]',
                'noplaylist': True,
                'quiet': True,
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
                },
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessor_args': ['-movflags', 'faststart'],
            }

            # Download the video as a stream
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=False)  # Change to download=False
                video_url = info_dict['url']
                video_title = info_dict.get('title', 'video')
                sanitized_filename = sanitize_filename(video_title + '.mp4')

                return Response(ydl.urlopen(video_url),  # Stream the video directly
                                mimetype="application/octet-stream",
                                headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(sanitized_filename)}"})

        except Exception as e:
            flash(f"An error occurred: {str(e)}")

    return render_template("index.html")

if __name__ == "__main__":
    app.run()