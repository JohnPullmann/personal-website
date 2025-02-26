from flask import render_template, session, Blueprint, flash, request, redirect, url_for
from website.main.forms import ContactMe
from flask_mail import Message
from website import mail, database
from website.models import PortfolioElement, Project, Work, Education, Certification
from sqlalchemy import desc, asc, union_all
from website.main.utils import filter_portfolio_elements, build_portfolio_timeline
from flask import current_app
from flask import session
from flask_wtf.csrf import generate_csrf
from bs4 import BeautifulSoup
from website.users.forms import AddPortfolio_Comment
from website.models import User, Portfolio_Comment
from flask_login import current_user
from datetime import datetime


main = Blueprint('main', __name__) 

@main.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('main.home'))

@main.route('/home', methods=['GET', 'POST'])
def home():
    # home route
    # Contact me form
    form = ContactMe()
    session['_csrf_token'] = generate_csrf()  # Manually generate and store a CSRF token in the session

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
    timespan = request.args.get('timespan')

    PortfolioElements = filter_portfolio_elements(button, search, sort, timespan)
    PortfolioElements = PortfolioElements.paginate(page=page, per_page=4)

    portfolio_timeline = build_portfolio_timeline() # TODO global creating

    return render_template('portfolio.html', title='Portfolio', PortfolioElements=PortfolioElements, timeline=portfolio_timeline, timespan=timespan, button=button, sort=sort, search=search)


@main.route('/resume')
def resume():
    # resume route
    resume_lang = request.args.get('resume_lang')
    if not resume_lang:
        resume_lang = 'en'

    return render_template('resume.html', title='Resume', resume_lang=resume_lang)

@main.route('/toggle_theme', methods=['POST'])
def toggle_theme():
    theme = request.json.get('theme')
    session['theme'] = theme
    return '', 204

@main.route('/portfolio/<string:element_type>/<string:element_name>', methods=['GET', 'POST'])
def portfolio_element_page(element_type, element_name):
    #get the element from the database
    element = PortfolioElement.query.filter_by(type=element_type, url_name=element_name).first_or_404()
    
    form = AddPortfolio_Comment()
    if form.validate_on_submit():
        comment = Portfolio_Comment(user_id=current_user.id, author_object=current_user, content=form.content.data, date_posted=datetime.utcnow(), portfolio_element_id=element.id)
        with current_app.app_context():
            database.session.add(comment)
            database.session.commit()
        return redirect(url_for('main.portfolio_element_page', element_type=element_type, element_name=element_name))

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
    timespan = request.args.get('timespan')
    PortfolioElements = filter_portfolio_elements(button, search, sort, timespan)
    PortfolioElements = PortfolioElements.paginate(page=page, per_page=4)

    portfolio_timeline = build_portfolio_timeline() # TODO global creating

    return render_template('portfolio_element.html', title='Portfolio', form=form, PortfolioElements=PortfolioElements, timeline=portfolio_timeline, timespan=timespan, PortfolioElementSelected=element, OrderedImages=OrderedImages, SvgContents=svg_contents)

@main.route('/testing')
def testing():
    return render_template('testing.html', title='Testing')