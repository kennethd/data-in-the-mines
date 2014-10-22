
from collections import defaultdict
import ConfigParser
import os

REPORT_SECTION = 'ditm-report'

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
    >>> len(c)
    1
    >>> ig = 'data-in-the-mines.examples.mtcars.input_generator'
    >>> len(c[ig])
    3
    >>> report_ids = sorted([ conf['report_id'] for conf in c[ig] ])
    >>> report_ids
    ['mtcars_kmeans3', 'mtcars_kmeans4', 'mtcars_stats']
    """
    cp = ConfigParser.SafeConfigParser()
    configs = defaultdict(list)
    for f in os.listdir(config_dir):
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

