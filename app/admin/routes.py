# -*- coding: utf-8 -*-
import datetime
from flask import Blueprint, render_template, g
from flask_security import login_required, roles_accepted, current_user
from app.models import Board, Sound
from app import db
from .models_security import User, Role, user_datastore

mod_admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static/admin')


@mod_admin.before_app_first_request
def init_my_blueprint():
    for role in ['artwork', 'upload', 'sounds', 'admin']:
        user_datastore.find_or_create_role(role)

    users = [
        ['the_bunk@gmx.de', '', ['admin']]
    ]
    for u in users:
        if not user_datastore.get_user(u[0]):
            user_datastore.create_user(email=u[0],
                                       confirmed_at=datetime.datetime.now(),
                                       password='')
            db.session.commit()
            for r in u[2]:
                user_datastore.add_role_to_user(u[0], r)
            db.session.commit()

    print('admin done')


@mod_admin.route('/')
@login_required
@roles_accepted('admin')
def admin():
    return render_template('admin/admin.html')


@mod_admin.route('/users')
@login_required
@roles_accepted('admin')
def admin_users():
    return render_template('admin/users.html')


@mod_admin.route('/boards')
@login_required
@roles_accepted('admin')
def admin_boards():
    return render_template('admin/boards.html')


@mod_admin.route('/sounds')
@login_required
@roles_accepted('admin')
def admin_sounds():
    return render_template('admin/sounds.html')
