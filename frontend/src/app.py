from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap5
import requests

app = Flask(__name__)
bootstrap = Bootstrap5(app)

API_URL = "http://127.0.0.1:8000/trials"


@app.route('/')
def home():
    res = requests.get(API_URL)
    trials = res.json()
    return render_template('home.html', trials=trials)


@app.route('/create_trial', methods=['POST'])
def create_trial():
    trial = {
        "crop": request.form['crop'],
        "location": request.form['location'],
        "status": request.form.get('status', "Active")
    }

    requests.post(API_URL, data=trial)

    return redirect('/')