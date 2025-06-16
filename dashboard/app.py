from flask import Flask, request, render_template_string, flash, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-me")

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DATA_FILE = os.path.join(DATA_DIR, 'feedback.json')
os.makedirs(DATA_DIR, exist_ok=True)

FORM_TEMPLATE = """
<!doctype html>
<title>Feedback</title>
<h1>Feedback Form</h1>
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <ul>
    {% for category, message in messages %}
      <li class="{{ category }}">{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
<form method="post">
  Name: <input type="text" name="name" value="{{ request.form.get('name', '') }}"><br>
  Message:<br>
  <textarea name="message">{{ request.form.get('message', '') }}</textarea><br>
  <input type="submit" value="Submit">
</form>
"""

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        message = request.form.get('message', '').strip()
        if not name or not message:
            flash('Name and message are required.', 'error')
        else:
            entry = {
                'name': name,
                'message': message,
                'timestamp': datetime.utcnow().isoformat()
            }
            data = []
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception:
                    data = []
            data.append(entry)
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('feedback'))
    return render_template_string(FORM_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
