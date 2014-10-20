
import os

from flask import Blueprint, abort, current_app, render_template
from jinja2 import TemplateNotFound

from ditm.config import read_configs

bp_dir = os.path.dirname(os.path.realpath(__file__))
tmpl_dir = os.path.sep.join([bp_dir, 'templates'])
ditm = Blueprint('data-in-the-mines', __name__, template_folder=tmpl_dir)

@ditm.route('/')
@ditm.route('/<section>')
@ditm.route('/<section>/<period>')
@ditm.route('/<section>/<period>/<report_id>')
def show(section='index', period='examples', report_id=None):

    if period not in ('daily', 'weekly', 'monthly', 'yearly', 'examples'):
        abort(404)

    config_root = current_app.config['CONFIG_ROOT']
    config_root = os.path.realpath(os.path.expanduser(config_root))
    config_dir = os.path.sep.join([ config_dir, '{}.d'.format(period) ])
    configs = read_configs(config_dir)

    sections = set()
    report_ids = set()
    for c in configs:
        sections.add(c['section'])
        if section == c['section']:
            report_ids.add(c['report_id'])
    sections = list(sections)
    report_ids = list(report_ids)

    if section not in sections + ['index']:
        abort(404)

    tmpl_kwargs = {
        'section': section,
        'period': period,
        'report_id': report_id,
        'sections': sections,
        'report_ids': report_ids,
    }

    try:
        return render_template('report.html', **tmpl_kwargs)
    except TemplateNotFound:
        abort(404)

