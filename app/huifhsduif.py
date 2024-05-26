
import requests
import yaml
import pprint

def fetch_crd():
    response = requests.get("https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/kube-prometheus-stack/charts/crds/crds/crd-prometheusrules.yaml")
    

    crds = list(yaml.safe_load_all(response.text))
    crd = crds[0]
    unpack(crd, 0)

def unpack(crd, indent: int):
    content = """"""
    if type(crd) == str:
        print(" "*indent, crd)
    else:
        for item in crd:
            if type(crd[item]) == dict:
                print(" "*indent, item)
                unpack(crd[item], indent+1)
            elif type(crd[item]) == list:
                for element in crd[item]:
                    unpack(element, indent+1)
            else:
                print(" "*indent, item, ":", crd[item])

fetch_crd()

