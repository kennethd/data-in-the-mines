
from collections import defaultdict
import ConfigParser
import itertools
import os

REPORT_SECTION = 'ditm-report'

# Periodic reports are configured via a series of config dirs corresponding to:
PERIODS = ['hourly', 'daily', 'weekly', 'monthly', 'yearly', 'examples']

def configured_cp():
    """sets default values for optional config file sections"""
    return ConfigParser.SafeConfigParser({
        'section': 'my reports',
        'title': 'My Report',
        'template': 'data-in-the-mines-default-report.html',
        'source': '',
        'handler': '',
    })


def read_configs(config_dir):
    """parse directory of config files, return dict

    The dictionary returned is keyed on input_generator, values are lists of
    dictionaries containing all config values for each of that generators
    "listeners" (intended to allow efficiently creating multiple reports from
    the same dataset; say kmeans3 & kmeans4, for example)

    >>> up = lambda x: os.path.dirname(x)
    >>> projroot = up(up(up(os.path.realpath(__file__))))
    >>> confroot = os.path.sep.join([projroot, 'etc', 'data-in-the-mines', 'examples.d'])
    >>> c = read_configs(confroot)
    >>> # example.d configs reference 2 sources for 4 reports
    >>> len(c)
    2
    >>> # 3 reports are configured to receive input from mtcars.input_generator
    >>> ig = 'data-in-the-mines.examples.mtcars.input_generator'
    >>> len(c[ig])
    3
    >>> report_ids = sorted([ conf['report_id'] for conf in c[ig] ])
    >>> report_ids
    ['mtcars_kmeans3', 'mtcars_kmeans4', 'mtcars_stats']
    >>> # get names of all reports across all periods
    >>> global_confs = [ confs for (src, confs) in c.items() ]
    >>> global_confs = [ i for i in itertools.chain.from_iterable(global_confs) ]
    >>> report_ids = sorted([ conf['report_id'] for conf in global_confs ])
    >>> report_ids
    ['mtcars_kmeans3', 'mtcars_kmeans4', 'mtcars_stats', 'visual_playlists']
    """
    configs = defaultdict(list)
    config_dir = os.path.realpath(os.path.expanduser(config_dir))
    for f in os.listdir(config_dir):
        cp = configured_cp()
        if f[-5:] == ".conf":
            report_id = f[:-5]
            file_path = os.path.sep.join([config_dir, f])
            cp.read(file_path)
            source = cp.get(REPORT_SECTION, 'source')
            configs[source].append({
                'title': cp.get(REPORT_SECTION, 'title'),
                'section': cp.get(REPORT_SECTION, 'section'),
                'handler': cp.get(REPORT_SECTION, 'handler'),
                'report_id': report_id,
                'template': cp.get(REPORT_SECTION, 'template'),
            })
    return dict(configs)


def sections_from_configs(config_root):
    """parse all configs and return all sections defined

    >>> up = lambda x: os.path.dirname(x)
    >>> projroot = up(up(up(os.path.realpath(__file__))))
    >>> confroot = os.path.sep.join([projroot, 'etc', 'data-in-the-mines'])
    >>> s = sections_from_configs(confroot)
    >>> s
    ['segments', 'stats', 'visuals']
    """
    cp = configured_cp()
    sections = set()
    config_root = os.path.realpath(os.path.expanduser(config_root))
    for p in PERIODS:
        config_dir = os.path.sep.join([config_root, '{}.d'.format(p)])
        for f in os.listdir(config_dir):
            if f[-5:] == ".conf":
                file_path = os.path.sep.join([config_dir, f])
                cp.read(file_path)
                section = cp.get(REPORT_SECTION, 'section')
                if section:
                    sections.add(section)
    return sorted(list(sections))
