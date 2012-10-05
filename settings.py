import os

# environment variables


PORT = int(os.environ.get("PORT", 5000))
SECRET_KEY = str(os.environ.get("SECRET_KEY"))
DEBUG = str(os.environ.get("DEBUG"))
SQLALCHEMY_DATABASE_URI=str(os.environ.get("SQLALCHEMY_DATABASE_URI"))
SENDGRID_KEY = os.environ.get("SENDGRID_KEY")
