"""Authentication routes as a blueprint."""
from flask import Blueprint, request, session, make_response
from .utils import encode, decode, ph

bp = Blueprint('auth', __name__)


@bp.route('/home/login', methods=['POST'])
def login():
    res = make_response('OK')
    session.clear()
    sname = request.form['name']
    password = request.form['password']
    # actual auth logic will be injected by app factory through globals
    from . import db
    sql = db.sql
    try:
        ress = sql.search('users', f'name="{sname}"')
        npw = ph.hash(password)
        if password == ress[0][2] and ress[0][6] == 1:
            session['username'] = sname
            session['password'] = password
            session['uid'] = str(ress[0][0])
            sql.update('users', 'password', '"'+npw+'"', f'id={ress[0][0]}')
            sql.update('users', 'pwd_need_update', 0, f'id={ress[0][0]}')
            return res
        elif ress[0][6] == 0:
            pres = ph.verify(str(ress[0][2]), str(password))
            session['username'] = sname
            session['password'] = password
            session['uid'] = str(ress[0][0])
            sql.update('users', 'password', '"'+npw+'"', f'id={ress[0][0]}')
            sql.update('users', 'pwd_need_update', 0, f'id={ress[0][0]}')
            return res
    except Exception:
        # fallback for urlencoded names
        scname = encode(sname)
        ress = sql.search('users', f'name="{scname}"')
        if password == ress[0][2] and ress[0][6] == 1:
            session['username'] = scname
            session['password'] = password
            session['uid'] = str(ress[0][0])
            npw = ph.hash(password)
            sql.update('users', 'password', '"'+npw+'"', f'id={ress[0][0]}')
            sql.update('users', 'pwd_need_update', 0, f'id={ress[0][0]}')
            return res
        elif ress[0][6] == 0:
            pres = ph.verify(str(ress[0][2]), str(password))
            session['username'] = scname
            session['password'] = password
            session['uid'] = str(ress[0][0])
            sql.update('users', 'password', '"'+npw+'"', f'id={ress[0][0]}')
            sql.update('users', 'pwd_need_update', 0, f'id={ress[0][0]}')
            return res
    return 'username or password incorrect'


@bp.route('/home/signin', methods=['GET', 'POST'])
def signin():
    from . import db
    sql = db.sql
    if request.method == 'GET':
        sname = request.args.get('name')
        password = request.args.get('password')
        sname, password = encode(sname), encode(password)
        cc = sql.search('users', f'name="{sname}"')
        if len(cc) == 0:
            phash = ph.hash(password)
            res = sql.add('users', 'name,password,signin_date',
                          '"{0}","{1}",Now()'.format(sname, phash))
            userN = sql.search('users', f'name="{sname}"')
            if res == 1:
                resp = make_response('OK')
                session.clear()
                session['username'] = sname
                session['password'] = password
                session['uid'] = str(userN[0][0])
                return 'OK'
            else:
                return str(res)
        else:
            return 'username repeated'
    else:
        sname = request.form['name']
        password = request.form['password']
        sname, password = encode(sname), encode(password)
        cc = sql.search('users', f'name="{sname}"')
        if len(cc) == 0:
            phash = ph.hash(password)
            res = sql.add('users', 'name,password,signin_date',
                          '"{0}","{1}",Now()'.format(sname, phash))
            userN = sql.search('users', f'name="{sname}"')
            if res == 1:
                resp = make_response('OK')
                session.clear()
                session['username'] = sname
                session['password'] = password
                session['uid'] = str(userN[0][0])
                return 'OK'
            else:
                return str(res)
        else:
            return 'username repeated'


@bp.route('/forum/verify')
def verify():
    from . import db
    sql = db.sql
    username = session.get('username')
    password = session.get('password')
    res = sql.search('users', f'name="{username}"')
    try:
        if (ph.verify(res[0][2], password)):
            return 'OK'
    except Exception:
        return 'password not match.'
    return 'False'
