import datetime
import os
from flask import render_template, request, flash, redirect
from flask_security import recoverable
from .models_security import User, Role, user_datastore
from .routes import mod_admin


@mod_admin.route('/users/user/<uid>')
def admin_users_user(uid):
    if not uid:
        flash(gettext("Kein Benutzer angegeben."), 'error')
        return redirect('/')
    user = user_datastore.get_user(uid)
    # user = User.query.filter(User.id==uid).first()
    roles = Role.query.order_by(Role.name).all()
    if not user:
        flash("Keine passender Benutzer gefunden.", 'error')
        return redirect('/admin/users/')
    return render_template('admin/user.html', user=user, roles=roles)

@mod_admin.route('/users/user2role', methods=['POST'])
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


@mod_admin.route('/users/adduser/', methods=['POST'])
def admin_users_adduser():
    data = request.get_json()
    user = user_datastore.create_user(email=data['email'], confirmed_at=datetime.datetime.now(), active=True)
    user_datastore.commit()
    flash("Benutzer wurde angelegt.", "success")
    recoverable.send_reset_password_instructions(user)
    user_datastore.activate_user(user)  # is this needed?
    return "/admin"

@mod_admin.route('/users/remove_user/<iduser>')
def admin_remove_user(iduser):
    user = user_datastore.get_user(iduser)
    user_datastore.delete_user(user)
    user_datastore.commit()
    flash("Benutzer wurde gelöscht.", "success")
    return "/admin"

@mod_admin.route('/users/role/<rolename>')
def admin_users_role(rolename):
    if not rolename:
        flash("Keine Rolle angegeben.", 'error')
        return redirect('/admin/users/')
    role = user_datastore.find_role(rolename)  # Role.query.filter_by(name=name).first()
    users = User.query.filter_by(active=True).order_by(User.email).all()
    if not role:
        flash("Keine passende Rolle gefunden.", 'error')
        return redirect('/admin/users/')
    return render_template('admin/role.html', users=users, role=role)

@mod_admin.route('/users/addrole/', methods=['POST'])
def admin_roles_addrole():
    data = request.get_json()
    user_datastore.create_role(name=data['name'], description=data['description'])
    user_datastore.commit()
    flash("Rolle wurde angelegt.", "success")
    return "/admin"

@mod_admin.route('/users/remove_role/<rolename>')
def admin_remove_role(rolename):
    role = user_datastore.find_role(rolename)
    user_datastore.delete(role)
    user_datastore.commit()
    flash("Rolle wurde gelöscht.", "success")
    return "/admin"
