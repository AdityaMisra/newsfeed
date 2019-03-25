import datetime
from collections import defaultdict

from newsfeed.entities import User, Post, Comment


class NewsFeed(object):
    def __init__(self):
        self.users = []
        self.user_name_mapping = {}

        self.posts = []
        self.post_id_mapping = {}

        self.comments = []
        self.post_comments_mapping = defaultdict(lambda: list())

    def sign_up(self, name):
        _id = len(self.users) + 1
        user = User(_id, name)

        self.users.append(user)
        self.user_name_mapping.update({name: user})

    def login(self, username):
        user = self.check_valid_user(username)
        if not user:
            return

        self.show_news_feed(user)

    def post(self, message, username):

        user = self.check_valid_user(username)
        if not user:
            return

        _id = len(self.posts) + 1

        post = Post(_id, message, user, datetime.datetime.now())
        self.posts.append(post)
        self.post_id_mapping.update({_id: post})

        user.posts.append(post)

    def check_valid_user(self, username):
        user = None
        try:
            user = self.user_name_mapping[username]
        except KeyError:
            print("Please sign up first!")
        return user

    def comment_on_post(self, post_id, comment, username):
        user = self.check_valid_user(username)
        if not user:
            return

        post = self.post_id_mapping.get(post_id)
        if not post:
            return

        _id = len(self.comments) + 1
        comment = Comment(_id, user, post, comment, datetime.datetime.now())
        self.comments.append(comment)

        self.post_comments_mapping[post].append(comment)
        post.number_of_comments += 1

    def up_vote_on_post(self, post_id, username):
        user = self.check_valid_user(username)
        if not user:
            return

        post = self.post_id_mapping.get(post_id)
        if not post:
            return

        post.up_votes += 1

    def down_vote_on_post(self, post_id, username):
        user = self.check_valid_user(username)
        if not user:
            return

        post = self.post_id_mapping.get(post_id)
        if not post:
            return

        post.down_votes += 1

    def follow(self, username, followee_username):
        user = self.check_valid_user(username)
        if not user:
            return

        followee_user = self.check_valid_user(followee_username)
        if not followee_user:
            return

        user.followees.append(followee_user)

    def show_news_feed(self, user):
        final_post_list = []

        followees = user.followees
        followee_post_list = []

        user_followee_set = set(followees)
        all_users = set(self.users)

        for each_followee in followees:
            followee_post_list.extend(each_followee.posts)

        followee_post_list = sorted(followee_post_list,
                                    key=lambda x: (x.up_votes - x.down_votes, x.number_of_comments, x.timestamp),
                                    reverse=True)

        non_followee_post_list = []
        non_followee_users = all_users - user_followee_set

        for each_user in non_followee_users:
            non_followee_post_list.extend(each_user.posts)

        non_followee_post_list = sorted(non_followee_post_list,
                                        key=lambda x: (x.up_votes - x.down_votes, x.number_of_comments, x.timestamp),
                                        reverse=True)

        final_post_list.extend(followee_post_list)
        final_post_list.extend(non_followee_post_list)

        self.print_posts(final_post_list)

    def print_posts(self, post_list):
        for post in post_list:
            comments = self.post_comments_mapping.get(post, [])
            print("id: {}\n"
                  "({} upvotes, {} downvotes)\n"
                  "{}\n"
                  "{}\n"
                  "{}\n".
                  format(post.id, post.up_votes, post.down_votes, post.user.name, post.post_message,
                         post.timestamp.strftime('%Y-%m-%d %I:%M %p')))

            for idx, comment in enumerate(comments, 1):
                tabs = '\t'*1
                print("{}id: {}\n"
                      "{}{}\n"
                      "{}{}\n"
                      "{}{}\n".
                      format(tabs, comment.id,
                             tabs, comment.user.name,
                             tabs, comment.comment,
                             tabs, comment.timestamp.strftime('%Y-%m-%d %I:%M %p')))


def test_run():
    n = NewsFeed()
    n.login('aditya')
    n.sign_up('aditya')
    n.login('aditya')
    n.post('hi test message', 'aditya')
    n.sign_up('test1')
    n.sign_up('test2')
    n.login('test1')
    n.up_vote_on_post(1, 'aditya')
    n.login('test1')
    n.follow('test1', 'test2')
    n.login('test2')
    n.post('hello flipkart', 'test2')
    n.post('hello bangalore', 'test2')
    n.comment_on_post(1, 'hi there!', 'test2')
    n.down_vote_on_post(1, 'test2')
    n.login('test1')
    n.post('Hi India', 'test2')
    n.post('Hi Karnataka', 'test2')
    n.post('Hi Bengaluru', 'test2')
    n.post('yoyoyoy', 'aditya')
    n.post('Hello Delhi', 'aditya')
    n.post('Hello Walmart', 'aditya')
    n.up_vote_on_post(2, 'aditya')
    n.up_vote_on_post(2, 'aditya')
    n.up_vote_on_post(2, 'aditya')
    n.up_vote_on_post(2, 'aditya')

