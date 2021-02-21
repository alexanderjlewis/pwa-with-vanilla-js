#app.py
import json
from gen import generate
from flask import Flask, render_template, url_for, send_file

app = Flask(__name__)
with open('data/recipes.json') as f:
    data = json.load(f)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/list')
def list_page():
    return render_template('list.html', recipes=data['recipes'])

@app.route('/recipe/<name>')
def hello(name=None):
    render_recipe = None
    for recipe in data['recipes']:
        if recipe['safe_name'] == name:
            render_recipe = recipe
    chart = generate(render_recipe)
    return render_template('chart.html', recipe=render_recipe, chart=chart)

@app.route('/sw.js')
def sw():
    return send_file('static/js/sw.js')

@app.route('/offline')
def offline():
    return render_template('offline.html')