from flask import Flask, render_template, request
import lyricsgenius

# Вставь сюда свой Genius API токен
GENIUS_API_TOKEN = "Dpy1WA8RCFXRCmoAWMsEk9KKrb5WMlrDnmcK_ZrhJVBGzi8dX6BmE8ENY2QJTmOs"

genius = lyricsgenius.Genius(GENIUS_API_TOKEN, skip_non_songs=True, remove_section_headers=True)
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    lyrics = ""
    title = ""
    error = ""
    if request.method == "POST":
        query = request.form["query"]
        try:
            song = genius.search_song(query)
            if song:
                lyrics = song.lyrics.replace('\n', '<br>')
                title = song.title
            else:
                error = "Песня не найдена."
        except Exception as e:
            error = f"Ошибка при поиске: {e}"

    return render_template("index.html", title=title, lyrics=lyrics, error=error)


if __name__ == "__main__":
    app.run(debug=True)
