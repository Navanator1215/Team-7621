"""
Course: CST 205 - Multimedia Design & Programming.
Title: Driscoll's R&D Platform
Authors: Juan Zavala, Alan Olvera, Antonio Navarro, David J Salinas-Villafuerte
Date: May 14, 2026

GitHub Repository:
https://github.com/Navanator1215/Team-7621.git

Description:
This backend API manages trial data, database operations,
file uploads, and CRUD routes.

Team Contribtuions for this file: 

Alan Olvera and Antonio Navarro- Worked on making the FLask API that our frontend uses. 

"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

from database import db
from models import Trial


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
DATABASE_PATH = os.path.join(BASE_DIR, "trials.db")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

# Configure the Flask app with database and upload settings
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trials.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

CORS(app)
db.init_app(app)


@app.route("/")
def home():
    return jsonify({"message": "Flask backend is running"})

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    # Serve uploaded media files from the uploads directory
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/trials", methods=["GET"])
def get_trials():
    # Retrieve all trials from the database, ordered by most recent first
    trials = Trial.query.order_by(Trial.id.desc()).all()
    return jsonify([trial.to_dict() for trial in trials])

@app.route("/trials", methods=["POST"])
def create_trial():
    # Gather form data from the request to create a new trial record
    crop = request.form.get("crop", "").strip()
    variety = request.form.get("variety", "").strip()
    location = request.form.get("location", "").strip()
    objective = request.form.get("objective", "").strip()
    season = request.form.get("season", "").strip()
    status = request.form.get("status", "Active").strip()
    notes = request.form.get("notes", "").strip()

    if not crop or not location:
        return jsonify({"error": "Crop and location are required."}), 400

    media = request.files.get("media")
    media_filename = None
    media_type = None

    # Handle media file upload if a file is provided
    if media and media.filename:
        media_filename = secure_filename(media.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], media_filename)
        media.save(save_path)

        if media.mimetype.startswith("image/"):
            media_type = "image"
        elif media.mimetype.startswith("video/"):
            media_type = "video"
        else:
            media_type = "file"

    trial = Trial(
        crop=crop,
        variety=variety,
        location=location,
        objective=objective,
        season=season,
        status=status,
        notes=notes,
        media_filename=media_filename,
        media_type=media_type,
    )

    # Save the new trial record to the database
    db.session.add(trial)
    db.session.commit()

    return jsonify(trial.to_dict()), 201

@app.route("/trials/<int:trial_id>", methods=["PUT"])
def update_trial(trial_id):
    trial = Trial.query.get_or_404(trial_id)

    # Update trial fields with form data, using existing values as defaults
    trial.crop = request.form.get("crop", trial.crop).strip()
    trial.variety = request.form.get("variety", trial.variety).strip()
    trial.location = request.form.get("location", trial.location).strip()
    trial.objective = request.form.get("objective", trial.objective).strip()
    trial.season = request.form.get("season", trial.season).strip()
    trial.status = request.form.get("status", trial.status).strip()
    trial.notes = request.form.get("notes", trial.notes).strip()

    media = request.files.get("media")

    # Handle media file upload if a new file is provided
    if media and media.filename:
        media_filename = secure_filename(media.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], media_filename)
        media.save(save_path)

        trial.media_filename = media_filename

        if media.mimetype.startswith("image/"):
            trial.media_type = "image"
        elif media.mimetype.startswith("video/"):
            trial.media_type = "video"
        else:
            trial.media_type = "file"

    db.session.commit()
    return jsonify(trial.to_dict())

@app.route("/trials/<int:trial_id>", methods=["DELETE"])
def delete_trial(trial_id):
    # Delete the trial record with the specified ID from the database
    trial = Trial.query.get_or_404(trial_id)
    db.session.delete(trial)
    db.session.commit()
    return jsonify({"message": "Trial deleted successfully"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)