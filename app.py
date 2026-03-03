from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

projects = [
    {
        "name": "DayyStream",
        "desc": "Platform streaming anime online dengan koleksi lengkap dan tampilan modern. Nikmati anime favorit kapan saja dan di mana saja.",
        "url": "https://dayystream.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://dayystream.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "Streaming",
        "color": "#ff6b9d"
    },
    {
        "name": "DAYYdesu",
        "desc": "Website anime dengan database terlengkap, informasi episode, sinopsis, dan rating untuk semua genre anime.",
        "url": "https://dayydesu.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://dayydesu.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "Streaming",
        "color": "#a78bfa"
    },
    {
        "name": "MediaDown",
        "desc": "Tools download media anime, video, dan konten digital berkualitas tinggi dengan antarmuka yang mudah digunakan.",
        "url": "https://media-down-v2.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://media-down-v2.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "Downloader",
        "color": "#34d399"
    },
    {
        "name": "NekoStream",
        "desc": "Platform streaming anime alternatif dengan kecepatan tinggi, subtitle Indonesia, dan update episode terbaru.",
        "url": "https://neko-stream-sand.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://neko-stream-sand.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "Streaming",
        "color": "#fb923c"
    },
    {
        "name": "DayyShort",
        "desc": "Layanan URL shortener khusus untuk komunitas anime, mudah digunakan dan dapat melacak statistik klik.",
        "url": "https://dayy-short.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://dayy-short.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "DramaBox",
        "color": "#38bdf8"
    },
    {
        "name": "Animeku.id",
        "desc": "Website anime Indonesia dengan koleksi lengkap, update terbaru, dan antarmuka yang nyaman untuk semua pecinta anime.",
        "url": "https://animeku-id.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://animeku-id.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "Streaming",
        "color": "#f472b6"
    },
]

app_data = {
    "name": "AnimeDayy",
    "desc": "Aplikasi Android all-in-one untuk pecinta anime. Streaming, download, dan track anime favoritmu langsung dari smartphone.",
    "url": "https://animedayy-download.vercel.app",
    "screenshot": "https://api.microlink.io/?url=https://animedayy-download.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
}

support_url = "https://sociabuzz.com/dayynime/tribe"

@app.route('/')
def index():
    return render_template('index.html', projects=projects, app=app_data, support_url=support_url)

# Serve static files explicitly (needed for Vercel)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
