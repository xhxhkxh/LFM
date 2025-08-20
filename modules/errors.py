"""Error handlers and helpers for the app."""
from flask import render_template


def register_error_handlers(app):
    @app.errorhandler(500)
    def e500(e=None):
        return render_template('403.htm'), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        return render_template("error.htm", ec=error), 500
