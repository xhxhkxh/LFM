"""Small classes extracted from app.py for posts and replies."""


class Post:
    def __init__(self, i, t, c, a, pt, aid, aem):
        self.id = i
        self.title = t
        self.content = c
        self.author = a
        self.post_time = pt
        self.author_id = aid
        self.author_email_md5 = aem


class Reply:
    def __init__(self, content, author_id, author_name, author_email_md5):
        self.content = content
        self.author_id = author_id
        self.author_name = author_name
        self.author_email_md5 = author_email_md5
