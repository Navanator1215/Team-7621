# backend/models.py

from database import db


class Trial(db.Model):
    __tablename__ = "trials"

    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(100))
    location = db.Column(db.String(120), nullable=False)
    objective = db.Column(db.String(200))
    season = db.Column(db.String(50))
    status = db.Column(db.String(50), default="Active")
    notes = db.Column(db.Text)
    media_filename = db.Column(db.String(255))
    media_type = db.Column(db.String(20))

    def to_dict(self):
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
        }