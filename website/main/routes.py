from flask import render_template, session, Blueprint, flash, request, redirect, url_for
from website.main.forms import ContactMe
from flask_mail import Message
from website import mail, database
from website.models import PortfolioElement, Project, Work, Education, Certification



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

    # Create database if it doesn't exist
    database.create_all()

    # Get elements from database
    PortfolioElements = PortfolioElement.query.all()
    Projects = Project.query.all()
    Works = Work.query.all()
    Educations = Education.query.all()
    Certifications = Certification.query.all()


    return render_template('portfolio.html', title='Portfolio', PortfolioElements=PortfolioElements)

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

@main.route('/portfolio/<string:element_type>/<string:element_name>')
def portfolio_element_page(element_type, element_name):
    # portfolio element route
    ...

    '''
    # Create database if it doesn't exist
    database.create_all()

    # Get element from database
    element = PortfolioElement.query.filter_by(type=element_type, url_name=url_name).first_or_404()

    return render_template('portfolio-element.html', title=element.name, element=element)
    '''