"""Read-only local queries. Neo4j is an optional teaching/export tool."""
from KGQA.ltp import normalize_relation
from graph_data import chart_data, people, person_profile, relations


def query(name):
    if name not in people():
        raise KeyError(name)
    return chart_data([row for row in relations() if name in row[:2]], [name])


def get_KGQA_answer(array):
    if not 2 <= len(array) <= 3:
        raise ValueError("仅支持一至两层关系")
    if array[0] not in people():
        raise KeyError(array[0])
    paths = {array[0]: [[]]}
    for relation in array[1:]:
        next_paths = {}
        for row in relations():
            if row[1] in paths and normalize_relation(row[2]) == normalize_relation(relation):
                next_paths.setdefault(row[0], []).extend(path + [row] for path in paths[row[1]])
        paths = next_paths
    rows = [row for person_paths in paths.values() for path in person_paths for row in path]
    return {
        "graph": chart_data(rows, [array[0]]),
        "answers": sorted(paths),
        "message": "、".join(sorted(paths)) if paths else "数据中未记录匹配关系；这不代表历史上不存在。",
    }


def get_answer_profile(name):
    return person_profile(name)
