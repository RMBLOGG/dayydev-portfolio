from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import requests as http
from datetime import date

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

# ── Supabase config ────────────────────────────────────────
SUPABASE_URL     = "https://mafnnqttvkdgqqxczqyt.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hZm5ucXR0dmtkZ3FxeGN6cXl0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE4NzQyMDEsImV4cCI6MjA4NzQ1MDIwMX0.YRh1oWVKnn4tyQNRbcPhlSyvr7V_1LseWN7VjcImb-Y"

HEADERS = {
    "apikey":        SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type":  "application/json",
    "Prefer":        "return=representation",
}

REST = f"{SUPABASE_URL}/rest/v1"

# ── Supabase helpers ───────────────────────────────────────

def sb_get_clicks():
    """Return dict {project_key: click_count}"""
    try:
        r = http.get(f"{REST}/portfolio_clicks?select=project_key,click_count",
                     headers=HEADERS, timeout=5)
        rows = r.json() if r.ok else []
        return {row["project_key"]: row["click_count"] for row in rows}
    except Exception:
        return {}

def sb_increment_click(key):
    """Increment click_count for project_key, return new count."""
    try:
        # Fetch current count
        r = http.get(
            f"{REST}/portfolio_clicks?project_key=eq.{key}&select=click_count",
            headers=HEADERS, timeout=5)
        rows = r.json() if r.ok else []
        current = rows[0]["click_count"] if rows else 0
        new_count = current + 1

        # Upsert
        http.post(
            f"{REST}/portfolio_clicks",
            headers={**HEADERS, "Prefer": "resolution=merge-duplicates,return=minimal"},
            json={"project_key": key, "click_count": new_count, "updated_at": "now()"},
            timeout=5)
        return new_count
    except Exception:
        return 0

def sb_get_visitors_today():
    """Return visitor count for today, increments by 1."""
    today = str(date.today())
    try:
        r = http.get(
            f"{REST}/portfolio_visitors?visit_date=eq.{today}&select=visit_count",
            headers=HEADERS, timeout=5)
        rows = r.json() if r.ok else []
        current = rows[0]["visit_count"] if rows else 0
        new_count = current + 1

        http.post(
            f"{REST}/portfolio_visitors",
            headers={**HEADERS, "Prefer": "resolution=merge-duplicates,return=minimal"},
            json={"visit_date": today, "visit_count": new_count},
            timeout=5)
        return new_count
    except Exception:
        return 0

# ── Projects data ──────────────────────────────────────────

projects = [
    {
        "name": "Dayynime",
        "key": "dayynime",
        "desc": "Platform streaming anime online dengan koleksi lengkap dan tampilan modern. Nikmati anime favorit kapan saja dan di mana saja.",
        "url": "https://dayynime.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://dayynime.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "Streaming",
        "color": "#ff6b9d",
        "category": "anime"
    },
    {
        "name": "Animeku.ID",
        "key": "animeku",
        "desc": "Website streaming anime Indonesia dengan koleksi terlengkap, update terbaru, dan antarmuka yang nyaman untuk semua pecinta anime.",
        "url": "https://animeku-id.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://animeku-id.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "Streaming",
        "color": "#a78bfa",
        "category": "anime"
    },
    {
        "name": "Cinevu",
        "key": "cinevu",
        "desc": "Platform streaming film dan series dengan koleksi lengkap, subtitle Indonesia, dan kualitas video terbaik.",
        "url": "https://cinevu.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://cinevu.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "Film",
        "color": "#fb923c",
        "category": "movie"
    },
    {
        "name": "Cinevu API",
        "key": "cinevu-api",
        "desc": "REST API backend untuk platform Cinevu — menyediakan data film, episode, dan sumber streaming secara real-time.",
        "url": "https://cinevu-api.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://cinevu-api.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "API",
        "color": "#34d399",
        "category": "tools"
    },
    {
        "name": "Dayynime API",
        "key": "dayynime-api",
        "desc": "REST API scraper anime yang menyediakan data episode, streaming, dan informasi anime terbaru untuk integrasi berbagai platform.",
        "url": "https://dayynime-api.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://dayynime-api.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "API",
        "color": "#38bdf8",
        "category": "tools"
    },
    {
        "name": "MyList Anime",
        "key": "mylist",
        "desc": "Buat dan kelola daftar anime favoritmu, lalu bagikan ke teman-teman dengan mudah. Track anime yang sudah dan belum ditonton.",
        "url": "https://mylistanime-v2.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://mylistanime-v2.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "MyList",
        "color": "#f472b6",
        "category": "anime"
    },
    {
        "name": "DayyScorer",
        "key": "dayyscorer",
        "desc": "Pantau skor pertandingan sepak bola secara live dan tonton siaran langsungnya dalam satu platform yang lengkap.",
        "url": "https://dayyscorer.vercel.app",
        "screenshot": "https://api.microlink.io/?url=https://dayyscorer.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
        "tag": "Sports",
        "color": "#4ade80",
        "category": "tools"
    },
]

app_data = {
    "name": "AnimeDayy",
    "desc": "Aplikasi Android all-in-one untuk pecinta anime. Streaming, download, dan track anime favoritmu langsung dari smartphone.",
    "url": "/",
    "screenshot": "https://api.microlink.io/?url=https://animedayy-download.vercel.app&screenshot=true&meta=false&embed=screenshot.url",
}

support_url = "https://sociabuzz.com/dayynime/tribe"

anime_keys = [p["key"] for p in projects if p["category"] == "anime"]
movie_keys = [p["key"] for p in projects if p["category"] == "movie"]
tools_keys = [p["key"] for p in projects if p["category"] == "tools"]

# ── Routes ─────────────────────────────────────────────────

@app.route('/')
def index():
    clicks         = sb_get_clicks()
    visitors_today = sb_get_visitors_today()

    total_clicks = sum(clicks.values())
    anime_clicks = sum(clicks.get(k, 0) for k in anime_keys)
    movie_clicks = sum(clicks.get(k, 0) for k in movie_keys)
    tools_clicks = sum(clicks.get(k, 0) for k in tools_keys)

    return render_template('index.html',
        projects=projects,
        app=app_data,
        support_url=support_url,
        clicks=clicks,
        visitors_today=visitors_today,
        ctr_total=total_clicks,
        ctr_anime=anime_clicks,
        ctr_movie=movie_clicks,
        ctr_tools=tools_clicks,
    )

@app.route('/api/track-click', methods=['POST'])
def track_click():
    data = request.get_json(silent=True) or {}
    key  = data.get('key', '').strip()
    if not key:
        return jsonify({'error': 'no key'}), 400

    sb_increment_click(key)
    clicks = sb_get_clicks()

    total = sum(clicks.values())
    anime = sum(clicks.get(k, 0) for k in anime_keys)
    movie = sum(clicks.get(k, 0) for k in movie_keys)
    tools = sum(clicks.get(k, 0) for k in tools_keys)

    return jsonify({
        'clicks': clicks,
        'totals': {'total': total, 'anime': anime, 'movie': movie, 'tools': tools}
    })

@app.route('/api/stats')
def stats():
    clicks = sb_get_clicks()
    return jsonify({'clicks': clicks})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
