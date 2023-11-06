from flask import render_template
from website import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', title='Portfolio')

@app.route('/resume')
def resume():
    return render_template('resume.html', title='Resume')