import pytest
from app import app, DATA_DIR

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr("app.DATA_DIR", tmp_path)
    return app.test_client()

def test_home_page_opens(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Локальный файловый менеджер".encode() in response.data

def test_create_and_download_file(client, tmp_path):
    response = client.post("/create", data={"filename": "hello.txt", "content": "Привет"})
    assert response.status_code == 302
    assert (tmp_path / "hello.txt").read_text(encoding="utf-8") == "Привет"
    download = client.get("/download/hello.txt")
    assert download.status_code == 200
    assert "Привет".encode() in download.data

def test_delete_file(client, tmp_path):
    (tmp_path / "remove.txt").write_text("test", encoding="utf-8")
    response = client.post("/delete/remove.txt")
    assert response.status_code == 302
    assert not (tmp_path / "remove.txt").exists()

def test_path_traversal_is_rejected(client):
    response = client.get("/download/../secret.txt")
    assert response.status_code in (400, 404)
