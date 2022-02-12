from database import Database
from models.post import Post

import uuid
import datetime


class Blog(object):
    def __init__(self, author, title, description, id=None):
        self.author = author
        self.title = title
        self.description = description
        self.id = uuid.uuid4().hex if id is None else id

    def save_to_mongo(self):
        Database.insert(collection="blogs", data=self.json())

    def json(self):
        return {
            "blog_id": self.id,
            "blog_author": self.author,
            "blog_title": self.title,
            "blog_description": self.description
        }

    def new_post(self):
        title = input("Enter the title of the post: ")
        content = input("Enter the content of the post: ")
        date = input("Enter the date (in format DDMMYYYY) or leave it blank for today: ")
        post = Post(blog_id=self.id,
                    title=title,
                    content=content,
                    author=self.author,
                    date=datetime.datetime.strptime(date, "%d%m%Y") if date != "" else datetime.datetime.utcnow())
        post.save_to_mongo()

    def get_all_posts(self):
        return Post.find_all_posts_by_blog_id(self.id)

    @classmethod
    def get_blog_by_id(cls, blog_id):
        blog_data = Database.find_one(collection="blogs", query={"blog_id": blog_id})
        return cls(author=blog_data["blog_author"],
                   title=blog_data["blog_title"],
                   description=blog_data["blog_description"],
                   id=blog_data["blog_id"])
