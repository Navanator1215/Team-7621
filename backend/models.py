"""
Course: CST 205 - Multimedia Design & Programming.
Title: Driscoll's R&D Platform
Authors: Juan Zavala, Alan Olvera, Antonio Navarro, David J. Salinas-Villafuerte
Date: May 14, 2026

GitHub Repository:
https://github.com/Navanator1215/Team-7621.git

Description:
This file defines the Trial database model used by the backend API.
The model represents a field trial and stores important information
such as crop, variety, location, objective, season, status, notes,
and uploaded media details.

Team Contribtuions for this file: 

Juan Zavala, Alan Olvera, Antonio Navarro, David J. Salinas-Villafuerte- All worked 
on coming up with the exact model for the database table. 

"""

from database import db


class Trial(db.Model):
    __tablename__ = "trials"

    # Define the columns for the trials table
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(120), nullable=False)
    objective = db.Column(db.String(200), nullable=True)
    season = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default="Active")
    notes = db.Column(db.Text, nullable=True)
    media_filename = db.Column(db.String(255), nullable=True)
    media_type = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        media_url = None
        if self.media_filename:
            media_url = f"http://127.0.0.1:8000/uploads/{self.media_filename}"

        return {
            "id": self.id,
            "crop": self.crop,
            "variety": self.variety,
            "location": self.location,
            "objective": self.objective,
            "season": self.season,
            "status": self.status,
            "notes": self.notes,
            "media_filename": self.media_filename,
            "media_type": self.media_type,
            "media_url": media_url,
        }
