from models.blog import Blog
from database import Database
from datetime import datetime


class Menu(object):
    def __init__(self):
        # ask user for authors name
        # check does user exist
        # if not, promt to create a new user
        self.user = input("Enter the authors name: ").strip().title()
        self.user_blog = None
        if self._user_has_account():
            print(f"Welcome back {self.user}.")
        else:
            self._prompt_user_for_account()

    def _user_has_account(self):
        blog = Database.find_one(collection="blogs", query={"blog_author": self.user})
        if blog is not None:
            self.user_blog = Blog.get_blog_by_id(blog["blog_id"])
            return True
        else:
            return False

    def _prompt_user_for_account(self):
        title = input("Enter the title of the blog: ")
        description = input("Enter the description of the blog: ")
        blog = Blog(author=self.user, title=title, description=description)
        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):
        choice = input("Do you want to read or write blogs? (r/w) \nFor exit press q: ").lower().strip()
        while choice != "q":
            if choice == "r":
                # list all blogs
                # pick one blog and show posts
                self._list_blogs()
                self._view_blog()
            elif choice == "w":
                # write new post in author's blog
                self.user_blog.new_post()
            else:
                print(f"Your choice was {choice}. Wrong choice. Try again.")
            choice = input("Do you want to read or write blogs? (r/w) \nFor exit press q: ").lower().strip()

    @staticmethod
    def _list_blogs():
        blogs = Database.find(collection="blogs", query={})
        for blog in blogs:
            print(f"ID: {blog['blog_id']}, Title: {blog['blog_title']}, Author: {blog['blog_author']}")

    @staticmethod
    def _view_blog():
        try:
            my_id = input("Enter the blog id you want to see: ")
            blog = Blog.get_blog_by_id(my_id)
            posts = blog.get_all_posts()
            for post in posts:
                print(f"Title: {post['title']}, Data: {datetime.strftime(post['created_date'], '%Y-%m-%d')}, Contant: {post['content']}")
        except:
            print("Wrong ID. Try again.")

