from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import lyricsgenius
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Вставь свой API ключ
GENIUS_API_TOKEN = "your_genius_token_here"
genius = lyricsgenius.Genius(GENIUS_API_TOKEN, skip_non_songs=True, remove_section_headers=True)


@app.get("/", response_class=HTMLResponse)
async def form():
    return """
    <html>
        <head>
            <title>Поиск текста</title>
        </head>
        <body>
            <h1>Введите название трека:</h1>
            <form action="/" method="post">
                <input type="text" name="query">
                <button type="submit">Поиск</button>
            </form>
        </body>
    </html>
    """


@app.post("/", response_class=HTMLResponse)
async def get_lyrics(query: str = Form(...)):
    song = genius.search_song(query)
    if not song:
        return "<h3>Песня не найдена :(</h3>"

    return f"""
    <html>
        <head>
            <title>{song.title}</title>
        </head>
        <body>
            <h2>{song.title}</h2>
            <pre>{song.lyrics}</pre>
            <button onclick="copyLyrics()">Скопировать текст</button>
            <script>
                function copyLyrics() {{
                    navigator.clipboard.writeText(document.querySelector('pre').innerText)
                        .then(() => alert("Скопировано!"));
                }}
            </script>
        </body>
    </html>
    """
