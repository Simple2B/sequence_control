#!/user/bin/env python
import os
import click

from app import create_app, db, models, forms
from app.models import User, Reason

app = create_app()


def add_admin():
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@admin.com")
    ADMIN_COMPANY = os.environ.get("ADMIN_COMPANY", "umbrella")
    ADMIN_WP_RES = os.environ.get("ADMIN_COMPANY", "test_wp_res")
    User(
        username=ADMIN_USERNAME,
        password=ADMIN_PASSWORD,
        email=ADMIN_EMAIL,
        company=ADMIN_COMPANY,
        wp_responsible=ADMIN_WP_RES,
        role=User.Role.admin,
    ).save()


def add_reasons():
    print("Started!")
    REASONS = os.environ.get("REASONS", "admin").split(", ")
    for reason in REASONS:
        print(reason)
        Reason(name=reason).save()
    print("Done!")


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, m=models, forms=forms)


@app.cli.command()
def create_db():
    """Create the configured database."""
    db.create_all()
    add_admin()


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


@app.cli.command()
def reasons_add():
    """adding reasons from .env"""
    add_reasons()


if __name__ == "__main__":
    app.run()
