import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

# instantiate extensions
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app(environment="development"):

    from config import config
    from app.views import (
        main_blueprint,
        auth_blueprint,
        user_blueprint,
        define_blueprint,
        project_manager_blueprint,
        viewer_blueprint,
        wp_manager_blueprint,
        admin_blueprint,
        project_blueprint,
        reason_blueprint,
        wp_milestone_blueprint,
        milestone_blueprint,
        work_package_blueprint,
        location_blueprint,
        plan_blueprint,
        control_blueprint,
    )
    from app.models import (
        User,
        AnonymousUser,
    )

    # Instantiate app.
    app = Flask(__name__)

    # Set app config.
    env = os.environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)

    # Set up extensions.
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints.
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(define_blueprint)
    app.register_blueprint(project_manager_blueprint)
    app.register_blueprint(viewer_blueprint)
    app.register_blueprint(wp_manager_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(project_blueprint)
    app.register_blueprint(reason_blueprint)
    app.register_blueprint(wp_milestone_blueprint)
    app.register_blueprint(milestone_blueprint)
    app.register_blueprint(work_package_blueprint)
    app.register_blueprint(location_blueprint)
    app.register_blueprint(plan_blueprint)
    app.register_blueprint(control_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.anonymous_user = AnonymousUser

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template("error.html", error=exc), exc.code

    return app
