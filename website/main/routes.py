from flask import render_template, session, Blueprint, flash, request, redirect, url_for
from website.main.forms import ContactMe
from flask_mail import Message
from website import mail, database
from website.models import PortfolioElement, Project, Work, Education, Certification
from sqlalchemy import desc, asc, union_all
from website.main.utils import filter_portfolio_elements
from flask import current_app
from flask import session
from flask_wtf.csrf import generate_csrf
from bs4 import BeautifulSoup



main = Blueprint('main', __name__) 

@main.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('main.home'))

@main.route('/home', methods=['GET', 'POST'])
def home():
    # home route
    ...
    # Contact me form
    form = ContactMe()
    session['_csrf_token'] = generate_csrf()  # Manually generate and store a CSRF token in the session
    #print(session.get('csrf_token'))
    #print(session)
    if form.validate_on_submit():
        try:
            msg = Message('New contact form submission',
                        sender=current_app.config['MAIL_USERNAME'],
                        recipients=['john.pullmann@gmail.com'])
            msg.body = f"From: {form.name.data} \r\nEmail: {form.email.data}\r\nMessage: {form.message.data}"
            msg.html = render_template('emails/contact-me.html' , name=form.name.data, email=form.email.data, message=form.message.data)
            mail.send(msg)
            flash('Success! You message has been sent.', 'success')

            return redirect(url_for('main.home') + "#contact-me")
        except Exception as e:
            flash(f'Failed to send email. {e}', 'fail')
    

    return render_template('home.html', title='Home', form=form)	

@main.route('/portfolio')
def portfolio():
    # portfolio route
    ...
    page = request.args.get('page', 1, type=int)

    # Create database if it doesn't exist
    database.create_all()

    # Get parameters from query
    button = request.args.get('button')
    sort = request.args.get('sort')
    search = request.args.get('search')

    PortfolioElements = filter_portfolio_elements(button, search, sort)
    PortfolioElements = PortfolioElements.paginate(page=page, per_page=4)

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

    #get the element from the database
    element = PortfolioElement.query.filter_by(type=element_type, url_name=element_name).first_or_404()
    OrderedImages = element.images[1:len(element.images)//2+1] + [element.images[0]] + element.images[len(element.images)//2+1:]

    # Read the SVG files and store their contents in a dictionary
    svg_contents = {}

    for tag in element.tags:
        with current_app.open_resource('static/images/tags/' + tag.name + '.svg') as f:
            svg_contents[tag.name] = f.read().decode('utf-8')

    #Base for portfolio element website in the background
    page = request.args.get('page', 1, type=int)
    # Create database if it doesn't exist
    database.create_all()
    # Get parameters from query
    button = request.args.get('button')
    sort = request.args.get('sort')
    search = request.args.get('search')
    PortfolioElements = filter_portfolio_elements(button, search, sort)
    PortfolioElements = PortfolioElements.paginate(page=page, per_page=4)

    return render_template('portfolio_element.html', title='Portfolio', PortfolioElements=PortfolioElements, PortfolioElementSelected=element, OrderedImages=OrderedImages, SvgContents=svg_contents)