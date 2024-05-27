from classist import crd_object 
import requests
import yaml
import pprint
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def fetch_crd():
    #response = requests.get("https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/kube-prometheus-stack/charts/crds/crds/crd-prometheusrules.yaml")
    response = """type: object
description: "foo bar object"
properties:
  foo:
    type: string
    pattern: "abc"
    description: "Does some stuff idk what"
  bar:
    type: integer
  metadata:
    type: object
    properties:
      name:
        type: string
        pattern: "^a"
        description: "its a name goshdarnit"
anyOf:
- properties:
    bar:
      minimum: 42
  required: ["bar"]"""

    crds = list(yaml.safe_load_all(response))#.text))
    crd = crds[0]
    # pprint.pp(crd)
    crd = unpack(crd, 0, "TOP")
    print(crd)
    return render_template("table.html", crd = crd)

def unpack(crd, indent: int, prev_name:str):
    top_level_obj = crd_object([], prev_name)
    if type(crd) == str:
        top_level_obj.add_child(crd_object([], crd))
    else:
        for key in crd:
            if type(crd[key]) == dict:
                # print(" "*indent, key, "B")
                top_level_obj.add_child(unpack(crd[key], indent+1, key))
            elif type(crd[key]) == list:
                # print(" "*(indent+1) + key)
                norm_list = False
                for element in crd[key]:
                    if type(element) != str:
                        top_level_obj.add_child(unpack(element, indent+1, key))
                    else:
                        norm_list = True
                if norm_list:
                    top_level_obj.add_child(crd_object([], key, "", "", crd[key]))
            else:
                # print(" "*indent, key, ":", crd[key], "C")
                top_level_obj.add_child(crd_object([], key, "","", [crd[key]]))
    return typeify(describe(top_level_obj))

def describe(obj:crd_object):
    for poss_desc in obj.childs:
        if poss_desc.name == "description":
            # print(poss_desc, poss_desc.description, obj.name)
            obj.add_description(poss_desc.info)
            obj.remove_child(poss_desc)
    return obj

def typeify(obj:crd_object):
    for poss_desc in obj.childs:
        if poss_desc.name == "type":
            # print(poss_desc, poss_desc.description, obj.name)
            obj.add_types(poss_desc.info)
            obj.remove_child(poss_desc)
    return obj

app.run()