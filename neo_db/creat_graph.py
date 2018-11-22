from py2neo import Graph, Node, Relationship, NodeMatcher
from config import graph

with open("./raw_data/triples_processed.txt") as f:
    graph.run("MATCH (n) DETACH DELETE n")
    print("Delete all nodes and relationships")
    for line in f.readlines():
        relation_array = line.strip("\n").split(",")
        print(relation_array)
        graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (relation_array[3],relation_array[0]))
        graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (relation_array[4], relation_array[1]))
        graph.run(
            "MATCH(e: Person), (cc: Person) \
            WHERE e.Name='%s' AND cc.Name='%s'\
            CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
            RETURN r" % (relation_array[0], relation_array[1], relation_array[2],relation_array[2])
        )