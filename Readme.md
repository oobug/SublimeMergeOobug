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
