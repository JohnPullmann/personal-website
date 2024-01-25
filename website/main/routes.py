from flask import render_template, session, Blueprint, flash
from flask import request
from website.main.forms import ContactMe
from flask_mail import Message
from website import mail
from flask import redirect, url_for


main = Blueprint('main', __name__)  # Use 'dark' as the default theme

@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
    # home route
    ...
    # Contact me form
    form = ContactMe()
    if form.validate_on_submit():
        msg = Message('New contact form submission',
                      sender='webtesting489@gmail.com',
                      recipients=['john.pullmann@gmail.com'])
        msg.body = f"From: {form.name.data} \r\nEmail: {form.email.data}\r\nMessage: {form.message.data}"
        msg.html = render_template('emails/contact-me.html' , name=form.name.data, email=form.email.data, message=form.message.data)
        mail.send(msg)
        flash('Success! You message has been sent.', 'success')

        return redirect(url_for('main.home') + "#contact-me")


    return render_template('home.html', title='Home', form=form)	

@main.route('/portfolio')
def portfolio():
    # portfolio route
    ...
    return render_template('portfolio.html', title='Portfolio')

@main.route('/resume')
def resume():
    # resume route
    ...
    return render_template('resume.html', title='Resume')

@main.route('/toggle_theme', methods=['POST'])
def toggle_theme():
    theme = request.json.get('theme')
    session['theme'] = theme
    return '', 204