"""open_url: Open a URL in the system default web browser

Uses os.system instead of the webbrowser module to work around Sublime
Merge limitation
"""

import os
import sys

url = sys.argv[1]

os.system('explorer "{}"'.format(url))
