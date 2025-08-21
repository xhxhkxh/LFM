"""Authentication module: authentication logic separated from route definitions.

This module exposes functions that implement the business logic for
login/signin/verify. Route wrappers live in `route/auth.py` and call these
functions so the codebase cleanly separates module logic and routing.
"""
from flask import request, session, make_response
from .utils import encode, decode, ph


'''
ress[0][0] -> id
ress[0][1] -> name
ress[0][2] -> password
ress[0][3] -> signin_date
ress[0][4] -> usergroup
ress[0][5] -> email
ress[0][6] -> pwd_need_update
'''


def login():
    """Handle login logic (returns Flask response or string)."""
    print("[LOGIN] -> ", request.args if request.method ==
          'GET' else request.form)
    res = make_response('OK')
    session.clear()
    sname = request.form['name']
    password = request.form['password']
    # actual auth logic uses modules.db
    from . import db
    sql = db.sql
    try:
        ress = sql.search('users', f'name="{sname}"')
        if ph.verify(str(ress[0][2]), str(password)):
            pres = ph.verify(str(ress[0][2]), str(password))
            session['username'] = sname
            session['password'] = password
            session['uid'] = str(ress[0][0])
            sql.update('users', 'pwd_need_update', 0, f'id={ress[0][0]}')
            print('[LOGIN] success -> ', session['username'], session['uid'])
            return res
    except Exception:
        # fallback for urlencoded names
        scname = encode(sname)
        ress = sql.search('users', f'name="{scname}"')
        if ph.verify(str(ress[0][2]), str(password)):
            session['username'] = scname
            session['password'] = password
            session['uid'] = str(ress[0][0])
            sql.update('users', 'pwd_need_update', 0, f'id={ress[0][0]}')
            return res

    return 'username or password incorrect'


def signin():
    """Handle user sign-up logic (GET/POST compatible)."""
    from . import db
    print("[SIGNIN] -> ", request.args if request.method ==
          'GET' else request.form)
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


def verify():
    """Verify current session credentials."""
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
