import json
from pathlib import Path

import pytest

from app import app
from graph_data import image_path, people, person_profile
from KGQA.ltp import get_target_array


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    return app.test_client()


@pytest.mark.parametrize("path", ["/", "/index", "/get_all_relation", "/search", "/KGQA"])
def test_pages_load_without_external_scripts(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert 'src="https://' not in response.text
    assert 'src="http://' not in response.text
    assert "script-src 'self'" in response.headers["Content-Security-Policy"]
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_export_matches_live_graph_and_edges_have_endpoints(client):
    graph = client.get("/graph_data").json
    exported = json.loads((Path(__file__).resolve().parents[1] / "static/data.json").read_text())
    assert graph == exported
    ids = {node["id"] for node in graph["data"]}
    assert len(ids) == len(graph["data"]) == 122
    assert all(edge["source"] in ids and edge["target"] in ids for edge in graph["links"])
    assert len({tuple(sorted(edge.items())) for edge in graph["links"]}) == 146


def test_all_people_have_matching_profiles_and_portraits():
    for name in people():
        assert person_profile(name)["name"] == name
        assert person_profile(name)["summary"] != "暂无简介"
        assert image_path(name).is_file()


@pytest.mark.parametrize("method", ["get", "post"])
def test_search_and_profile_support_both_methods(client, method):
    options = "query_string" if method == "get" else "data"
    response = getattr(client, method)("/search_name", **{options: {"name": "曹操"}})
    assert response.status_code == 200
    assert len(response.json["links"]) == 32
    assert all("曹操" in (edge["source"], edge["target"]) for edge in response.json["links"])
    response = getattr(client, method)("/get_profile", **{options: {"character_name": "曹操"}})
    assert response.status_code == 200
    assert response.json["name"] == "曹操"
    assert "曹操（155年" in response.json["summary"]


@pytest.mark.parametrize("question,answers", [
    ("曹操的爸爸是谁？", ["曹嵩"]),
    ("曹操的妻子是谁？", ["刘氏", "卞氏"]),
    ("刘备的义弟是谁？", ["关羽", "张飞"]),
])
def test_answers_include_every_match(client, question, answers):
    response = client.get("/KGQA_answer", query_string={"name": question})
    assert response.status_code == 200
    assert response.json["answers"] == answers
    assert len(response.json["graph"]["links"]) == len(answers)


def test_two_hop_answer_and_no_match(client):
    # Liu Bei -> Zhang Fei -> Zhang Bao, following incoming relationship edges.
    response = client.get("/KGQA_answer", query_string={"name": "刘备的义弟的儿子是谁？"})
    assert response.status_code == 200
    assert response.json["answers"] == ["关兴", "张苞"]
    assert any(edge["target"] == "刘备" for edge in response.json["graph"]["links"])
    response = client.get("/KGQA_answer", query_string={"name": "曹操的父亲的父亲是谁？"})
    assert response.json["answers"] == []
    assert response.json["graph"]["links"] == []
    assert "未记录" in response.json["message"]


@pytest.mark.parametrize("question", ["", "不存在的人的父亲是谁？", "曹操的", "曹操的父亲的父亲的父亲是谁？", "曹操的银行卡是谁？"])
def test_parser_rejects_unsupported_input(question):
    with pytest.raises(ValueError):
        get_target_array(question)


@pytest.mark.parametrize("name", ["../../app.py", "/etc/passwd", "曹操' MATCH (n) DETACH DELETE n //", '<script>alert(1)</script>'])
def test_unknown_names_never_access_files_or_execute_queries(client, name):
    for path, key in [("/portrait", "name"), ("/search_name", "name"), ("/get_profile", "character_name")]:
        response = client.get(path, query_string={key: name})
        assert response.status_code == 404
        assert response.json == {"error": "未找到该人物"}


def test_limits_and_portrait_content_type(client):
    assert client.get("/search_name").status_code == 400
    assert client.get("/search_name", query_string={"name": "曹" * 201}).status_code == 400
    assert client.post("/search_name", data={"name": "a" * 5000}).status_code == 413
    response = client.get("/portrait", query_string={"name": "曹嵩"})
    assert response.status_code == 200
    assert response.mimetype == "image/jpeg"
    assert response.data[:2] == b"\xff\xd8"
