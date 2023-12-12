import os

class Config:
    SECRET_KEY = 'Nerde2023!'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SESSION_TYPE = 'filesystem'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    # Add other configuration variables as needed
