# import all necessary libraries

from app.Indoor_air_quality.routes import display_dashboard
from flask import render_template, redirect,request, flash, redirect, url_for
from wtforms.widgets.core import CheckboxInput
from app.auth.forms import RegistrationForm
from app.auth.forms import UserloginForm
from app.auth import authentication as at
from app.auth.models import User
from flask_login import login_user,logout_user, login_required, current_user
from flask_jwt_extended import create_access_token
from flask import jsonify


# route signup form

@at.route('/signup', methods=['GET', 'POST'])
def signup():
    
    form = RegistrationForm()
    if current_user.is_authenticated:
        flash('You are already logged-in')
        return redirect(url_for('main.display_dashboard'))
    if form.validate_on_submit():
        User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data)
        flash('Signup Sucessfuly')
        return redirect(url_for('authentication.do_the_login'))

    return render_template('signup.html', form=form)


# route landing page 

@at.route('/', methods=['GET', 'POST'])
def do_the_login():
    if current_user.is_authenticated:
        flash('You are already logged-in')
        return redirect(url_for('main.display_dashboard'))
    form = UserloginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.name.data).first()

        if not user or not user.check_password(form.password.data):
            flash('Invalid Credentials, Please try again')
            return redirect(url_for('authentication.do_the_login'))

        # # Create JWT token
        # access_token = create_access_token(identity=user.id)

        # # You can return this token as a JSON response or store it in cookies
        # return jsonify(access_token=access_token), 200

        login_user(user, form.remember_me.data)
        return redirect(url_for('main.display_dashboard'))
    return render_template('login.html', form=form)

# route lagout page

@at.route('/logout')
@login_required
def log_out_user():
    logout_user()
    flash('you are loged-out')
    return redirect(url_for('authentication.do_the_login'))

