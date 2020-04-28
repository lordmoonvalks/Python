from flask import render_template, request, Blueprint
from flaskblog.models import Post
from flask_login import login_required
from flaskblog import f

base = Blueprint('base',__name__)

@base.route("/")
@base.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=7) #page pagination linked with home page
    ##show posts of all users (decrypt them using fernet)
    print(posts.items)
    # print(posts.post)
    for i, items in enumerate(posts.items):
        print(i, items)
        print(posts.items[i].title)
        posts.items[i].title = f.decrypt(posts.items[i].title).decode()
        posts.items[i].content = f.decrypt(posts.items[i].content).decode()
    return render_template('home.html', posts=posts) 


@base.route("/about")
def about():
    return render_template('about.html', title='About')



