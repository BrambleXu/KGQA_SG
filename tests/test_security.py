import importlib
import json
from pathlib import Path
import runpy

from flask import Flask

ROOT = Path(__file__).resolve().parents[1]


def test_graph_json_is_valid():
    graph = json.loads((ROOT / "static/data.json").read_text())
    assert len(graph["data"]) == 122
    assert len(graph["links"]) == 146


def test_no_debug_server(monkeypatch):
    calls = []
    monkeypatch.setattr(Flask, "run", lambda self, **kwargs: calls.append(kwargs))
    runpy.run_path(str(ROOT / "app.py"), run_name="__main__")
    assert calls == [{"host": "127.0.0.1", "debug": False}]


def test_import_and_local_search_do_not_need_database_or_nlp():
    app = importlib.import_module("app").app
    response = app.test_client().get("/search_name", query_string={"name": "曹操"})
    assert response.status_code == 200
    assert any(node["name"] == "曹操" for node in response.json["data"])


def test_profile_rejects_path_traversal():
    app = importlib.import_module("app").app
    response = app.test_client().get(
        "/get_profile", query_string={"character_name": "../../data/portraits/曹操"}
    )
    assert response.status_code == 404


def test_empty_and_unsupported_questions_are_client_errors():
    app = importlib.import_module("app").app
    for question in ["", "曹操", "曹操的银行卡是什么"]:
        response = app.test_client().get("/KGQA_answer", query_string={"name": question})
        assert response.status_code == 400
        assert "error" in response.json


def test_old_jquery_removed():
    assert not (ROOT / "static/js/jquery-2.2.4.min.js").exists()
    for template in (ROOT / "templates").glob("*.html"):
        assert "jquery-2.2.4" not in template.read_text(encoding="utf-8-sig")
