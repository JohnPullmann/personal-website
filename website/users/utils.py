import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from website import mail
from flask import render_template

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext= os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/users/profile_pics/', picture_fn)
    output_size= (125, 125)
    i= Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    msg.html = render_template('emails/reset-password.html' , reset_url=url_for('users.reset_token', token=token, _external=True), account_name=user.username, account_email=user.email)

    mail.send(msg)
