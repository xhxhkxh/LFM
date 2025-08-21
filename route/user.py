from flask import Blueprint, request, session, render_template, abort
from modules import db as db_module
from modules.utils import decode, encode
import re

bp = Blueprint('user', __name__)


@bp.route('/user/<int:user_id>')
def user_home(user_id):
    sql = db_module.sql
    user = sql.search('users', f'id = {user_id}')
    if not user:
        abort(404)
    posts = sql.search('posts', f'authorID={user_id}')
    processed_posts = [[p[0], decode(p[1]), decode(p[2])] for p in posts]
    return render_template('user.htm', uid=user_id, suid=session.get('uid'), uname=decode(user[0][1]), p=processed_posts, email=user[0][5])


@bp.route('/user/<int:user_id>/changeemail', methods=['GET'])
def change_email(user_id):
    uid = session.get('uid')
    if str(user_id) != str(uid):
        abort(401)
    email = request.args.get('e')
    if not email or re.search(r'["\']', email):
        return 'Illegal Character!'
    email = encode(email).replace('%40', '@')
    try:
        sql = db_module.sql
        sql.update('users', 'email', '"{}"'.format(email), f'id = {uid}')
        return 'OK'
    except Exception as e:
        return str(e)
