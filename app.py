from pathlib import Path
from flask import Flask, abort, redirect, render_template_string, request, send_file, url_for

app = Flask(__name__)
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

PAGE = """
<!doctype html>
<html lang="ru">
<head><meta charset="utf-8"><title>Локальный файловый менеджер</title></head>
<body>
  <h1>Локальный файловый менеджер</h1>
  <form method="post" action="/create">
    <label>Имя файла: <input name="filename" required></label>
    <label>Текст: <input name="content" required></label>
    <button type="submit">Создать файл</button>
  </form>
  <h2>Файлы</h2>
  <ul>
  {% for name in files %}
    <li><a href="/download/{{ name }}">{{ name }}</a>
      <form method="post" action="/delete/{{ name }}" style="display:inline">
        <button type="submit">Удалить</button>
      </form>
    </li>
  {% else %}<li>Файлов пока нет</li>{% endfor %}
  </ul>
</body></html>
"""

def safe_file_path(filename: str) -> Path:
    # Разрешаем только простые имена файлов, без путей и спецсимволов.
    if not filename or Path(filename).name != filename or filename in {".", ".."}:
        abort(400, description="Недопустимое имя файла")
    path = (DATA_DIR / filename).resolve()
    if path.parent != DATA_DIR.resolve():
        abort(400, description="Недопустимый путь")
    return path

@app.get("/")
def index():
    files = sorted(p.name for p in DATA_DIR.iterdir() if p.is_file())
    return render_template_string(PAGE, files=files)

@app.post("/create")
def create_file():
    filename = request.form.get("filename", "")
    content = request.form.get("content", "")
    path = safe_file_path(filename)
    path.write_text(content, encoding="utf-8")
    return redirect(url_for("index"))

@app.get("/download/<filename>")
def download_file(filename):
    path = safe_file_path(filename)
    if not path.is_file():
        abort(404)
    return send_file(path, as_attachment=True, download_name=path.name)

@app.post("/delete/<filename>")
def delete_file(filename):
    path = safe_file_path(filename)
    if not path.is_file():
        abort(404)
    path.unlink()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Для контейнера слушаем все интерфейсы; debug выключен.
    app.run(host="0.0.0.0", port=8080, debug=False)
