"""
Course: CST 205
Title: Driscoll's R&D Platform
Authors: Juan Zavala, Alan Olvera, Antonio Navarro, David J. Salinas-Villafuerte
Date: May 13, 2026

GitHub Repository:
https://github.com/your-username/your-repository

Description:
This frontend Flask application displays the user interface for the
R&D trial management platform. It connects to the backend API to
create, view, edit, update, delete, search, and filter trial records.
It also sends uploaded media files from the frontend form to the
backend for storage.
"""

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:8000/trials"


@app.route("/")
def home():
    # keep original text for display
    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "All").strip()

    # lowercase version only for filtering
    search_lower = search.lower()

    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        trials = res.json()
    except requests.exceptions.RequestException:
        trials = []

    filtered_trials = []

    for trial in trials:
        crop = str(trial.get("crop", "")).lower()
        variety = str(trial.get("variety", "")).lower()
        location = str(trial.get("location", "")).lower()
        objective = str(trial.get("objective", "")).lower()
        status = str(trial.get("status", ""))

        matches_search = (
            search_lower in crop
            or search_lower in variety
            or search_lower in location
            or search_lower in objective
        )

        matches_status = status_filter == "All" or status == status_filter

        if matches_search and matches_status:
            filtered_trials.append(trial)

    # summary (keep based on ALL trials, not filtered)
    total = len(trials)
    active = len([t for t in trials if t.get("status") == "Active"])
    completed = len([t for t in trials if t.get("status") == "Completed"])
    locations = len(set(t.get("location") for t in trials if t.get("location")))
    planned = len([t for t in trials if t.get("status") == "Planned"])

    return render_template(
        "home.html",
        trials=filtered_trials,
        total=total,
        active=active,
        completed=completed,
        planned=planned,
        locations=locations,
        search=search, 
        status_filter=status_filter,
    )


@app.route("/create_trial", methods=["POST"])
def create_trial():
    form_data = {
        "crop": request.form.get("crop", "").strip(),
        "variety": request.form.get("variety", "").strip(),
        "location": request.form.get("location", "").strip(),
        "objective": request.form.get("objective", "").strip(),
        "season": request.form.get("season", "").strip(),
        "status": request.form.get("status", "Active").strip(),
        "notes": request.form.get("notes", "").strip(),
    }

    files = {}
    media = request.files.get("media")
    if media and media.filename:
        files["media"] = (media.filename, media.stream, media.mimetype)

    try:
        requests.post(API_URL, data=form_data, files=files)
    except requests.exceptions.RequestException:
        pass

    return redirect(url_for("home"))


@app.route("/delete_trial/<int:trial_id>", methods=["POST"])
def delete_trial(trial_id):
    try:
        requests.delete(f"{API_URL}/{trial_id}")
    except requests.exceptions.RequestException:
        pass

    return redirect(url_for("home"))

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
    trial_data = {
        "crop": request.form['crop'],
        "location": request.form['location'],
        "status": request.form['status'],
        "objective": request.form.get("objective"),
        "notes": request.form.get("notes")
    }

    media = request.files.get("media")

    files = {}
    if media and media.filename:
        files["media"] = (media.filename, media.stream, media.mimetype)

    requests.put(f"{API_URL}/{trial_id}", data=trial_data, files=files)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

