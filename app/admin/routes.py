# -*- coding: utf-8 -*-
import datetime
import os
from flask import Blueprint, render_template, request, current_app, flash
from flask_security import login_required, roles_accepted, current_user
from werkzeug.utils import secure_filename
from app import db
from app.core import remove_html
from app.models import Board, Sound
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
                                       password='test1234')
            db.session.commit()
            for r in u[2]:
                user_datastore.add_role_to_user(u[0], r)
            db.session.commit()

    print('admin done')


@mod_admin.route('/')
@login_required
@roles_accepted('admin')
def admin():
    roles = Role.query.all()
    users = User.query.all()
    return render_template('admin/admin.html', users=users, roles=roles)


@mod_admin.route('/users')
@login_required
@roles_accepted('admin')
def admin_users():
    return render_template('admin/users.html')


@mod_admin.route('/boards')
@login_required
@roles_accepted('admin')
def admin_boards():
    sounds = Sound.query.all()
    boards = Board.query.all()
    return render_template('admin/boards.html', sounds=sounds, boards=boards)


@mod_admin.route('/sounds')
@login_required
@roles_accepted('admin')
def admin_sounds():
    sounds = Sound.query.all()
    return render_template('admin/sounds.html', sounds=sounds)


@mod_admin.route('/sound/submit', methods=["POST"])
def sound_submit():
    name = remove_html(request.form['name'])
    description = remove_html(request.form['description'])
    soundfile = request.files['soundfile']

    if Sound.query.filter_by(name=name).first():
        flash('Dieser Name existiert bereits.', 'danger')
        return "1"

    # save file
    filename = secure_filename(soundfile.filename)
    db_filename = "sounds/" + filename
    filename = os.path.join(current_app.config['SOUNDS_DIR'], filename)
    soundfile.save(filename)

    # add to database
    new_sound = Sound(name=name, description=description, soundfile=db_filename, enabled=True)
    db.session.add(new_sound)
    db.session.commit()

    flash('Soundfile übertragen, dankeschön.', 'success')
    return "0"


@mod_admin.route('/board/submit', methods=["POST"])
def board_submit():
    name = remove_html(request.form['name'])
    sounds = "1, 2,3 "  #TODO

    if Board.query.filter_by(name=name).first():
        flash('Dieser Name existiert bereits.', 'danger')
        return "1"

    # add to database
    new_board = Board(name=name)
    db.session.add(new_board)
    db.session.commit()
    for s in sounds:
        sound = Sound.query.filter_by(id=s).first()
        if sound:
            new_board.sounds.append(sound)
            db.session.commit()

    flash('Board erstellt.', 'success')
    return "0"
