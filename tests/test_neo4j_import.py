from contextlib import nullcontext
from unittest.mock import Mock

from neo_db import import_graph


def test_import_keeps_untrusted_data_out_of_cypher_and_does_not_delete(monkeypatch):
    hostile_name = "O'Connor) DETACH DELETE n //"
    monkeypatch.setattr(import_graph, "relations", lambda: [(hostile_name, "曹操", "父亲", "魏国", "魏国")])
    transaction = Mock()
    session = Mock()
    session.execute_write.side_effect = lambda callback: callback(transaction)
    driver = Mock()
    driver.session.return_value = nullcontext(session)

    assert import_graph.import_graph(driver, "example") == 1

    query = transaction.run.call_args.args[0]
    parameters = transaction.run.call_args.kwargs
    assert hostile_name not in query
    assert "DELETE" not in query.upper()
    assert "$rows" in query
    assert "KGQASGPerson" in query
    assert parameters["rows"][0]["source"] == hostile_name
    driver.session.assert_called_once_with(database="example")


def test_missing_password_does_not_attempt_connection(monkeypatch):
    from neo_db.config import connect

    monkeypatch.delenv("NEO4J_PASSWORD", raising=False)
    import pytest
    with pytest.raises(ValueError, match="NEO4J_PASSWORD"):
        connect()
