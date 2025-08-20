"""Configuration values for the app."""
from datetime import timedelta

VERSION = 'v4.0.4 - "Attercap"'

# Replace these placeholders with real values in deployment
SECRET_KEY = 'Your Secret Key Here'
MYSQL = {
    'host': r'Your MySQL Host Here',
    'user': r'Your MySQL User Here',
    'port': 3306,
    'password': 'Your MySQL Password Here',
    'db': r'Database Name Here',
    'charset': 'utf8'
}

CAPTCHA_SECRET_KEY = 'Your Secret Key Here'

PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
