"""Forum related routes as a blueprint."""
from flask import Blueprint, render_template, request, redirect, session, send_file, abort
from .models import Post, Reply
from .utils import get_md5, encode, decode, is_forbidden
from random import randint as ri
from os import listdir

bp = Blueprint('forum', __name__)

# In original code NEED_UPDATE_FLAG and pl were module-level; keep local cache
pl = []
NEED_UPDATE_FLAG = True


@bp.route('/forum')
def forum_index():
    global NEED_UPDATE_FLAG, pl
    username = session.get('username')
    if NEED_UPDATE_FLAG:
        pl = []
        from . import db
        sql = db.sql
        posts = sql.search('posts', 'True ORDER BY id DESC')
        for i in posts:
            userInfo = sql.search('users', f'id="{i[3]}"')
            uiFix = 'none' if userInfo[0][5] is None else userInfo[0][5]
            bpobj = Post(id=i[0], title=decode(i[1]), content=i[2], author=decode(
                userInfo[0][1]), ptime=i[4], aid=i[3], aem=get_md5(uiFix))
            pl.append(bpobj)
    return render_template('forum.htm', name=username, l=pl)


@bp.route('/forum/m')
def forum_mobile():
    # reuse same logic
    return forum_index()


@bp.route('/new-post')
def new_post():
    return render_template('np-m.htm', uname=session.get('username'))


@bp.route('/forum/post', methods=['POST'])
def post_create():
    global NEED_UPDATE_FLAG
    if request.method != 'POST':
        abort(500)
    t, c, a = request.form['title'], request.form['content'], request.form['author']
    if is_forbidden(t) or is_forbidden(c) or is_forbidden(a):
        abort("Stop Attacking My Site Using This Stupid Pattern!!!!!! :(")
    t, c, a = encode(t), encode(c), encode(a)
    uid = session.get('uid')
    from . import db
    sql = db.sql
    res = sql.add('posts', 'title,content,authorID,P_time',
                  '"{0}","{1}","{2}",sysdate()'.format(t, c, uid))
    NEED_UPDATE_FLAG = True
    if res != 1:
        return str(res)
    return redirect('/forum')


@bp.route('/forum/post/<id>')
def show_post(id):
    from . import db
    sql = db.sql
    fp = sql.search('posts', f'id={id}')[0]
    fpusr = sql.search('users', f'id={fp[3]}')[0]
    nsp = Post(id=fp[0], title=decode(fp[1]), content=fp[2], author=decode(
        fpusr[1]), ptime=fp[4], aid=fpusr[0], aem=get_md5(fpusr[5]))
    repl = []
    coms = sql.search('reply', f'ref_to={id}')
    for rep in coms:
        u = sql.search('users', f'id={rep[2]}')[0]
        repl.append(Reply(content=decode(rep[1]), aid=rep[2], authorName=decode(
            u[1]), authorEmail=get_md5(u[5])))
    return render_template('post-nt.htm', p=nsp, replys=repl)


@bp.route('/post/comment/<id>', methods=['POST'])
def comment(id):
    if request.method != 'POST':
        abort(405)
    c = request.form['content']
    if is_forbidden(str(request.form)) or is_forbidden(c) or is_forbidden(decode(str(request.form))):
        abort("Stop Attacking My Site Using This Weird Pattern!!!!!! :(")
    c = encode(c)
    aid = session.get('uid')
    from . import db
    sql = db.sql
    res = sql.add('reply', 'content,authorID,ref_to',
                  "'{0}','{1}','{2}'".format(c, aid, id))
    if c == None or c == '':
        return 'Empty content!'
    if res != 1:
        return str(res)
    return redirect(f'/forum/post/{id}')


@bp.route('/getImage')
def get_image():
    pictures = listdir('drawings')
    return send_file('drawings/' + pictures[ri(0, len(pictures) - 1)])


@bp.route('/fonts/hsr.TTF')
def font():
    return send_file('fonts/hsr.TTF')


@bp.route('/forum/fonts/hsr.TTF')
def fmfont():
    return send_file('fonts/hsr.TTF')
