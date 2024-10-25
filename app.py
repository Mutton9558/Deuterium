from flask import Flask, request, Response, render_template, flash, after_this_request
import os
from dotenv import load_dotenv
import yt_dlp
import re
from urllib.parse import quote

load_dotenv('.env')

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
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
                },
                'username': 'oauth',
                'password': ''
            }

            # Download the video and prepare the filename
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=True)
                filename = ydl.prepare_filename(info_dict)
                video_title = info_dict.get('title', 'video')
                sanitized_filename = sanitize_filename(video_title + '.mp4')
                os.rename(filename, sanitized_filename)  # Rename the file to the sanitized name

            # Serve the file
            @after_this_request
            def cleanup(response):
                try:
                    # Delay the deletion until after the response is finished
                    response.call_on_close(lambda: os.remove(sanitized_filename))
                except Exception as e:
                    print(f"Error deleting file {sanitized_filename}: {str(e)}")
                return response

            return Response(open(sanitized_filename, 'rb'), 
                            mimetype="application/octet-stream",
                            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(sanitized_filename)}"})

        except Exception as e:
            flash(f"An error occurred: {str(e)}")

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
