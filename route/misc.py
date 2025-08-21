from flask import Blueprint, render_template

bp = Blueprint('misc', __name__)


@bp.route('/md-playground')
def md_playground():
    return render_template('md.html')
