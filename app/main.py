from classist import crd_object 
import requests
import yaml
import pprint
import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def base():
    return render_template("base.html")

@app.route("/fetch-crd", methods=['POST'])
def fetch_crd():
    print("here")
    url = request.form["URL"]
    response = requests.get(url)
    crds = list(yaml.safe_load_all(response.text))
    crd = crds[0]
    # pprint.pp(crd)

    crd = unpack(crd, 0, ["top"], [], True)

    # print(crd)
    
    return render_template("table.html", crd = crd)

def unpack(crd, indent, classes:list, current_set:list, top=False):
    # print(crd)
    if type(crd) == str:
        # print("A", crd)
        current_set.append(crd_object(crd, indent+1, "", "", classes.append(classes[-1]+"."+name)))
    else:
        for name in crd:
            # print(name)
            if type(crd[name]) == dict:
                desc = ""
                types = ""
                for possible in crd[name]:
                    if possible == "type":
                        types = crd[name][possible]
                    if possible == "description":
                        desc = crd[name][possible]
                current_set.append(crd_object(name, indent+1, desc, types, classes.append(classes[-1]+"."+name)))
                #print(name, current_set, classes)
                #new_classes = classes.append(classes[-1]+"."+name)
                #print(new_classes)
                current_set = unpack(crd[name], indent+1, classes, current_set)
                classes.pop(-1)

            elif type(crd[name]) == list:
                norm_list = False
                for element in crd[name]:
                    if type(element) != str:
                        current_set.append(crd_object(name, indent+1, "", "", classes.append(classes[-1]+"."+name)))
                        current_set = unpack(element, indent+1, classes, current_set)
                    else:
                        norm_list=True
                if norm_list:
                    current_set.append(crd_object(name, indent+1, "", "", classes.append(classes[-1]+"."+name), crd[name]))


            else:
                if not top:
                    if name == "type":
                        pass
                    elif name == "description":
                        pass
                    else:
                        current_set.append(crd_object(name, indent+1, "", "", classes.append(classes[-1]+"."+name), crd[name]))
                else:
                    current_set.append(crd_object(name, indent+1, "", "", classes.append(classes[-1]+"."+name), crd[name]))
        
    return current_set

app.run(debug=True)
# def unpack(crd, indent: int, prev_name:str):
#     top_level_obj = crd_object([], prev_name)
#     if type(crd) == str:
#         top_level_obj.add_child(crd_object([], crd, parent=prev_name))
#     else:
#         for key in crd:
#             if type(crd[key]) == dict:
#                 # print(" "*indent, key, "B")
#                 top_level_obj.add_child(unpack(crd[key], indent+1, key))
#             elif type(crd[key]) == list: 
#                 # print(" "*(indent+1) + key)
#                 norm_list = False
#                 for element in crd[key]:
#                     if type(element) != str:
#                         top_level_obj.add_child(unpack(element, indent+1, key))
#                     else:
#                         norm_list = True
#                 if norm_list:
#                     top_level_obj.add_child(crd_object([], key, "", ""))
#             else:
#                 # print(" "*indent, key, ":", crd[key], "C")
#                 top_level_obj.add_child(crd_object([], key, "",""))
#     return typeify(describe(top_level_obj))

# def describe(obj:crd_object):
#     for poss_desc in obj.childs:
#         if poss_desc.name == "description":
#             # print(poss_desc, poss_desc.description, obj.name)
#             obj.add_description(poss_desc.info)
#             obj.remove_child(poss_desc)
#     return obj

# def typeify(obj:crd_object):
#     for poss_desc in obj.childs:
#         if poss_desc.name == "type":
#             # print(poss_desc, poss_desc.description, obj.name)
#             obj.add_types(poss_desc.info)
#             obj.remove_child(poss_desc)
#     return obj

