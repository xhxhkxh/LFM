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
from modules import config, db as db_module, errors as errors_module, forum as forum_module
from classes.post import Post, Reply

# 初始化全局变量
VERSION = "1.0.0"
NEED_UPDATE_FLAG = True
pl = []
forbiddenString = r"(?i)(script|select|insert|update|delete|drop|;|--)"

# 辅助函数


def getMd5(s):
    import hashlib
    return hashlib.md5(s.encode('utf-8')).hexdigest() if s else 'none'


# Post/Reply classes moved to classes/post.py


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

    # 注册蓝图（从 route 包统一导出）
    try:
        from route import blueprints
        for bp in blueprints:
            app.register_blueprint(bp)
    except Exception as e:
        print('Failed to import/register route.blueprints:', e)

    # 注册错误处理器
    errors_module.register_error_handlers(app)

    return app


# 创建应用实例
app = create_app()

# 路由已迁移到 route 目录下的各文件

if __name__ == '__main__':
    # Enable a temporary self-signed certificate for development HTTPS
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
