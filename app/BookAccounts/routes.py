# import all the necessary library

from os import error
from sqlalchemy import orm
from sqlalchemy.orm import query
from app.BookAccounts import main
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required


@main.route('/dashboard')
@login_required
def display_dashboard():
    return render_template('home.html')



     
@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
