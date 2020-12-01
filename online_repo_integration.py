r"""GitHub/GitLab/Bitbucket integration

To use, run the following:
git config --global alias.open '!f() {
    local action="${1:-branch}"
    local target="${2:-HEAD}"
    local output="$(py "${APPDATA}/Sublime Merge/Packages/SublimeMergeOobug/online_repo_integration.py" "$action" "$target")"

    if [ "$output" != "${output#"1: "}" ]; then
        echo "${output#"1: "}"
        return 1
    elif [ "$output" != "${output#"2: "}" ]; then
        echo "${output#"2: "}"
        return 2
    fi
}; f'

Inspired by:
https://forum.sublimetext.com/t/github-gitlab-bitbucket-integration-commands-menu-items/53893
"""

import os
import re
import sys

try:
    from git import Repo
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gitpython"])
    from git import Repo

# Import local OpenUrl function
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from open_url import OpenUrl


def OpenOnlineRepository(action="branch", target="HEAD"):
    """Open the online repository URL for the action and target"""
    git = Repo(os.getcwd()).git
    remote = "origin"

    if action in ("branch", "pr"):
        initialTarget = target

        # Get full name (i.e. refs/heads/*; refs/remotes/*/*);
        # src: https://stackoverflow.com/a/9753364
        target = git.rev_parse(target, symbolic_full_name=True)

        if target.startswith("refs/remotes/"):
            # Extract from remote branch reference
            target = target[13:]
        else:
            # Extract from local branch reference
            # src: https://stackoverflow.com/a/9753364
            target = git.for_each_ref(target, format="%(upstream:short)")

        # split remote/branch
        try:
            remote, target = target.split("/", maxsplit=1)
        except ValueError:
            return "2: Branch ({}) does not point to a remote repository.".format(
                initialTarget
            )

    repoUrl = git.remote("get-url", remote) or ""
    repoUrl = re.sub(r"git@(ssh\.)?", r"https://", repoUrl)
    repoUrl = re.sub(r"(https://)[^/]+@", r"\1", repoUrl)
    repoUrl = re.sub(r"(\.(com|org|io|ca))\:v\d", r"\1", repoUrl)
    repoUrl = re.sub(r"(\.(com|org|io|ca))\:", r"\1/", repoUrl)
    repoUrl = re.sub(r"\.git$", r"", repoUrl)

    if not repoUrl:
        return "1: Cannot open: no remote repository configured under ({})".format(
            remote
        )

    lowerRepoUrl = repoUrl.lower()

    if action == "commit":
        commitTarget = git.rev_parse(target)

    if "github" in lowerRepoUrl:
        if action == "commit":
            repoUrl += "/commit/{}".format(commitTarget)
        elif action == "pr":
            repoUrl += "/compare/{}?expand=1".format(target)
        elif action == "tag":
            repoUrl += "/releases/tag/{}".format(target)
        elif action == "branch":
            repoUrl += "/tree/{}".format(target)
    elif "bitbucket" in lowerRepoUrl:
        if action == "commit":
            repoUrl += "/commits/{}".format(commitTarget)
        elif action == "pr":
            repoUrl += "/pull-requests/new?source={}".format(target)
        elif action == "tag":
            repoUrl += "/src/{}".format(target)
        elif action == "branch":
            repoUrl += "/src/{}".format(target)
    elif "gitlab" in lowerRepoUrl:
        if action == "commit":
            repoUrl += "/-/commit/{}".format(commitTarget)
        elif action == "pr":
            repoUrl += "/-/merge_requests/new?merge_request[source_branch]={}".format(
                target
            )
        elif action == "tag":
            repoUrl += "/-/tags/{}".format(target)
        elif action == "branch":
            repoUrl += "/-/tree/{}".format(target)
    elif "azure" in lowerRepoUrl or "tfs" in lowerRepoUrl:
        if "_git" not in lowerRepoUrl:
            repoUrl = re.sub(r"(/[^/]+)$", r"/_git\1", repoUrl)

        if action == "commit":
            repoUrl += "/commit/{}".format(commitTarget)
        elif action == "pr":
            repoUrl += "/pullrequestcreate?sourceRef={}".format(target)
        elif action == "tag":
            repoUrl += "?version=GT{}".format(target)
        elif action == "branch":
            repoUrl += "?version=GB{}".format(target)
    else:
        return "1: Cannot open: not a GitHub, GitLab, or Bitbucket repository"

    OpenUrl(repoUrl)


if __name__ == "__main__":
    action = sys.argv[1]
    target = sys.argv[2]
    print(OpenOnlineRepository(action, target))
