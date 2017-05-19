from flask import request
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import url_for
from flask import Response
from flask import session
from flask import flash
from flask import abort

from models.user import User
from functools import wraps
from usr_util.utils import *
import json


def current_user():
    uid = int(session.get('uid', -1))
    u = User.get(uid)
    return u


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        if not current_user().is_admin():
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def email_verify_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if not current_user().email_verified():
            flash('邮箱未验证，请先验证邮箱', 'warning')
            return redirect(url_for('user.profile'))
        return f(*args, **kwargs)

    return function
