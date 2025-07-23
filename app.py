from os import listdir
from flask import Flask, abort, render_template, request, redirect, session
from flask import send_file, make_response, send_from_directory
from random import randint as ri
from time import sleep
from datetime import timedelta
import re
import pymysql
import hashlib
from urllib.parse import quote as urlencode
from urllib.parse import unquote
from argon2 import PasswordHasher
import requests
import json

# captcha secret key
# This is a placeholder for your hCaptcha secret key.
# Make sure to replace 'Your Secret Key Here' with your actual hCaptcha secret key.
# You can obtain a key from https://www.hcaptcha.com/
# And this function is currently WIP.

# Replace with your actual secret key
CAPTCHA_SECRET_KEY = 'Your Secret Key Here'

VERSION = 'v4.0.4 - \"Attercap\"'

forbiddenString = "%p(.*?%s)*.*?%"

ph = PasswordHasher()


def init():
    print("Hello from LFM develop team!")
    print("Current running version:", VERSION)


def getMd5(s):
    if s == None or s == '':
        return ' '
    md = hashlib.md5(s.encode())
    return md.hexdigest()


NEED_UPDATE_FLAG = True


def errorPageCheck(item):
    if item[0] == -1:
        return render_template("error.htm", errorcode=item[1])
    return item[1]


class Post:
    def __init__(self, i, t, c, a, pt, aid, aem):
        self.title = t
        self.content = c
        self.author = a
        self.id = i
        self.commentL = []
        self.ptime = pt
        self.aid = aid
        self.aem = aem


class reply:
    def __init__(self, c, aid, auname, auem):
        self.content = c
        self.aid = aid
        if aid == None or aid == 'skip':
            self.userC = None
        else:
            self.userC = sql.search('users', 'id='+str(aid))[0]
        self.authorName = auname
        self.authorEmail = auem

    def desuct(self):
        return str(self.content)+" "+str(self.aid) +\
            " "+str(self.userC)+" "+str(self.authorName)+" "\
            + str(self.authorEmail)

    def build(self, desc):
        lm = desc.split(" ")
        self.content = lm[0]
        self.aid = lm[1]
        self.userC = lm[2]
        self.authorName = lm[3]
        self.authorEmail = lm[4]


pl = []


class SQL():
    # SQL function returns a tuple, 0 pos is a status code, 1 pos is index.
    # -1 stands for error,1 for OK.
    #
    def __init__(self):
        # self.host = '127.0.0.1'
        # self.user = 'root'
        # self.port = 3306
        # self.password = 'xteclab'
        # self.charset = 'utf8'
        # self.db = 'lfm'
        # self.conn = None
        # self.cursor = None
        # self.debug = True
        self.host = r'Your MySQL Host Here'  # Replace with your actual MySQL host
        self.user = r'Your MySQL User Here'  # Replace with your actual MySQL user
        self.port = 3306  # Default MySQL port  (Or change it if needed)
        # Replace with your actual MySQL password
        self.password = 'Your MySQL Password Here'
        self.charset = r'utf8'
        self.db = r'Database Name Here'  # Replace with your actual database name
        self.conn = None
        self.cursor = None
        self.debug = True

    def connectSql(self):
        '''
        Open a connection to database
        '''
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                charset=self.charset
            )
            self.cursor = self.conn.cursor()
            return 1
        except Exception as e:
            return e

    def search(self, table, content):
        if self.debug:
            print("SQL exec:", "SELECT * FROM %s WHERE %s" % (table, content))
        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute("SELECT * FROM %s WHERE %s" % (table, content))
            return self.cursor.fetchall()
        except Exception as e:
            return e

    def delete(self, table, condition):
        self.conn.ping(reconnect=True)
        try:
            self.cursor.execute("DELETE FROM %s WHERE %s" % (table, condition))
            self.conn.commit()
            return 1
        except Exception as e:
            return e

    def add(self, table, wv, vv):
        self.conn.ping(reconnect=True)
        try:
            self.cursor.execute(
                "INSERT INTO %s(%s) VALUES (%s)" % (table, wv, vv))
            self.conn.commit()
            return 1
        except Exception as e:
            return e

    def update(self, table, uv, vv, condition):
        self.conn.ping(reconnect=True)
        sql = "UPDATE %s SET %s=%s WHERE %s" % (table, uv, vv, condition)
        print("[SQL] update exec:", sql)
        self.cursor.execute(
            sql
        )
        print("SQL exec:", sql)
        try:

            self.conn.commit()
            return 1
        except Exception as e:
            return e

    def advanceSelect(self, wv, table, condition):
        self.conn.ping(reconnect=True)
        try:
            sql = "select %s from %s where %s" % (wv, table, condition)
            self.cursor.execute(sql)
            print("SQL exec:", sql)
            return self.cursor.fetchall()
        except Exception as e:
            return e


init()
app = Flask(__name__)
app.secret_key = 'Your Secret Key Here'  # Replace with your actual secret key
app.permanent_session_lifetime = timedelta(
    hours=1)  # sets session lifetime to one hour
print("[+] Creating SQL session...")
sql = SQL()
ret = 0
res = sql.connectSql()
print(res)
while sql.cursor == None:
    print("Next retry will in 5 sec")
    sleep(5)
    res = sql.connectSql()
    print("SQL cursor:", sql.cursor, "Retry time:", ret,
          "Connect returned with:", res, flush=True)
    ret += 1
    if ret >= 10:
        print("Max retry time exceed!Quitting...")
        break


@app.route("/robots.txt")
def rebot():
    return send_from_directory(app.static_folder, "robots.txt")


@app.errorhandler(500)
def e500(e=None):
    return render_template('403.htm'), 500


@app.route("/fonts/hsr.TTF")
def font():
    return send_file("fonts/hsr.TTF")


@app.route("/forum/fonts/hsr.TTF")
def fmfont():
    return send_file("fonts/hsr.TTF")


@app.errorhandler(Exception)
def handle_exception(error):
    # 在这里写上你的异常处理逻辑
    # 比如日志记录、发送邮件等
    return render_template("error.htm", ec=error), 500


@app.route("/errorpage/<id>")
def eid(id):
    abort(int(id))


@app.route("/")
def into():
    return render_template("into.htm")


@app.route("/home")
def home():
    return render_template("login_remake.htm")


@app.route("/about-us")
def abus():
    abort(404)


@app.route("/home/login", methods=["POST"])
def login():
    print("|[LOGIN]")
    print("|[+]Inbound new login request. Type: {}, with data: {}".format(request.method, request.form))
    res = make_response("OK")
    session.clear()
    # if request.method == "GET":
    #     print("Legacy login mode")

    #     sname = request.args.get('name')
    #     password = request.args.get('password')
    #     ress = sql.search('users', 'name=\"{0}\"'.format(sname))
    #     print(ress)
    #     print(
    #         "|____[+] Handling login request from uname: {} with pwd: {}".format(sname, password))
    #     try:
    #         if password == ress[0][2]:
    #             # Legacy cookie don't use
    #             # res.set_cookie("username", sname)
    #             # res.set_cookie("password", password)
    #             # res.set_cookie("uid", str(ress[0][0]))
    #             session['username'] = sname
    #             session['password'] = password
    #             session['uid'] = str(ress[0][0])
    #             return res
    #     except:
    #         print(
    #             "|___ [!] Username not found, operating backup plan... (For Chinese characters)")

    #         scname = urlencode(sname)
    #         ress = sql.search('users', 'name=\"{0}\"'.format(scname))
    #         if password == ress[0][2]:
    #             # Legacy cookie don't use
    #             # res.set_cookie("username", sname)
    #             # res.set_cookie("password", password)
    #             # res.set_cookie("uid", str(ress[0][0]))
    #             session['username'] = scname
    #             session['password'] = password
    #             session['uid'] = str(ress[0][0])
    #             return res

    #     return 'username or password incorrect'
    sname = request.form['name']
    password = request.form['password']
    ress = sql.search('users', 'name=\"{0}\"'.format(sname))
    print(ress)
    pres = "Failed"
    npw = ph.hash(password)
    print(
        "|____[+] Handling login request from uname: {} with pwd: {}".format(sname, password))
    try:
        if password == ress[0][2] and ress[0][6] == 1:
            # Legacy cookie don't use
            # res.set_cookie("username", sname)
            # res.set_cookie("password", password)
            # res.set_cookie("uid", str(ress[0][0]))
            session['username'] = sname
            session['password'] = password
            session['uid'] = str(ress[0][0])
            print(
                "|____[+] Updating password hash for: {} (id: {})".format(sname, ress[0][0]))
            npw = ph.hash(password)
            sql.update("users", "password", "\""+npw +
                       "\"", "id={}".format(ress[0][0]))
            sql.update("users", "pwd_need_update",
                       0, "id={}".format(ress[0][0]))
            return res
        elif ress[0][6] == 0:
            print(
                "|____[+] New password hash login for: {} (id: {})".format(scname, ress[0][0]))
            try:
                pres = ph.verify(str(ress[0][2]), str(password))
            except:
                print(
                    "|____[-] Failed! Storaged {} \n|______ (e) -> {}".format(ress[0][2], e))
                return 'username or password incorrect'
            finally:
                print("|____[+] Password check end. res: {}".format(pres))

            session['username'] = scname
            session['password'] = password
            session['uid'] = str(ress[0][0])

            sql.update("users", "password", "\""+npw +
                       "\"", "id={}".format(ress[0][0]))
            sql.update("users", "pwd_need_update",
                       0, "id={}".format(ress[0][0]))
            return res
    except:
        print(
            "|_____ [!] Username not found, operating backup plan... (For Chinese characters)")
        scname = urlencode(sname)
        ress = sql.search('users', 'name=\"{0}\"'.format(scname))
        if password == ress[0][2] and ress[0][6] == 1:
            # Legacy cookie don't use
            # res.set_cookie("username", sname)
            # res.set_cookie("password", password)
            # res.set_cookie("uid", str(ress[0][0]))
            session['username'] = scname
            session['password'] = password
            session['uid'] = str(ress[0][0])
            print(
                "|_____[+] Updating password hash for: {} (id: {})".format(scname, ress[0][0]))
            npw = ph.hash(password)
            sql.update("users", "password", "\""+npw +
                       "\"", "id={}".format(ress[0][0]))
            sql.update("users", "pwd_need_update",
                       0, "id={}".format(ress[0][0]))
            return res
        elif ress[0][6] == 0:
            print(
                "|_____[+] New password hash login for: {} (id: {})".format(scname, ress[0][0]))
            try:
                pres = ph.verify(str(ress[0][2]), str(password))
            except Exception as e:
                print(
                    "|____[-] Failed! Storaged {} \n|______ (e) -> {}".format(ress[0][2], e))
                return 'username or password incorrect'
            finally:
                print("|____[+] Password check end. res: {}".format(pres))

            session['username'] = scname
            session['password'] = password
            session['uid'] = str(ress[0][0])

            sql.update("users", "password", "\""+npw +
                       "\"", "id={}".format(ress[0][0]))
            sql.update("users", "pwd_need_update",
                       0, "id={}".format(ress[0][0]))
            return res
    return 'username or password incorrect'


@app.route("/home/signin", methods=['GET', "POST"])
def signin():
    print("|[SIGNIN]")
    if request.method == "GET":
        print("|___[+]Using legacy signin mode (GET)")
        sname = request.args.get('name')
        password = request.args.get('password')
        sname, password = urlencode(sname), urlencode(password)
        print("Sign in request get with args:", sname, " ", password)
        print("Checking if username is usable...")
        cc = sql.search("users", 'name=\"{0}\"'.format(sname))
        print("SQL returned with:", cc)

        if len(cc) == 0:
            print('|____[+] Name ok')
            # name is OK:
            phash = ph.hash(password)
            res = sql.add('users', 'name,password,signin_date',
                          '\"{0}\",\"{1}\",Now()'.format(sname, phash))
            userN = sql.search('users', 'name=\"{0}\"'.format(sname))
            if res == 1:
                print("|____[+] Successfully created user")
                res = make_response("OK")
                session.clear()
                # Legacy cookie method don't use...
                # res.delete_cookie("username")
                # res.delete_cookie("password")
                # res.delete_cookie("uid")
                # res.set_cookie("username", sname)
                # res.set_cookie("password", password)
                # res.set_cookie("uid", str(userN[0][0]))
                session['username'] = sname
                session['password'] = password
                session['uid'] = str(userN[0][0])
                return "OK"
            else:
                return str(res)
        else:
            return 'username repeated'
    else:
        sname = request.form['name']
        password = request.form['password']
        sname, password = urlencode(sname), urlencode(password)
        print("|____[+] Sign in request get with args:", sname, " ", password)
        print("Checking if username is usable...")
        cc = sql.search("users", 'name=\"{0}\"'.format(sname))
        print("|____[+] SQL returned with:", cc)

        if len(cc) == 0:
            print('|____[+] Name ok')
            # name is OK:
            phash = ph.hash(password)
            res = sql.add('users', 'name,password,signin_date',
                          '\"{0}\",\"{1}\",Now()'.format(sname, phash))
            userN = sql.search('users', 'name=\"{0}\"'.format(sname))
            if res == 1:
                print("|____[+] Successfully created user")
                res = make_response("OK")
                session.clear()
                # Legacy cookie method don't use...
                # res.delete_cookie("username")
                # res.delete_cookie("password")
                # res.delete_cookie("uid")
                # res.set_cookie("username", sname)
                # res.set_cookie("password", password)
                # res.set_cookie("uid", str(userN[0][0]))
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
    global NEED_UPDATE_FLAG
    global pl
    # uid = request.cookies.get("uid")
    # username = request.cookies.get("username")
    # password = request.cookies.get("password")
    username = session.get("username")
    if NEED_UPDATE_FLAG:
        pl = []

        posts = sql.search('posts', 'True ORDER BY id DESC')
        print("Start post list build session...")
        for i in posts:
            userInfo = sql.search('users', 'id=\"{0}\"'.format(i[3]))
            uiFix = 'none'
            if userInfo[0][5] == None:
                uiFix = 'none'
            else:
                uiFix = userInfo[0][5]
            bp = Post(i[0], unquote(i[1]), i[2], unquote(userInfo[0]
                      [1]), i[4], i[3], getMd5(uiFix))
            pl.append(bp)
        # print(pl)
    return render_template("forum.htm", name=username, l=pl, ver=VERSION, uid=session.get("uid"))


@app.route("/forum/m")
def forumMobile():
    global NEED_UPDATE_FLAG
    global pl
    # uid = request.cookies.get("uid")
    # username = request.cookies.get("username")
    # password = request.cookies.get("password")
    username = session.get("username")
    if NEED_UPDATE_FLAG:
        pl = []

        posts = sql.search('posts', 'True ORDER BY id DESC')
        print("Start post list build session...")
        for i in posts:
            userInfo = sql.search('users', 'id=\"{0}\"'.format(i[3]))
            uiFix = 'none'
            if userInfo[0][5] == None:
                uiFix = 'none'
            else:
                uiFix = userInfo[0][5]
            bp = Post(i[0], unquote(i[1]), i[2], unquote(userInfo[0]
                      [1]), i[4], i[3], getMd5(uiFix))
            pl.append(bp)
        # print(pl)
    return render_template("forum-m.htm", name=username, l=pl, ver=VERSION, uid=session.get("uid"))


@app.route("/forum/verify")
def verify():
    # username = request.cookies.get("username")
    # password = request.cookies.get("password")
    username = session.get("username")
    password = session.get("password")
    res = sql.search('users', 'name=\"{0}\"'.format(username))
    # print(res)
    try:
        if (ph.verify(res[0][2], password)):
            return 'OK'
    except:
        return 'password not match.'
    return 'False'


@app.route("/home/m")
def mobileHome():
    return render_template("login-re-m.htm")


@app.route("/new-post")
def postNt():
    return render_template("np-m.htm", uname=session.get("username"))


@app.route("/forum/post", methods=['POST'])
def post():
    global NEED_UPDATE_FLAG
    if request.method == 'POST':
        # # Process hCaptcha

        # captcha_token = request.form['h-captcha-response']
        # parameters = {
        #     'secret': CAPTCHA_SECRET_KEY,
        #     'response': captcha_token,
        #     'sitekey': '57128e2c-6daa-4f5e-b7ba-36000c8cf7dc'
        # }

        # req = requests.post(
        #     'https://api.hcaptcha.com/siteverify', data=parameters)
        # reqd = req.json()

        # if (reqd['success'] != 'true'):
        #     emsg = str("Captcha-Failure\n Error message:"+str(reqd))
        #     abort(emsg)

        print("received:", request.form)
        t, c, a = request.form['title'], request.form['content'], request.form['author']
        if re.match(forbiddenString, t) or re.match(forbiddenString, c) or re.match(forbiddenString, a):
            abort("Stop Attacking My Site Using This Stupid Pattern!!!!!! :(")
        t, c, a = urlencode(t), urlencode(c), urlencode(a)
        c.replace("\n", '\n')
        if re.match(forbiddenString, t) or re.match(forbiddenString, c) or re.match(forbiddenString, a):
            abort("Stop Attacking My Site Using This Stupid Pattern!!!!!! :(")
        uid = session.get("uid")
        # if "\"" in t or "\'" in t or "\"" in c or "\'" in c:
        #     return 'Illegal Characters!\n非法字符！'
        res = sql.add("posts", "title,content,authorID,P_time",
                      '\"{0}\",\"{1}\",\"{2}\",sysdate()'.format(t, c, uid))
        print("New post received with:", t, c, a)
        NEED_UPDATE_FLAG = True
        if res != 1:
            return str(res)
        return redirect("/forum")
    else:
        abort(500)


@app.route("/user/<id>")
def userHome(id):
    findedUser = sql.search("users", 'id = '+str(id))
    print("User found:", findedUser)

    # sid = request.cookies.get("uid")
    sid = session.get("uid")
    postedPost = sql.search('posts', 'authorID='+str(id))
    print("pp f:", postedPost)
    procPost = []
    for i in postedPost:
        procPost.append([i[0], unquote(i[1]), unquote(i[2])])
    return render_template("user.htm", uid=id, suid=sid, uname=unquote(findedUser[0][1]), p=procPost, email=findedUser[0][5])


@app.route("/user/<id>/changeemail", methods=['GET'])
def changeEmail(id):
    # uid = request.cookies.get("uid")
    uid = session.get("uid")
    print("Received change email form uid:", uid, "for id:", id)
    if id != uid:
        abort(401)
    if request.cookies.get("password") != sql.search('users', 'id='+id)[0][2]:
        abort(401)
    try:
        ne = request.args.get("e")
        ne = urlencode(ne).replace("%40", '@')
        print("received:", request.values)
        if "\"" in ne or "\'" in ne or forbiddenString in request.args.get("e"):
            return 'Illegal Character!'
        sql.update('users', 'email', "\""+str(ne)+"\"", 'id = '+uid)
        return 'OK'
    except Exception as e:
        return str(e)


@app.route("/forum/post/<id>")
def showPostInfo(id):
    print("Invoke reply build session:")
    fp = sql.search("posts", 'id={0}'.format(str(id)))[0]
    fpusr = sql.search('users', 'id={0}'.format(str(fp[3])))[0]
    nsp = Post(i=fp[0], t=unquote(fp[1]), c=fp[2], a=unquote(fpusr[1]),
               pt=fp[4], aid=fpusr[0], aem=getMd5(fpusr[5]))
    print("Getting cache...")

    repl = []
    coms = sql.search('reply', 'ref_to={0}'.format(str(id)))
    print("fetched replys:", coms)
    for rep in coms:
        repl.append(reply(unquote(rep[1]), rep[2], unquote(sql.search('users', 'id={0}'.format(str(rep[2])))[
                    0][1]), getMd5(sql.search('users', 'id={0}'.format(str(rep[2])))[0][5])))
        sp = sql.search('posts', 'id='+str(id))
        su = sql.search('users', 'id='+str(sp[0][3]))
        nsp = Post(id, unquote(sp[0][1]), sp[0][2], unquote(su[0][1]),
                   sp[0][4], su[0][0], getMd5(su[0][5]))
    return render_template('post-nt.htm', p=nsp, replys=repl)


@app.route("/getImage")
def image():
    pictures = listdir("drawings")
    return send_file("drawings/"+pictures[ri(0, len(pictures) - 1)])


@app.route("/post/comment/<id>", methods=['POST'])
def comment(id):
    global NEED_UPDATE_FLAG
    if request.method == 'POST':

        print("received:", request.form)
        c = request.form['content']
        if re.match("%p(.*?%s)*.*?%", str(request.form)):
            abort("Stop Attacking My Site Using This Weird Pattern!!!!!! :(")
        if re.match("%p(.*?%s)*.*?%", c):
            abort("Stop Attacking My Site Using This Weird Pattern!!!!!! :(")
        if re.match("%p(.*?%s)*.*?%", unquote(str(request.form))):
            abort("Stop Attacking My Site Using This Weird Pattern!!!!!! :(")
        c = urlencode(c)
        if re.match("%p(.*?%s)*.*?%", c):
            abort("Stop Attacking My Site Using This Weird Pattern!!!!!! :(")
        aid = session.get("uid")
        res = sql.add('reply', 'content,authorID,ref_to',
                      '\'{0}\',\'{1}\',\'{2}\''.format(c, aid, id))
        if c == None or c == '':
            return "Empty content!"
        if res != 1:
            return str(res)
        return redirect("/forum/post/{0}".format(id))
    else:
        abort(405)


@app.route("/md-playground")
def mdpg():
    return render_template('md.html')
