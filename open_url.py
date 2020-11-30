"""open_url: Open a URL in the system default web browser

Uses os.system instead of the webbrowser module to work around a
limitation in Sublime Merge.
"""

import os
import re
import sys

url = sys.argv[1]

# Validate URL
urlRegex = re.compile(
    # http:// or https://
    r"^https?://"
    # domain...
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
    # localhost...
    r"localhost|"
    # ...or ip
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    # optional port
    r"(?::\d+)?"
    # end of URL
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)

if urlRegex.match(url):
    os.system('explorer "{}"'.format(url))
