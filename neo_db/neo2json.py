from py2neo import Graph
import codecs
import os
import json

CA_LIST = {"魏国":0,"蜀国":1,"吴国":2,"群雄":3}

graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="neo"
)

# graph.run("MATCH (n: Person) RETURN n.Name, n.cate").data()

data = graph.run(
    "match(p)-[r]->(n:Person) return p.Name,r.relation,n.Name,p.cate,n.cate"
    ).data()
print(data)
# data[0]
# {'p.Name': '公孙越', 'r.relation': '弟弟', 'n.Name': '公孙瓒', 'p.cate': '群雄', 'n.cate': '群雄'}


data = list(data)

def get_json_data(data):
    json_data = {'data': [], "links": []}
    d = []

    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.Name'] + "_" + i['p.cate'])
        d.append(i['n.Name'] + "_" + i['n.cate'])
        d = list(set(d))
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")

        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['name'] = j_array[0]
        data_item['category'] = CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
        link_item = {}

        link_item['source'] = name_dict[i['p.Name']]

        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)

    return json_data

json_data = get_json_data(data)

f = codecs.open('../static/data.json','w+','utf-8')
f.write(json.dumps(json_data,  ensure_ascii=False))