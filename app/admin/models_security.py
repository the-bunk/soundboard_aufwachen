# -*- coding: utf-8 -*-
"""
    app.users.models
    ~~~~~~~~~~~~~~~~~~~~~
    User models
"""
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from app.core import db as db_sec


roles_users = db_sec.Table(
    'roles_users',
    db_sec.Column('user_id', db_sec.Integer(), db_sec.ForeignKey('user.id')),
    db_sec.Column('role_id', db_sec.Integer(), db_sec.ForeignKey('role.id')))


class Role(RoleMixin, db_sec.Model):
    __tablename__ = 'role'

    id = db_sec.Column(db_sec.Integer(), primary_key=True)
    name = db_sec.Column(db_sec.String(80), unique=True)
    description = db_sec.Column(db_sec.String(255))

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return (self.name != other and
                self.name != getattr(other, 'name', None))


class User(UserMixin, db_sec.Model):
    __tablename__ = 'user'

    id = db_sec.Column(db_sec.Integer, primary_key=True)
    email = db_sec.Column(db_sec.String(255), unique=True)
    password = db_sec.Column(db_sec.String(120))
    active = db_sec.Column(db_sec.Boolean())
    confirmed_at = db_sec.Column(db_sec.DateTime())
    last_login_at = db_sec.Column(db_sec.DateTime())
    current_login_at = db_sec.Column(db_sec.DateTime())
    last_login_ip = db_sec.Column(db_sec.String(100))
    current_login_ip = db_sec.Column(db_sec.String(100))
    login_count = db_sec.Column(db_sec.Integer)
    registered_at = db_sec.Column(db_sec.DateTime())
    roles = db_sec.relationship('Role', secondary=roles_users,
                                backref=db_sec.backref('user', lazy='dynamic'))

    def has_role(self, role):
        return role in self.roles


user_datastore = SQLAlchemyUserDatastore(db_sec, User, Role)
