from flask import Flask, render_template, request
import lyricsgenius
import logging

# Инициализация API (замени на свой токен)
GENIUS_API_TOKEN = "Dpy1WA8RCFXRCmoAWMsEk9KKrb5WMlrDnmcK_ZrhJVBGzi8dX6BmE8ENY2QJTmOs"
genius = lyricsgenius.Genius(GENIUS_API_TOKEN, skip_non_songs=True, remove_section_headers=True, verbose=True)

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"].strip()

        results = []

        try:
            song = genius.search_song(query)
            if song:
                # Получаем текст песни, удаляя любые разделы
                lyrics = song.lyrics.replace('\n', '<br>')  # Замена новых строк на HTML <br> для форматирования
                logging.debug(f"Трек найден: {song.title}")
                results.append({"title": song.title, "lyrics": lyrics})
            else:
                return render_template("index.html", error="Трек не найден.")

            return render_template("result.html", results=results)
        except Exception as e:
            logging.error("Ошибка при поиске трека: %s", e)
            return render_template("index.html", error=f"Произошла ошибка: {e}")

    return render_template("index.html")
