from flask import Flask, render_template, redirect, url_for
import json
import os
import subprocess
import sys

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')

KEYWORD_PATH = os.path.join(DATA_DIR, 'keyword_output_with_cpc.json')
HOOK_PATH = os.path.join(DATA_DIR, 'generated_hooks.json')


def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/keywords')
def show_keywords():
    data = load_json(KEYWORD_PATH) or {}
    keywords = data.get('filtered_keywords', data if isinstance(data, list) else [])
    return render_template('keywords.html', keywords=keywords)


@app.route('/hooks')
def show_hooks():
    hooks = load_json(HOOK_PATH) or []
    return render_template('hooks.html', hooks=hooks)


@app.route('/run_pipeline', methods=['POST'])
def run_pipeline():
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(BASE_DIR), 'run_pipeline.py')])
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
