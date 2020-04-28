from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    upload_file = FileField('Update File', validators=[FileAllowed(['mp3', 'mp4', 'jpg', 'png', 'avi', 'mpg', 'mpeg'])])
