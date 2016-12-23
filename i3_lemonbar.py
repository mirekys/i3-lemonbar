#!/usr/bin/env python3

import os
from i3_lemonbar_conf import *


cwd = os.path.dirname(os.path.abspath(__file__))
lemon = "lemonbar -p -f '%s' -f '%s' -g '%s' -B '%s' -F '%s'" % (font, iconfont, geometry, color_back, color_fore)
feed = "python3 -c 'import i3_lemonbar_feeder; i3_lemonbar_feeder.run()'"

check_output('cd %s; %s | %s' % (cwd, feed, lemon), shell=True)
