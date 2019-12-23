"""Set the line endings of a specified file.

Arguments:
    path-to-file, line-ending-type

To Use, add the following to your .gitconfig, updating "path/to"
appropriately:

[alias]
    set-line-endings = "!f() { /c/Python27/python.exe /c/path/to/set-line-endings.py $1 $2; }; f"
"""

import sys

# replacement strings
UNIX_NEWLINE = '\n'
WINDOWS_NEWLINE = '\r\n'
MAC_NEWLINE = '\r'

# relative or absolute file path, e.g.:
file_path = sys.argv[1]

with open(file_path, 'rb') as open_file:
    content = open_file.read()

if sys.argv[2] == 'windows':
    content = content.replace(UNIX_NEWLINE, WINDOWS_NEWLINE)
else:
    content = content.replace(
        WINDOWS_NEWLINE, UNIX_NEWLINE
    ).replace(
        MAC_NEWLINE, UNIX_NEWLINE
    )

with open(file_path, 'wb') as open_file:
    open_file.write(content)
