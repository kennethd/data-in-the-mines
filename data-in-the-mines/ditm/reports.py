
import os

def mk_reports_dir(report_dir):
    """create directory structure for a new report"""
    # approximation of `mkdir -p`
    # https://mail.python.org/pipermail/python-dev/2010-July/102092.html
    try:
        os.makedirs(report_dir)
    except OSError, e:
        if e.errno == 17:
            mk_reports_dir(report_dir.rsplit(os.path.sep, 1)[0])

def existing_reports(report_dir):
    """read reports dir and return list of reports avail there (a list of dates)

    The heirarchy of the reports directory is:

    {app.config['DITM_OUTPUT_DIR']}
        /{section}
            /{report_id}
                /YYYY-MM-DD
                    ...stuff...
    """
    try:
        return os.listdir(report_dir)
    except OSError:
        mk_reports_dir(report_dir)
    return []

