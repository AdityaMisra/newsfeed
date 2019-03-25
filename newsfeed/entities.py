import datetime


class User(object):
    def __init__(self, _id, name):
        self.id = _id
        self.name = name
        self.followees = []
        self.posts = []


class Post(object):
    def __init__(self, _id, message, user, timestamp=datetime.datetime.now()):
        self.id = _id
        self.post_message = message
        self.up_votes = 0
        self.down_votes = 0
        self.user = user
        self.timestamp = timestamp
        self.number_of_comments = 0


class Comment(object):
    def __init__(self, _id, user, post, comment, timestamp=datetime.datetime.now()):
        self.id = _id
        self.user = user
        self.post = post
        self.comment = comment
        self.timestamp = timestamp
