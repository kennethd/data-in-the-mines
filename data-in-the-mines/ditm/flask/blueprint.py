
import os

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

bp_dir = os.path.dirname(os.path.realpath(__file__))
tmpl_dir = os.path.sep.join([bp_dir, 'templates'])

ditm = Blueprint('data-in-the-mines', template_folder=tmpl_dir)

@ditm.route('/', defaults={'section': 'index', 'report_id': None})
@ditm.route('/<section>/<report_id>')
def show(page, report_id):
    try:
        render_template('report.html', report_id=report_id)
    except TemplateNotFound:
        abort(404)

