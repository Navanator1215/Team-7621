"""
Course: CST 205 - Multimedia Design & Programming.
Title: Driscoll's R&D Platform
Authors: Juan Zavala, Alan Olvera, Antonio Navarro, David J. Salinas-Villafuerte
Date: May 14, 2026

GitHub Repository:
https://github.com/Navanator1215/Team-7621.git

Description:
This frontend Flask application displays the user interface for the
R&D trial management platform. It connects to the backend API to
create, view, edit, update, delete, search, and filter trial records.
It also sends uploaded media files from the frontend form to the
backend for storage.

Team Contribuitons for this file: 
Juan Zavala: - Worked on the frontend routes, for creating/displaying/editing/deleting a trial 
as well as their respective html files. 

Alan Olvera- Worked on displayiing cards with trial information at the top of the screen and 
also worked on adding the search/filter functionalty for the displayed trials. 

Antonio Navarro - Worked on the UI design for the frontend routes (and their respectuve 
html files). 

David J. Salinas-Villafuerte - Worked also worked on the UI design for the routes as well.

"""

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:8000/trials"

# Home route:
# Gets all trials from the backend API, applies search/status filters,
# calculates dashboard summary values, and sends the data to home.html.
@app.route("/")
def home():
    # keep original text for display
    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "All").strip()

    # lowercase version only for filtering
    search_lower = search.lower()

    # Get all trials from backend API
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        trials = res.json()
    except requests.exceptions.RequestException:
        trials = []

    filtered_trials = []

    # Apply search and status filters
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
    # Gather form data
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

    # Handle media file upload
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
    # Attempt to delete the trial via the backend API
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

    # Find the trial with the matching ID
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
    # Handle media file upload if a new file is provided
    if media and media.filename:
        files["media"] = (media.filename, media.stream, media.mimetype)

    requests.put(f"{API_URL}/{trial_id}", data=trial_data, files=files)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

