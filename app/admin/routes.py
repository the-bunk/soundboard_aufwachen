# -*- coding: utf-8 -*-
import datetime
import os
from flask import Blueprint, render_template, request, current_app, flash, redirect
from flask_security import login_required, roles_accepted
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
        ['the_bunk@gmx.de', 'test1234', ['admin']]
    ]
    for u in users:
        if not user_datastore.get_user(u[0]):
            user_datastore.create_user(email=u[0],
                                       confirmed_at=datetime.datetime.now(),
                                       password=u[1])
            db.session.commit()
            for r in u[2]:
                user_datastore.add_role_to_user(u[0], r)
            db.session.commit()

    print('admin done')

@mod_admin.before_request
@login_required
@roles_accepted('admin')
def mod_admin_before_request():
    pass

@mod_admin.route('/')
@mod_admin.route('/users')
def admin():
    roles = Role.query.all()
    users = User.query.all()
    return render_template('admin/admin.html', users=users, roles=roles, selected='users')


@mod_admin.route('/boards')
def admin_boards():
    sounds = Sound.query.filter_by(enabled=True).all()
    boards = Board.query.all()
    return render_template('admin/boards.html', sounds=sounds, boards=boards, selected='boards')


@mod_admin.route('/sounds')
def admin_sounds():
    boards = Board.query.all()
    sounds = Sound.query.all()
    return render_template('admin/sounds.html', sounds=sounds, boards=boards, selected='sounds')


### SOUNDS
@mod_admin.route('/sound/submit', methods=["POST"])
def sound_submit():
    name = remove_html(request.form['name'])
    description = remove_html(request.form['description'])
    if 'soundfile' in request.files.to_dict():
        soundfile = request.files['soundfile']
    else:
        soundfile = None
    boards = request.form['boards']
    sound_id = request.form['sound_id']


    if sound_id == -1:
        # neuen sound erstellen
        if not name:
            flash('Kein Name.', 'danger')
            return redirect("/admin/sounds")
        sound = Sound.query.filter_by(name=name).first()
        if sound:
            flash('Dieser Name existiert bereits.', 'danger')
            return redirect("/admin/sounds")
        # save file
        filename = secure_filename(soundfile.filename)
        db_filename = "sounds/" + filename
        filename = os.path.join(current_app.config['SOUNDS_DIR'], filename)
        soundfile.save(filename)
        # add to database
        new_sound = Sound(name=name, description=description, soundfile=db_filename, enabled=True)
        db.session.add(new_sound)
        db.session.commit()
        for b in boards:
            board = Board.query.filter_by(id=b).first()
            if board:
                new_sound.boards.append(board)

        flash('Soundfile übertragen, dankeschön.', 'success')
        return "0"

    else:
        # sound bearbeiten
        sound = Sound.query.filter_by(id=sound_id).first()
        if not sound:
            flash('Ein Fehler ist aufgetreten.', 'danger')
            return redirect("/admin/sounds")
        # save file
        if soundfile:
            filename = secure_filename(soundfile.filename)
            db_filename = "sounds/" + filename
            filename = os.path.join(current_app.config['SOUNDS_DIR'], filename)
            soundfile.save(filename)
        # add to database
        if name:
            sound.name = name
            db.session.commit()
        if description:
            sound.description = description
            db.session.commit()

        for b in sound.boards:
            if not str(b.id) in boards:
                board = Board.query.filter_by(id=b.id).first()
                sound.boards.remove(board)
                db.session.commit()
        for b_id in boards:
            board = Board.query.filter_by(id=b_id).first()
            if not board in sound.boards:
                sound.boards.append(board)
                db.session.commit()
        flash('Soundfile bearbeitet.', 'success')
        return "0"


@mod_admin.route('/sounds/enabled', methods=["GET", "POST"])
def sound_enable():
    data = request.get_json()
    sound_id = data["sound_id"]

    sound = Sound.query.filter_by(id=sound_id).first()
    sound.enabled = not sound.enabled
    db.session.commit()

    return str(sound.enabled)


@mod_admin.route('/sounds/edit/<sound_id>')
def sound_edit(sound_id):
    sound = Sound.query.filter_by(id=sound_id).first()
    boards = Board.query.all()
    sounds = Sound.query.all()
    return render_template('admin/sounds.html', sounds=sounds, boards=boards, sound=sound, selected='sounds')


@mod_admin.route('/sound/delete/<sound_id>')
def sound_delete(sound_id):
    sound = Sound.query.filter_by(id=sound_id).first()

    #datei löschen
    filename = os.path.join(current_app.config['MAIN_STATIC_DIR'], sound.soundfile)
    # filename = os.path.join(current_app.config['SOUNDS_DIR'], sound.soundfile)
    if os.path.exists(filename):
        os.remove(filename)

    #datenbankeintrag löschen
    db.session.delete(sound)
    db.session.commit()

    flash('Sound gelöscht.', 'success')


### BOARDS
@mod_admin.route('/board/submit', methods=["POST"])
def board_submit():
    data = request.get_json()
    name = data["name"]
    sounds = data["sounds"]
    board_id = data["board_id"]

    if board_id == -1:
        # neues board erstellen
        if not name:
            flash('Kein Name.', 'danger')
            return redirect("/admin/boards")

        board = Board.query.filter_by(name=name).first()
        if board:
            flash('Dieser Name existiert bereits.', 'danger')
            return redirect("/admin/boards")

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
    else:
        # board bearbeiten
        board = Board.query.filter_by(id=board_id).first()
        if name:
            board.name = name
            db.session.commit()
        for s in board.sounds:
            if not s.id in sounds:
                sound = Sound.query.filter_by(id=s.id).first()
                board.sounds.remove(sound)
                db.session.commit()
        for s_id in sounds:
            sound = Sound.query.filter_by(id=s_id).first()
            if not sound in board.sounds:
                board.sounds.append(sound)
                db.session.commit()
        flash('Board bearbeitet.', 'success')

    return "/admin/boards"
    return "/admin/sounds"


@mod_admin.route('/boards/edit/<board_id>')
def board_edit(board_id):
    board = Board.query.filter_by(id=board_id).first()
    sounds = Sound.query.filter_by(enabled=True).all()
    boards = Board.query.all()
    return render_template('admin/boards.html', sounds=sounds, boards=boards, board=board, selected='boards')


@mod_admin.route('/board/delete/<board_id>')
def board_delete(board_id):
    board = Board.query.filter_by(id=board_id).first()

    if board:
        db.session.delete(board)
        db.session.commit()
        flash('Board gelöscht.', 'success')
    else:
        flash('Es ist ein Fehler aufgetreten.', 'danger')

    return "/admin/boards"


### USERS
from .routes_users import *
