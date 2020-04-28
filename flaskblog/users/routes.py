from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post, Journal, Logs
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email
import requests
from flaskblog import f

users = Blueprint('users',__name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: #if user is logged in redirect on login/register to home page 
        return redirect(url_for('home'))


#register using bcrypt for hashing passwords securely in db

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration complete, please log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

# login route / comparing data from db
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base.home')) #if user is logged in redirect on login/register to home page 
    form = LoginForm()
    if form.validate_on_submit():  #check if email exist in db
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): #compare the password in db and bcrypted hash
            login_user(user, remember=form.remember.data ) 
            

            #after user is logged in.. we save the logs into the database
            ip_address = request.remote_addr
            print(ip_address)
            print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))

            if ip_address == "127.0.0.1":
                print("HERE")
                response = requests.get("http://ip-api.com/json/")
            else:
                response = requests.get("http://ip-api.com/json/{}".format(ip_address))    
            js = response.json()
            print(js)

            log = Logs(user_id=user.id, country=js["country"], ip_addr=js["query"]) #get ip addr and coutry
            db.session.commit() # add to db

            print(log) 

            #after login use reqdirect/request for redirect to next page if exist y/n if n go home page
            next_page = request.args.get('next')  
            return redirect(next_page) if next_page else redirect(url_for('base.home'))   #if the next_page arg is emptyredirect to home dir
        else:
            flash('Login Unsuccessful , wrong credentials', 'danger')
    return render_template('login.html', title='Login', form=form) #return login page if wrong credentials

#logout route
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('base.home'))


#account route with login_requred decorator
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm() # use acc update import for image updates
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account details updated!', 'success')
        return redirect(url_for('users.account')) # redirect back to account page after update 
    elif request.method == 'GET':     # populate data for update
        form.username.data = current_user.username
        form.email.data = current_user.email
    #set default avatar
    image_file = url_for('static', filename='profilepic/' + current_user.image_file) # name of the column storing images in models.py
    return render_template('account.html', title='Account', image_file=image_file, form=form)

#route for displaying blogs by username
@users.route("/user/<string:username>") #string username 
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user) 

#route for password reset

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('base.home'))
    form = RequestResetForm()
    if form.validate_on_submit(): #validate user
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user) # send email with link to reset pswd
        flash('An email has been sent with instructions')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Forgot Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('base.home')) #if worked redirect to t home
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password #hashing from form.password.data
        db.session.commit() #commit changes to user password in DB
        flash('Your passowrd has been updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Forgot Password', form=form)


## user's myblog page where they can see all their blogs

@users.route("/myblog")
def myblog():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username ).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5) # didnt have time to finish pagination :)
    #print all account owners posts
    for i, items in enumerate(posts.items):
        print(i, items)
        print(posts.items[i].title)
        posts.items[i].title = f.decrypt(posts.items[i].title).decode()
        posts.items[i].content = f.decrypt(posts.items[i].content).decode()   
        
    return render_template('myblog.html', posts=posts, user=user) 


@users.route("/private_journal")
@login_required
def private_journal():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username ).first_or_404()
    journals = Journal.query.filter_by(author=user)\
        .order_by(Journal.date_posted.desc())\
        .paginate(page=page, per_page=100) #didnt have time to finish pagination for private journals :)

    for i, items in enumerate(journals.items):
        print(i, items)
        print(journals.items[i].title)
        journals.items[i].title = f.decrypt(journals.items[i].title).decode()
        journals.items[i].content = f.decrypt(journals.items[i].content).decode()
    return render_template('private_journal.html', journals=journals, user=user) 

    

@users.route("/user/<string:username>") #string username 
@login_required
def user_journals(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    journals = Journal.query.filter_by(author=user)\
        .order_by(Journal.date_posted.desc())\
        .paginate(page=page, per_page=100)
    return render_template('user_journals.html', journals=journals, user=user) 