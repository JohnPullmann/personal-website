from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # home route
    ...
    return render_template('home.html', title='Home')

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