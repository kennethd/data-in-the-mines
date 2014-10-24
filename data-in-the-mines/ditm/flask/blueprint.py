
import os
import sys

from flask import Blueprint, abort, current_app, redirect, render_template, \
    send_from_directory
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename

from ditm import reports
from ditm.config import PERIODS, read_configs, sections_from_configs

bp_dir = os.path.dirname(os.path.realpath(__file__))
tmpl_dir = os.path.sep.join([bp_dir, 'templates'])
ditm = Blueprint('data-in-the-mines', __name__, template_folder=tmpl_dir,
    static_folder='static')

@ditm.route('/')
@ditm.route('/<section>')
@ditm.route('/<section>/<period>')
@ditm.route('/<section>/<period>/<report_id>')
@ditm.route('/<section>/<period>/<report_id>/<report_date>')
@ditm.route('/<section>/<period>/<report_id>/<report_date>/resources/<filename>')
def show(section='index', period='examples', report_id='', report_date='', filename=''):

    if period not in PERIODS:
        current_app.logger.error('bad period: {}'.format(period))
        abort(404)

    ditm_path = current_app.config['DITM_URL_PREFIX']

    report_root = current_app.config['DITM_OUTPUT_ROOT']
    report_root = os.path.realpath(os.path.expanduser(report_root))

    config_root = current_app.config['DITM_CONFIG_ROOT']
    config_root = os.path.realpath(os.path.expanduser(config_root))
    config_dir = os.path.sep.join([ config_root, '{}.d'.format(period) ])

    configs = read_configs(config_dir)
    sections = sections_from_configs(config_root)

    # user must select, in order:
    # section [user/config defined]
    # period [daily, weekly, examples, ...] corresponding to .d config dirs
    # report_id -> most recent report is displayed w/menu of past dates
    report_ids = set()
    report_template = ''
    for (src, src_configs) in configs.iteritems():
        for c in src_configs:
            if section == c['section']:
                report_ids.add(c['report_id'])
                if c['report_id'] == report_id:
                    report_template = c.get('template', '')
    report_ids = sorted(list(report_ids))

    if section not in sections + ['index']:
        current_app.logger.error('bad section: {} {}'.format(section, sections))
        abort(404)

    last_date = ''
    report_dates = []
    # having no reports configured for a time period is not an error
    if report_ids:
        if not report_id:
            report_id = report_ids[0]

        if report_id:
            if report_id not in report_ids:
                current_app.logger.error('bad report: {} {}'.format(report_id, report_ids))
                abort(404)
            report_dir = os.path.sep.join([report_root, section, period, report_id])
            report_dates = reports.existing_reports(report_dir)

        try:
            last_date = report_dates[-1]
        except IndexError:
            pass

        if last_date and not report_date:
            report_date = last_date
            # the only condition we have a report_id but no report_date is when
            # user has just selected a report_id; send them to most recent
            if report_id:
                report_path = "/".join([
                    ditm_path,
                    section,
                    period,
                    report_id,
                    report_date
                ]).rstrip("/")
                current_app.logger.info('redirecting to {}'.format(report_path))
                return redirect(report_path)

        # if we have a filename, request is for page resource
        if filename:
            filename = secure_filename(filename)
            resource_dir = os.path.sep.join([
                report_root,
                section,
                period,
                report_id,
                report_date,
            ])
            current_app.logger.info('serving {}/{}'.format(resource_dir, filename))
            return send_from_directory(resource_dir, filename)

    if not report_id:
        report_template = 'data-in-the-mines-nothing-there.html'

    # else returning page itself
    tmpl_kwargs = {
        'ditm_path': ditm_path,
        'section': section,
        'period': period,
        'report_id': report_id,
        'report_date': report_date,
        'sections': sections,
        'periods': PERIODS,
        'report_ids': report_ids,
        'report_dates': report_dates,
        'report_template': report_template
    }

    try:
        return render_template('data-in-the-mines.html', **tmpl_kwargs)
    except TemplateNotFound:
        current_app.logger.error('data-in-the-mines.html not found')
        abort(404)
