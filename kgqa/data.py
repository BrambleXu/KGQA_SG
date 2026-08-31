"""Read-only local data shared by the app and optional Neo4j importer."""
import csv
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = ("魏国", "蜀国", "吴国", "群雄")


@lru_cache(maxsize=1)
def relations():
    with (ROOT / "data/relationships.txt").open(encoding="utf-8", newline="") as stream:
        rows = tuple(sorted(set(tuple(row) for row in csv.reader(stream))))
    for row in rows:
        if len(row) != 5 or not all(row) or any(group not in CATEGORIES for group in row[3:]):
            raise ValueError("Invalid relationship data")
    return rows


@lru_cache(maxsize=1)
def people():
    groups = {}
    for source, target, _, source_group, target_group in relations():
        for name, group in [(source, source_group), (target, target_group)]:
            if name in groups and groups[name] != group:
                raise ValueError(f"Conflicting category for {name}")
            groups[name] = group
    return groups


@lru_cache(maxsize=1)
def profiles():
    return json.loads((ROOT / "data/profiles.json").read_text(encoding="utf-8"))


def chart_data(rows, extra_people=()):
    rows = sorted(set(rows))
    names = sorted(set(extra_people) | {name for row in rows for name in row[:2]})
    return {
        "data": [{"id": name, "name": name, "category": CATEGORIES.index(people()[name])} for name in names],
        "links": [{"source": source, "target": target, "value": relation} for source, target, relation, _, _ in rows],
    }


def person_profile(name):
    if name not in people():
        raise KeyError(name)
    return {"name": name, "category": people()[name], "summary": profiles().get(name, "暂无简介")}


def image_path(name):
    # Whitelist names before constructing any filesystem path.
    if name not in people():
        raise KeyError(name)
    path = ROOT / "data/portraits" / f"{name}.jpg"
    return path if path.is_file() else None
