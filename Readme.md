# SublimeMergeOobug

A repository to contain my settings, snippets, and extensions for Sublime Merge.

## Git Config settings

### Set line endings
    [alias]
        set-line-endings = "!f() { py \"${APPDATA}/Sublime Merge/Packages/SublimeMergeOobug/set-line-endings.py\" $1 $2; }; f"

### TortoiseGit diff tools

From https://github.com/TortoiseGit/TortoiseGit/tree/master/contrib/diff-scripts

    [difftool "diff-doc"]
        cmd="wscript.exe \"c:\\Toolbox\\Git\\diff-scripts\\diff-doc.js\" \"$LOCAL\" \"$REMOTE\""

### GitHub/GitLab/Bitbucket Integration

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
