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

    media = request.files.get("media")

    files = {}

    if media and media.filename:

        files["media"] = (media.filename, media.stream, media.mimetype)

    requests.post(API_URL, data=trial, files=files)

    return redirect('/')


@app.route('/delete_trial/<int:trial_id>', methods=['POST'])
def delete_trial(trial_id):
    requests.delete(f"{API_URL}/{trial_id}")
    return redirect('/')


@app.route('/edit_trial/<int:trial_id>')
def edit_trial(trial_id):
    res = requests.get(API_URL)

    trials = res.json()

    trial_to_edit = None

    for trial in trials:

        if trial["id"] == trial_id:

            trial_to_edit = trial

            break

    return render_template('edit.html', trial=trial_to_edit)

@app.route('/update_trial/<int:trial_id>', methods=['POST'])
def update_trial(trial_id):
    updated_trial = {
        "crop": request.form['crop'],
        "location": request.form['location'],
        "status": request.form['status']
    }

    requests.put(f"{API_URL}/{trial_id}", json=updated_trial)

    return redirect('/')