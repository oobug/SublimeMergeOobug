r"""GitHub/GitLab/Bitbucket integration

To use, run the following:
    git config --global alias.open '!f() { py \"${APPDATA}/Sublime Merge/Packages/SublimeMergeOobug/set-line-endings.py\" "${1:-branch}" "${2:-HEAD}" }; f'

Inspired by:
https://forum.sublimetext.com/t/github-gitlab-bitbucket-integration-commands-menu-items/53893
"""

import sys

action = sys.argv[1]
target = sys.argv[2]
remote = "origin"

if action in ("branch", "pr"):
    # Get full name (i.e. refs/heads/*; refs/remotes/*/*);
    # src: https://stackoverflow.com/a/9753364
    pass
