# SublimeMergeOobug

A repository to contain my settings, snippets, and extensions for Sublime Merge.

## Prerequisites

Using the functionality from this repository requires that the following items be installed:

- Sublime Merge (obviously)
- Git (not just the version bundled with Sublime Merge)
    - Sublime Merge preferences should be set to use the system Git binary
- Python (with the `py` launcher and `pip` module installed)

## Git Config settings

These example Git config settings include paths that make assumptions about the operating system (Windows) and about where your Sublime Merge settings files are stored (%APPDATA%/Sublime Merge) and will need to be tweaked if these assumptions are incorrect.

### Set line endings
    git config --global alias.set-line-endings '!f() {
        py "${APPDATA}/Sublime Merge/Packages/SublimeMergeOobug/set-line-endings.py" $1 $2;
    }; f'

### TortoiseGit diff tools

From https://github.com/TortoiseGit/TortoiseGit/tree/master/contrib/diff-scripts

A menu item has been added to the File menu to allow diffing a Word document with its previous version. This functionality relies on the contents of the diff-scripts repository being placed in the folder C:\Toolbox\Git\diff-scripts

    [difftool "diff-doc"]
        cmd="wscript.exe \"c:\\Toolbox\\Git\\diff-scripts\\diff-doc.js\" \"$LOCAL\" \"$REMOTE\""

### GitHub/GitLab/Bitbucket/Azure DevOps Integration

Inspired by https://forum.sublimetext.com/t/github-gitlab-bitbucket-integration-commands-menu-items/53893

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
