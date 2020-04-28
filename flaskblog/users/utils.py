import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

#saving user's avatar
#os and root app to give app all the way to the packet directory

def save_picture(form_picture):
    #hex as base of file name (8 bytes)
    random_hex = secrets.token_hex(8) #checking valid extension  
    _, f_ext, = os.path.splitext(form_picture.filename)  #os moduleto grab file extension from uploaded file 
    picture_fn = random_hex + f_ext 
    picture_path = os.path.join(current_app.root_path, 'static/profilepic', picture_fn) #os check if it concatinates correctl
    
    #image resizing
    #using pillow imported pacckage to resize uploaded users avatars to 125,125 so it doesnt take space and slow dont the page
    output_size = (125, 125)
    i = Image.open(form_picture)#pulling from form_picture below 
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

##reset email function
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='flaskismine@gmail.com', recipients=[user.email]) #this is a sample gmail.com account that i created for this Coursework project.
    msg.body = f'''To reset your password, click the link:
{url_for('users.reset_token', token=token, _external=True)} 

If you did not request password reset , you should ignore this email and contact administrator.   
'''
        
    mail.send(msg)


