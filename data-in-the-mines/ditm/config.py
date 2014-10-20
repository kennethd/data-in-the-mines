
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
    >>> len(c['data-in-the-mines.examples.mtcars.input_generator'])
    3
    """
    cp = ConfigParser.SafeConfigParser()
    configs = defaultdict(list)
    for f in os.listdir(config_dir):
        file_path = os.path.sep.join([config_dir, f])
        cp.read(file_path)
        source = cp.get(REPORT_SECTION, 'source')
        configs[source].append({
            'title': cp.get(REPORT_SECTION, 'title'),
            'section': cp.get(REPORT_SECTION, 'section'),
            'handler': cp.get(REPORT_SECTION, 'handler'),
        })
    return dict(configs)

