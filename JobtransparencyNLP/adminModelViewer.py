from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask_login import LoginManager,current_user
from flask import Flask,url_for, redirect, render_template, request, abort

class RegModelView(sqla.ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            for x in current_user.roles:
                if x.rolename == 'Admin':
                    return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('user.login', next=request.url))

class SuperModelView(sqla.ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            for x in current_user.roles:
                if x.rolename == 'SuperUser':
                    return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('user.login', next=request.url))