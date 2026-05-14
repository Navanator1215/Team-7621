"""
Course: CST 205 
Title: Driscoll's R&D Platform
Authors: Juan Zavala, , Alan Olvera, Antonio Navarro, David J Salinas-Villafuerte
Date: May 14, 2026

GitHub Repository:
https://github.com/Navanator1215/Team-7621.git

Description:

This file creates the SQLAlchemy database object used by the backend.

Team Contributions for this file:

Alan Olvera - Created and managed the database setup in this file.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
