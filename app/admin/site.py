# -*- coding: utf-8 -*-
import datetime
from flask import Blueprint, render_template, request, flash, current_app, redirect, session
from flask_babelex import gettext
from flask_security import login_required, roles_accepted, recoverable, current_user
from myapp.models_security import User, Role, user_datastore
from myapp.core import db as db_kochbuch  # as ist legacy WEGMACHEN

mod = Blueprint('site', __name__)
# from site import mod
#mod = Blueprint('site', __name__)


@mod.errorhandler(404)
def page_not_found(error):
    return render_template('site/page_not_found.html'), 404


@mod.before_app_first_request
def init_my_blueprint():
    print('site start')

    for role in ['kochbuch', 'pola', 'alex', 'admin']:
        user_datastore.find_or_create_role(role)

    users = [
        ['admin0@hebener.eu', 'test1234', ['kochbuch', 'pola']],
        ['admin3@hebener.eu', 'test1234', ['kochbuch', 'pola', 'alex']],
        ['admin4@hebener.eu', 'test1234', ['kochbuch', 'admin']]
    ]
    for u in users:
        if not user_datastore.get_user(u[0]):
            user_datastore.create_user(email=u[0],
                                       confirmed_at=datetime.datetime.now(),
                                       password='test1234')
            db_kochbuch.session.commit()
            userrole = user_datastore.find_or_create_role(u[0])
            user_datastore.add_role_to_user(u[0], userrole.name)
            for r in u[2]:
                user_datastore.add_role_to_user(u[0], r)
            db_kochbuch.session.commit()

    role = Role.query.filter_by(name="admin").first()
    user = User.query.first()
    print("ROLES:")
    for r in user.roles:
        print(r.name)
    if role in user.roles:
        print("user has role")
    else:
        print("user has role NOT")
    print(type(current_user.roles))
    users = User.query.filter(User.roles.any(Role.name.in_(["alex", "admin"]))).all()
    # users = User.query.filter(User.roles.any(Role.name.in_(current_user.roles()))).all()
    for u in users:
        print(u.email)
        for r in u.roles:
            print(r.name)

    print('site done')


@mod.route('/einkauf/')
def einkauf():
    return 'einkauf'


@mod.route('/profil')
@login_required
def profil():
    return 'profil'


@mod.route('/')
def home():

    return render_template('index.html')


# Sprache ändern
@mod.route('/language/<lang>', methods=['GET', 'POST'])
def set_language(lang):
    data = request.get_json()
    page = data["page"]
    if lang in current_app.config['LANGUAGES']:
        session['lang'] = lang
        flash(gettext('Sprache geändert.'), 'success')
    else:
        flash(gettext('Sprache nicht gefunden.'), 'warning')
    return page


@mod.route('/admin/')
@mod.route('/admin/settings/')
@login_required
@roles_accepted("admin", "users")
def admin():
    return render_template('site/admin.html', adminMenuSelected="settings")


@mod.route('/admin/users/')
def admin_users(noExtendBase=False):
    users = User.query.order_by(User.email).all()
    roles = Role.query.order_by(Role.name).all()
    return render_template('site/admin.html', noExtendBase=noExtendBase, adminMenuSelected="users", users=users, roles=roles)


@mod.route('/admin/users/user/<uid>')
def admin_users_user(uid):
    if not uid:
        flash("Kein Benutzer angegeben.", 'error')
        return redirect(str(current_app.config["SUBDIR"]) + '/site/admin/users/')
    user = user_datastore.get_user(uid)
    # user = User.query.filter(User.id==uid).first()
    roles = Role.query.order_by(Role.name).all()
    if not user:
        flash("Keine passender Benutzer gefunden.", 'error')
        return redirect(str(current_app.config["SUBDIR"]) + '/site/admin/users/')
    return render_template('site/admin/user.html', user=user, roles=roles)


@mod.route('/admin/users/adduser/', methods=['POST'])
def admin_users_adduser():
    data = request.get_json()
    user = user_datastore.create_user(email=data['email'], confirmed_at=datetime.datetime.now(), active=True)
    user_datastore.commit()
    flash("Benutzer wurde angelegt.", "success")
    recoverable.send_reset_password_instructions(user)
    user_datastore.activate_user(user)  # is this needed?
    return admin_users(True)


@mod.route('/admin/users/addrole/', methods=['POST'])
def admin_roles_addrole():
    data = request.get_json()
    user_datastore.create_role(name=data['name'], description=data['description'])
    user_datastore.commit()
    flash("Rolle wurde angelegt.", "success")
    return admin_users(True)


@mod.route('/admin/users/role/<rolename>')
def admin_users_role(rolename):
    if not rolename:
        flash("Keine Rolle angegeben.", 'error')
        return redirect(str(current_app.config["SUBDIR"]) + '/site/admin/users/')
    role = user_datastore.find_role(rolename)  # Role.query.filter_by(name=name).first()
    users = User.query.filter_by(active=True).order_by(User.email).all()
    if not role:
        flash("Keine passende Rolle gefunden.", 'error')
        return redirect(str(current_app.config["SUBDIR"]) + '/site/admin/users/')
    return render_template('site/admin/role.html', users=users, role=role)


@mod.route('/admin/users/user2role', methods=['POST'])
def admin_users_user2role():
    data = request.get_json()
    user = user_datastore.get_user(data['user'])
    role = user_datastore.find_role(data['role'])
    if data['val'] == '1':
        user_datastore.add_role_to_user(user.email, role)
        user_datastore.commit()
        return "button is-success spaced"
    else:
        user_datastore.remove_role_from_user(user.email, role)
        user_datastore.commit()
        return "button is-danger spaced"


@mod.route('/admin/users/remove_role/<rolename>')
def admin_remove_role(rolename):
    role = user_datastore.find_role(rolename)
    user_datastore.delete(role)
    user_datastore.commit()
    flash("Rolle wurde gelöscht.", "success")
    return redirect(str(current_app.config["SUBDIR"]) + '/admin/users')


@mod.route('/admin/users/remove_user/<iduser>')
def admin_remove_user(iduser):
    user = user_datastore.get_user(iduser)
    user_datastore.delete_user(user)
    user_datastore.commit()
    flash("Benutzer wurde gelöscht.", "success")
    return redirect(str(current_app.config["SUBDIR"]) + "/admin/users")


@mod.route('/admin/users/deactivate/<iduser>')
def admin_deactivate_user(iduser):
    user = user_datastore.get_user(iduser)
    user_datastore.toggle_active(user)
    user_datastore.commit()
    flash("Benutzer wurde deaktiviert.", "success")
    return str(user.is_active)


@mod.route('/username_is_available/<email>')
def username_is_available(email):
    user = user_datastore.get_user(email)
    if user:
        return "0"
    else:
        return "1"
