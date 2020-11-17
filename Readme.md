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

From https://forum.sublimetext.com/t/github-gitlab-bitbucket-integration-commands-menu-items/53893

    git config --global alias.open '!f() {
        local type="${1:-branch}"
        local target="${2:-HEAD}"
        local remote="origin"
        
        if [ "$type" = "branch" -o "$type" = "pr" ]; then
            # get full name (i.e. refs/heads/*; refs/remotes/*/*); src: https://stackoverflow.com/a/9753364
            target="$(git rev-parse --symbolic-full-name "$target")"
            
            if [ "$target" != "${target#"refs/remotes/"}" ]; then
                # extract from remote branch reference
                target="${target#"refs/remotes/"}"
            else
                # extract from local branch reference; src: https://stackoverflow.com/a/9753364
                target="$(git for-each-ref --format="%(upstream:short)" "$target")"
            fi
            # split remote/branch
            remote="${target%%/*}"
            target="${target#"$remote/"}"
            
            if [ -z "$remote" ]; then
                echo "Branch ($2) does not point to a remote repository." >&2
                return 2
            fi
        fi
        
        local repo_url="$(git remote get-url "$remote" | sed -E -e "s/(\.(com|org|io))\:/\1\//" -e "s/git@/https:\/\//" -e "s/\.git$//")"
        if [ -z "$repo_url" ]; then
            echo "Cannot open: no remote repository configured under (origin)" >&2
            return 1
        fi
        
        case "$(tr "[:upper:]" "[:lower:]" <<< "$repo_url")" in
            *github*)
                [ "$type" = "commit" ] && repo_url="$repo_url/commit/$(git rev-parse "$target")"
                [ "$type" = "pr"     ] && repo_url="$repo_url/compare/$target?expand=1"
                [ "$type" = "tag"    ] && repo_url="$repo_url/releases/tag/$target"
                [ "$type" = "branch" ] && repo_url="$repo_url/tree/$target"
                ;;
            *bitbucket*)
                [ "$type" = "commit" ] && repo_url="$repo_url/commits/$(git rev-parse "$target")"
                [ "$type" = "pr"     ] && repo_url="$repo_url/pull-requests/new?source=$target"
                [ "$type" = "tag"    ] && repo_url="$repo_url/src/$target"
                [ "$type" = "branch" ] && repo_url="$repo_url/src/$target"
                ;;
            *gitlab*)
                [ "$type" = "commit" ] && repo_url="$repo_url/-/commit/$(git rev-parse "$target")"
                [ "$type" = "pr"     ] && repo_url="$repo_url/-/merge_requests/new?merge_request[source_branch]=$target"
                [ "$type" = "tag"    ] && repo_url="$repo_url/-/tags/$target"
                [ "$type" = "branch" ] && repo_url="$repo_url/-/tree/$target"
                ;;
            *)
                echo "Cannot open: not a GitHub, GitLab, or Bitbucket repository" >&2
                return 1
                ;;
        esac
        
        explorer "$repo_url"
    }; f'
