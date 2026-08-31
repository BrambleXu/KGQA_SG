"""Idempotent optional importer. Run: uv run --extra neo4j python -m neo_db.creat_graph"""
import os

from graph_data import relations
from neo_db.config import connect

IMPORT_QUERY = """
UNWIND $rows AS row
MERGE (source:KGQASGPerson {Name: row.source})
SET source.cate = row.source_group
MERGE (target:KGQASGPerson {Name: row.target})
SET target.cate = row.target_group
MERGE (source)-[:RELATED_TO {relation: row.relation}]->(target)
"""


def import_graph(driver, database="neo4j"):
    rows = [
        dict(zip(("source", "target", "relation", "source_group", "target_group"), row))
        for row in relations()
    ]

    def write(transaction):
        transaction.run(IMPORT_QUERY, rows=rows).consume()

    with driver.session(database=database) as session:
        session.execute_write(write)
    return len(rows)


def main():
    with connect() as driver:
        count = import_graph(driver, os.environ.get("NEO4J_DATABASE", "neo4j"))
    print(f"Imported {count} relationships; no existing data was deleted.")


if __name__ == "__main__":
    main()
