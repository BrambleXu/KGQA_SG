"""Optional Neo4j configuration. Importing this module never opens a connection."""
import os


def connect():
    password = os.environ.get("NEO4J_PASSWORD")
    if not password:
        raise ValueError("Set NEO4J_PASSWORD before using the optional Neo4j importer")
    from neo4j import GraphDatabase

    return GraphDatabase.driver(
        os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.environ.get("NEO4J_USER", "neo4j"), password),
    )
