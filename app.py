from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False)

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        alias = request.form['alias']
        code = request.form['code']
        message = request.form['message']
        data[alias] = {'code': code, 'message': message}
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        return render_template('index.html', success=True)
    return render_template('index.html', success=False)

@app.route('/read', methods=['GET', 'POST'])
def read():
    if request.method == 'POST':
        alias = request.form['alias']
        code = request.form['code']
        if alias in data and data[alias]['code'] == code:
            return render_template('read.html', alias=alias, message=data[alias]['message'], error=False)
        else:
            return render_template('read.html', error=True)
    return render_template('read.html', error=None)

if __name__ == '__main__':
    app.run(debug=False)