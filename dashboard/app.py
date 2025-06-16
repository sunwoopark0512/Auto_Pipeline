import os
import json
import random
from datetime import datetime
from flask import Flask, request, make_response, render_template

app = Flask(__name__, template_folder='templates')

LOG_PATH = os.path.join('data', 'ab_test_log.json')
VARIANT_COOKIE = 'ab_variant'
VARIANTS = ['A', 'B']


def log_interaction(variant, endpoint):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []
    except Exception:
        data = []

    data.append({
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'variant': variant,
        'endpoint': endpoint
    })

    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route('/page')
def ab_page():
    variant = request.cookies.get(VARIANT_COOKIE)
    if variant not in VARIANTS:
        variant = random.choice(VARIANTS)
    log_interaction(variant, '/page')
    template = 'variant_a.html' if variant == 'A' else 'variant_b.html'
    resp = make_response(render_template(template))
    resp.set_cookie(VARIANT_COOKIE, variant, max_age=60 * 60 * 24 * 30)
    return resp


@app.route('/summary')
def summary():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    counts = {'A': 0, 'B': 0}
    for item in data:
        v = item.get('variant')
        if v in counts:
            counts[v] += 1

    return render_template('summary.html', counts=counts)


if __name__ == '__main__':
    app.run(debug=True)
