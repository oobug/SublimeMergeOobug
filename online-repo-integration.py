r"""GitHub/GitLab/Bitbucket integration

To use, run the following:
git config --global alias.open '!f() {
    py \"${APPDATA}/Sublime Merge/Packages/SublimeMergeOobug/online-repo-integration.py\" "${1:-branch}" "${2:-HEAD}"
}; f'

Inspired by:
https://forum.sublimetext.com/t/github-gitlab-bitbucket-integration-commands-menu-items/53893
"""

import re
import subprocess
import sys
import webbrowser


def ShellCommand(command):
    """Execute a shell command and return the output"""
    value = subprocess.check_output(command)
    return value.decode("utf-8").strip()


action = sys.argv[1]
target = initialTarget = sys.argv[2]
remote = "origin"

if action in ("branch", "pr"):
    # Get full name (i.e. refs/heads/*; refs/remotes/*/*);
    # src: https://stackoverflow.com/a/9753364
    target = ShellCommand(f'git rev-parse --symbolic-full-name "{target}"')

    if target.startswith("refs/remotes"):
        # Extract from remote branch reference
        target = target[12:]
    else:
        # Extract from local branch reference
        # src: https://stackoverflow.com/a/9753364
        target = ShellCommand(
            f'git for-each-ref --format="%(upstream:short)" "{target}"'
        )

    # split remote/branch
    try:
        remote, target = target.split("/", maxsplit=1)
    except ValueError:
        print(f"Branch ({initialTarget}) does not point to a remote repository.")

repoUrl = ShellCommand(f'git remote get-url "{remote}"') or ""
repoUrl = re.sub(r"(\.(com|org|io))\:", r"\1/", repoUrl)
repoUrl = re.sub(r"git@", r"https://", repoUrl)
repoUrl = re.sub(r"\.git", r"", repoUrl)

if not repoUrl:
    print(f"Cannot open: no remote repository configured under ({remote})")

lowerRepoUrl = repoUrl.lower()

if action == "commit":
    commitTarget = ShellCommand(f'git rev-parse "{target}"')

if "github" in lowerRepoUrl:
    if action == "commit":
        repoUrl += f"/commit/{commitTarget}"
    elif action == "pr":
        repoUrl += f"/compare/{target}?expand=1"
    elif action == "tag":
        repoUrl += f"/releases/tag/{target}"
    elif action == "branch":
        repoUrl += f"/tree/{target}"
elif "bitbucket" in lowerRepoUrl:
    if action == "commit":
        repoUrl += f"/commits/{commitTarget}"
    elif action == "pr":
        repoUrl += f"/pull-requests/new?source={target}"
    elif action == "tag":
        repoUrl += f"/src/{target}"
    elif action == "branch":
        repoUrl += f"/src/{target}"
elif "gitlab" in lowerRepoUrl:
    if action == "commit":
        repoUrl += f"/-/commit/{commitTarget}"
    elif action == "pr":
        repoUrl += f"/-/merge_requests/new?merge_request[source_branch]={target}"
    elif action == "tag":
        repoUrl += f"/-/tags/{target}"
    elif action == "branch":
        repoUrl += f"/-/tree/{target}"
else:
    print ("Cannot open: not a GitHub, GitLab, or Bitbucket repository")

webbrowser.open_new_tab(repoUrl)
