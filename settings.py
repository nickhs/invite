import os

# environment variables


PORT = int(os.environ.get("PORT", 5000))
SECRET_KEY = str(os.environ.get("SECRET_KEY", "secret"))
DEBUG = str(os.environ.get("DEBUG", True))
SQLALCHEMY_DATABASE_URI = str(os.environ.get("SQLALCHEMY_DATABASE_URI", 'sqlite:////tmp/test.db'))
SENDGRID_USERNAME = str(os.environ.get("SENDGRID_USERNAME", "change_your_settings.py"))
SENDGRID_PASSWORD = str(os.environ.get("SENDGRID_PASSWORD", "change_your_settings.py"))
