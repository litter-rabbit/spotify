from flask import Flask, render_template, request,flash,url_for,redirect
from spotify.extendtions import db, login_manager, whooshee, csrf, migrate, bootstrap, moment
from spotify.blueprints.main import main_bp
from spotify.blueprints.auth import auth_bp
from spotify.blueprints.ajax import ajax_bp
from spotify.settings import config, basedir
from spotify.models import Link

import click
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from spotify.models import Admin

from spotify.extendtions import db
from spotify.models import Order
import os





def register_extendtions(app):
    db.init_app(app)
    app.app_context().push()
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    whooshee.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    register_logging(app)



def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ajax_bp, url_prefix='/ajax')


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/tt.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)


def register_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def initadmin():
        """Initialize the admin."""
        admin = Admin(username='admin', passwrod='admin')
        db.session.add(admin)
        db.session.commit()
        click.echo('Initialized admin.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def addadmin(username, password):
        click.echo('Creating the temporary administrator account...')
        admin=Admin(username=username,passwrod=password)
        db.session.add(admin)
        db.session.commit()


def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


configname = os.getenv('FLASK_CONFIG', 'development')
app = Flask('spotify')
app.config.from_object(config[configname])
register_extendtions(app)
register_blueprints(app)
register_command(app)
register_errorhandlers(app)

