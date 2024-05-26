# app.py
from flask import Flask, render_template, request, jsonify
import requests
import yaml
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_crd', methods=['POST'])
def fetch_crd():
    url = request.json['url']
    response = requests.get(url)

    if response.headers['Content-Type'] == 'application/json':
        crds = [response.json()]
    else:
        crds = list(yaml.safe_load_all(response.text))

    return jsonify(crds)

if __name__ == '__main__':
    app.run(debug=True)
