"""Configuration values for the app."""
from datetime import timedelta

VERSION = 'v4.0.4 - "Attercap"'

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

try:
    from modules import config_test
    MYSQL = config_test.MYSQL
    print("[*] Loaded test config.")
except ImportError as e:
    print("[*] No test config found.")
    print(e)
    pass


CAPTCHA_SECRET_KEY = 'Your Secret Key Here'

PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
