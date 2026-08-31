"""Bounded relationship parser; legacy module name kept for compatibility.

Recognizes graph names and at most two explicit relationship terms.
This is not a general NLP model and requires no native LTP package.
"""
import re

from kgqa.data import people, relations

ALIASES = {"爸爸": "父亲", "爸": "父亲", "爹": "父亲", "妈妈": "母亲", "妈": "母亲", "娘": "母亲", "老婆": "妻", "妻子": "妻", "丈夫": "夫", "老公": "夫"}


def normalize_relation(word):
    return ALIASES.get(word, word)


def get_target_array(question):
    question = question.strip()
    name = next((name for name in sorted(people(), key=len, reverse=True) if question.startswith(name + "的")), None)
    if name is None:
        raise ValueError("请输入已知人物的关系，例如：曹操的父亲是谁？")
    rest = question[len(name) + 1:]
    rest = re.sub(r"(?:是|有)?(?:谁|哪位|哪些人|哪些)(?:呢)?[？?。！!]*$", "", rest)
    terms = [normalize_relation(term) for term in rest.split("的")]
    supported = {normalize_relation(row[2]) for row in relations()}
    if not 1 <= len(terms) <= 2 or any(term not in supported for term in terms):
        raise ValueError("仅支持数据中的一至两层关系，例如：曹操的父亲是谁？")
    return [name, *terms]
