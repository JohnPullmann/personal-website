from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from website import database, bcrypt
from website.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from website.models import User
from flask_login import login_user, current_user, logout_user
from website.users.forms import UpdateAccountForm
from website.users.utils import save_picture, send_reset_email
from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        with current_app.app_context():
            database.create_all()
            user = User(username=form.username.data, email = form.email.data, password=hashed_password)
            database.session.add(user)
            database.session.commit()

        flash(f"Your account has been created!", 'success')
        next_page = request.args.get('next')
        return redirect(url_for('users.login', next=next_page)) if next_page else redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        with current_app.app_context():
            database.create_all()
            user= User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page= request.args.get('next')

                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    next_page= request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file= picture_file
        current_user.username = form.username.data
        database.session.commit()
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/users/profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) 
    form = RequestResetForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login')) 
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token): 
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) 
    user= User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request')) 
    form= ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print("new-------", hashed_password)
        print("old-------", user.password)
        user.password = hashed_password
        database.session.commit()
        flash(f"Your password has been updated and you can now log in!", 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
