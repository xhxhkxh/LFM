"""Configuration values for the app."""
from datetime import timedelta

VERSION = 'v5.0.0 - "Spinnere"'

# Replace these placeholders with real values in deployment
SECRET_KEY = 'Your Secret Key Here'
MYSQL = {
    'host': r'Host goes here',
    'user': r'Name goes here',
    'port': 3306,
    'password': 'Password goes here',
    'db': r'db name goes here',
    'charset': 'utf8'
}

CAPTCHA_SECRET_KEY = 'Your Secret Key Here'

PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

