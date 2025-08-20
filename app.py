"""Application entrypoint - minimal app factory."""
import re
import os
from random import randint as ri
from urllib.parse import quote as urlencode, unquote

from flask import (
    Flask, request, session, make_response,
    redirect, abort, render_template, send_file
)
import argon2 as ph  # 假设密码哈希库为 phash
from modules import config, db as db_module, errors as errors_module, auth as auth_module, forum as forum_module

# 初始化全局变量
VERSION = "1.0.0"
NEED_UPDATE_FLAG = True
pl = []
forbiddenString = r"(?i)(script|select|insert|update|delete|drop|;|--)"  # 示例正则

# 辅助函数


def getMd5(s):
    import hashlib
    return hashlib.md5(s.encode('utf-8')).hexdigest() if s else 'none'


class Post:
    def __init__(self, i, t, c, a, pt, aid, aem):
        self.id = i
        self.title = t
        self.content = c
        self.author = a
        self.post_time = pt
        self.author_id = aid
        self.author_email_md5 = aem


class reply:
    def __init__(self, content, author_id, author_name, author_email_md5):
        self.content = content
        self.author_id = author_id
        self.author_name = author_name
        self.author_email_md5 = author_email_md5


def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.permanent_session_lifetime = config.PERMANENT_SESSION_LIFETIME

    # 初始化 DB 并挂载到模块
    db_module.sql = db_module.SQL()
    print("[+] Creating SQL session...")
    res = db_module.sql.connect()
    print("DB connect result:", res)

    # 注册蓝图
    app.register_blueprint(auth_module.bp)
    app.register_blueprint(forum_module.bp)

    # 注册错误处理器
    errors_module.register_error_handlers(app)

    return app


# 创建应用实例
app = create_app()


@app.route("/home/login", methods=["POST"])
def login():
    print("|[LOGIN]")
    print("|[+]Inbound new login request. Type: {}, with data: {}".format(request.method, request.form))
    res = make_response("OK")
    session.clear()

    sname = request.form['name']
    password = request.form['password']
    ress = db_module.sql.search('users', 'name="{}"'.format(sname))
    print(ress)

    try:
        user = ress[0]
        uid, stored_hash, pwd_need_update = user[0], user[2], user[6]

        if pwd_need_update == 1 and password == stored_hash:
            # 明文密码匹配，升级哈希
            npw = ph.hash(password)
            db_module.sql.update("users", "password",
                                 '"{}"'.format(npw), "id={}".format(uid))
            db_module.sql.update("users", "pwd_need_update",
                                 0, "id={}".format(uid))
            session['username'] = sname
            session['password'] = password
            session['uid'] = str(uid)
            return res
        elif pwd_need_update == 0:
            if ph.verify(stored_hash, password):
                session['username'] = sname
                session['password'] = password
                session['uid'] = str(uid)
                return res
    except Exception as e:
        print("Login error:", e)

    return 'username or password incorrect'


@app.route("/home/signin", methods=['GET', 'POST'])
def signin():
    print("|[SIGNIN]")
    if request.method == "GET":
        sname = request.args.get('name')
        password = request.args.get('password')
    else:
        sname = request.form['name']
        password = request.form['password']

    sname, password = urlencode(sname), urlencode(password)
    cc = db_module.sql.search("users", 'name="{}"'.format(sname))

    if len(cc) == 0:
        phash = ph.PasswordHasher(password)
        res = db_module.sql.add('users', 'name,password,signin_date',
                                '"{}","{}",NOW()'.format(sname, phash))
        if res == 1:
            userN = db_module.sql.search('users', 'name="{}"'.format(sname))
            session.clear()
            session['username'] = sname
            session['password'] = password
            session['uid'] = str(userN[0][0])
            return "OK"
        else:
            return str(res)
    else:
        return 'username repeated'


@app.route("/forum")
def forum():
    global NEED_UPDATE_FLAG, pl
    username = session.get("username")
    if NEED_UPDATE_FLAG:
        pl = []
        posts = db_module.sql.search('posts', 'True ORDER BY id DESC')
        for p in posts:
            user_info = db_module.sql.search(
                'users', 'id="{}"'.format(p[3]))[0]
            avatar = user_info[5] if user_info[5] else 'none'
            pl.append(Post(p[0], unquote(p[1]), p[2], unquote(
                user_info[1]), p[4], p[3], getMd5(avatar)))
        NEED_UPDATE_FLAG = False
    return render_template("forum.htm", name=username, l=pl, ver=VERSION, uid=session.get("uid"))


@app.route("/forum/m")
def forum_mobile():
    return forum()  # 复用forum逻辑


@app.route("/forum/verify")
def verify():
    username = session.get("username")
    password = session.get("password")
    res = db_module.sql.search('users', 'name="{}"'.format(username))
    try:
        if ph.verify(res[0][2], password):
            return 'OK'
    except:
        return 'password not match.'
    return 'False'


@app.route("/home/m")
def mobile_home():
    return render_template("login-re-m.htm")


@app.route("/")
def home():
    return render_template("login_remake.htm")


@app.route("/new-post")
def new_post():
    return render_template("np-m.htm", uname=session.get("username"))


@app.route("/forum/post", methods=['POST'])
def post():
    global NEED_UPDATE_FLAG
    title = request.form['title']
    content = request.form['content']
    author = request.form['author']

    if re.search(forbiddenString, title) or re.search(forbiddenString, content) or re.search(forbiddenString, author):
        abort(400, "Invalid input detected.")

    title = urlencode(title)
    content = urlencode(content)
    author = urlencode(author)

    uid = session.get("uid")
    res = db_module.sql.add("posts", "title,content,authorID,P_time",
                            '"{}","{}","{}",NOW()'.format(title, content, uid))
    if res != 1:
        return str(res)
    NEED_UPDATE_FLAG = True
    return redirect("/forum")


@app.route("/user/<int:user_id>")
def user_home(user_id):
    user = db_module.sql.search("users", 'id = {}'.format(user_id))
    if not user:
        abort(404)
    posts = db_module.sql.search('posts', 'authorID={}'.format(user_id))
    processed_posts = [[p[0], unquote(p[1]), unquote(p[2])] for p in posts]
    return render_template("user.htm", uid=user_id, suid=session.get("uid"),
                           uname=unquote(user[0][1]), p=processed_posts, email=user[0][5])


@app.route("/user/<int:user_id>/changeemail", methods=['GET'])
def change_email(user_id):
    uid = session.get("uid")
    if str(user_id) != str(uid):
        abort(401)
    email = request.args.get("e")
    if not email or re.search(r'["\']', email):
        return 'Illegal Character!'
    email = urlencode(email).replace("%40", '@')
    try:
        db_module.sql.update('users', 'email', '"{}"'.format(
            email), 'id = {}'.format(uid))
        return 'OK'
    except Exception as e:
        return str(e)


@app.route("/forum/post/<int:post_id>")
def show_post_info(post_id):
    post = db_module.sql.search("posts", 'id={}'.format(post_id))[0]
    user = db_module.sql.search('users', 'id={}'.format(post[3]))[0]
    nsp = Post(post[0], unquote(post[1]), post[2], unquote(
        user[1]), post[4], user[0], getMd5(user[5]))

    replies = []
    comments = db_module.sql.search('reply', 'ref_to={}'.format(post_id))
    for c in comments:
        author = db_module.sql.search('users', 'id={}'.format(c[2]))[0]
        replies.append(
            reply(unquote(c[1]), c[2], unquote(author[1]), getMd5(author[5])))

    return render_template('post-nt.htm', p=nsp, replys=replies)


@app.route("/getImage")
def get_image():
    pictures = os.listdir("drawings")
    if not pictures:
        abort(404)
    return send_file("drawings/"+pictures[ri(0, len(pictures) - 1)])


@app.route("/post/comment/<int:post_id>", methods=['POST'])
def add_comment(post_id):
    global NEED_UPDATE_FLAG
    content = request.form['content']
    if not content or re.search(r'%p(.*%s)*.*?%', content):
        abort(400, "Invalid content.")
    content = urlencode(content)
    author_id = session.get("uid")
    res = db_module.sql.add('reply', 'content,authorID,ref_to',
                            '"{}","{}","{}"'.format(content, author_id, post_id))
    if res != 1:
        return str(res)
    NEED_UPDATE_FLAG = True
    return redirect("/forum/post/{}".format(post_id))


@app.route("/md-playground")
def md_playground():
    return render_template('md.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
