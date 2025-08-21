"""Auth routes blueprint - thin wrappers around functions in modules.auth."""
from flask import Blueprint
from modules import auth as auth_module

bp = Blueprint('auth', __name__)


@bp.route('/home/login', methods=['POST'])
def login():
    return auth_module.login()


@bp.route('/home/signin', methods=['GET', 'POST'])
def signin():
    return auth_module.signin()


@bp.route('/forum/verify')
def verify():
    return auth_module.verify()
