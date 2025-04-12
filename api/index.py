from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = FastAPI()

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>Поиск текста песни</title>
        </head>
        <body>
            <h1>Введите название трека:</h1>
            <form method="post">
                <input name="query" type="text">
                <button type="submit">Поиск</button>
            </form>
        </body>
    </html>
    """


@app.post("/", response_class=HTMLResponse)
async def get_lyrics(query: str = Form(...)):
    try:
        # Поиск через Google
        search_url = f"https://www.google.com/search?q=site:genius.com+{urllib.parse.quote(query)}"
        search_response = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(search_response.text, "html.parser")

        # Поиск первой ссылки на Genius
        link = None
        for a in soup.select("a"):
            href = a.get("href", "")
            if "genius.com" in href and "/lyrics" in href:
                link = href.split("&")[0].replace("/url?q=", "")
                break

        if not link:
            return "<h3>Ссылка на песню не найдена :(</h3>"

        # Получаем HTML песни
        lyrics_page = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(lyrics_page.text, "html.parser")
        lyrics_divs = soup.select("div[data-lyrics-container=true]")
        lyrics = "\n".join([div.get_text(separator="\n") for div in lyrics_divs])

        return f"""
        <html>
            <head>
                <title>Lyrics</title>
            </head>
            <body>
                <h2>{query}</h2>
                <pre>{lyrics}</pre>
                <button onclick="copyLyrics()">Скопировать</button>
                <script>
                    function copyLyrics() {{
                        navigator.clipboard.writeText(document.querySelector('pre').innerText)
                            .then(() => alert("Скопировано!"));
                    }}
                </script>
            </body>
        </html>
        """

    except Exception as e:
        return f"<h3>Ошибка: {str(e)}</h3>"
