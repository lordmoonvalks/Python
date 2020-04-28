import os
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Journal
from flaskblog.posts.forms import PostForm
from flaskblog.base.utils import save_file

from flaskblog import f

posts = Blueprint('posts', __name__)


# route for posts & usage of forms
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        file_path = ''
        if form.upload_file.data:###adding file to database
            uploaded_file = save_file(form.upload_file.data)
            file_path = uploaded_file##remove if dont want to add to database
        print(form.title.data)
        print(form.content.data)
        post = Post(title=f.encrypt(bytes(form.title.data, 'utf-8')), content=f.encrypt(bytes(form.content.data, 'utf-8')), author=current_user,  # encrypt using frnet (title and content)
                    upload_file=file_path)  # bind author to current user

        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('base.home'))  # redirect to home directory after posting
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


# routing posts (when i click on it)
@posts.route("/post/<int:post_id>")  # id'ing posts
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)  # give me post with id , if doesnt exist = 404

    post.title = f.decrypt(post.title).decode() #decrypt posts using fernet
    post.content = f.decrypt(post.content).decode()

    return render_template('post.html', title=post.title, post=post)



#post update
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)  # give me post with id , if doesnt exist = 404
    if post.author != current_user:  # don't let update posts if not logged as blog owner
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = f.encrypt(bytes(form.title.data, 'utf-8'))
        post.content = f.encrypt(bytes(form.content.data, 'utf-8'))
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = f.decrypt(post.title).decode()
        form.content.data = f.decrypt(post.content).decode()
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

#post delete
@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:  # don't let update posts if not logged as blog owner
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('base.home'))


# routes for journals

#new journal
@posts.route("/journal/new", methods=['GET', 'POST'])
@login_required
def new_journal():
    form = PostForm()
    if form.validate_on_submit():
        file_path = ''
        if form.upload_file.data:
            uploaded_file = save_file(form.upload_file.data)
            file_path = uploaded_file
        journal = Journal(title=f.encrypt(bytes(form.title.data, 'utf-8')), content=f.encrypt(bytes(form.content.data, 'utf-8')), # encrypt using frnet (title and content)
                          author=current_user, upload_file=file_path)  # bind author to current user
        # add posts to database
        db.session.add(journal)
        db.session.commit()
        flash('Journal created!', 'success')
        return redirect(url_for('base.home'))  # redirect to home directory after posting
    return render_template('create_journal.html', title='New Journal', form=form, legend='New Journal')


@posts.route("/journal/<int:journal_id>")  # id'ing journals 
@login_required
def journal(journal_id):
    journal = Journal.query.get_or_404(journal_id)  # give me journals  with id , if doesnt exist = 404
    if journal.author != current_user:  # block access for other users to private journal as journals are visible only by account owner
        abort(403)

    journal.title = f.decrypt(journal.title).decode() #decrypt using fernet
    journal.content = f.decrypt(journal.content).decode()
    return render_template('journal.html', title=journal.title, journal=journal)


@posts.route("/journal/<int:journal_id>/update", methods=['GET', 'POST'])
@login_required
def update_journal(journal_id):
    journal = Journal.query.get_or_404(journal_id)  # give me post with id , if doesnt exist = 404
    if journal.author != current_user:  # don't let update posts if not logged as blog owner
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        journal.title = f.encrypt(bytes(form.title.data, 'utf-8'))
        journal.content = f.encrypt(bytes(form.content.data, 'utf-8'))
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.journal', journal_id=journal.id))
    elif request.method == 'GET':
        form.title.data = f.decrypt(journal.title).decode()
        form.content.data = f.decrypt(journal.content).decode()
    return render_template('create_journal.html', title='Update Journal', form=form, legend='Update Journal')


@posts.route("/journal/<int:journal_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_Journal(journal_id):
    journal = Journal.query.get_or_404(journal_id)
    if journal.author != current_user:  # don't let update posts if not logged as blog owner
        abort(403)
    db.session.delete(journal)
    db.session.commit()
    flash('Your journal has been deleted', 'success')
    return redirect(url_for('base.home'))

#

# @osts.route("/post_upload_file", methods=["GET", "POST"])
# def post_upload_image():
#
#   if request.method == "POST":
#
#       if request.files:
#
#           file = request.files["file"]
#
#        file.save(os.path.join(app.config["FILE_UPLOADS"], file.filename))
#
#           print("File Attached")
#
##
#          return redirect(request.url)
#
#   return render_template("public/post_upload_file.html")
#
