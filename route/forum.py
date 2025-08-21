from flask import request, session, render_template, redirect, abort, send_file
from modules import db as db_module
from urllib.parse import unquote
from .utils import urlencode, getMd5, Post, reply, forbiddenString, ri, VERSION, NEED_UPDATE_FLAG, pl
import os
import re


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
    return render_template("forum-nt-v2.htm", name=username, l=pl, ver=VERSION, uid=str(session.get("uid")))


@app.route("/forum/m")
def forum_mobile():
    return render_template("forum-m.htm")


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
