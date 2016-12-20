#!/usr/bin/env python3

import os
import platform
from i3_lemonbar_conf import *

python3_command_map = {'ubuntu': 'python3',
                       'arch': 'python',
                       'default': 'python3'}
try:
    distribution = platform.linux_distribution()[0].lower()
    python_command = python3_command_map[distribution]
except (KeyError, IndexError, TypeError):
    python_command = python3_command_map['default']

cwd = os.path.dirname(os.path.abspath(__file__))
lemon = "lemonbar -p -f '%s' -f '%s' -g '%s' -B '%s' -F '%s'" % (font, iconfont, geometry, color_back, color_fore)
feed = "{python_cmd} -c 'import i3_lemonbar_feeder; i3_lemonbar_feeder.run()'".format(python_cmd=python_command)

check_output('cd %s; %s | %s' % (cwd, feed, lemon), shell=True)
