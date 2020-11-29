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

### GitHub/GitLab/Bitbucket/Azure DevOps Integration

Originally from https://forum.sublimetext.com/t/github-gitlab-bitbucket-integration-commands-menu-items/53893

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
        
        local repo_url="$(git remote get-url "origin" | sed -E -e "s/git@(ssh\.)?/https:\/\//" -e "s/(https:\/\/)[^\/]+@/\1/" -e "s/(\.(com|org|io|ca))\:v[0-9]/\1/" -e "s/(\.(com|org|io|ca))\:/\1\//" -e "s/\.git$//")"
        
        if [ -z "$repo_url" ]; then
            echo "Cannot open: no remote repository configured under ($remote)" >&2
            return 1
        fi
        
        local lower_url="$(tr "[:upper:]" "[:lower:]" <<< "$repo_url")"
        
        if [[ "$lower_url" == *"azure"* || "$lower_url" == *"tfs"* ]]
        then
            if [[ "$lower_url" != *"_git"* ]]
            then
                repo_url="$(echo "$repo_url" | sed -E -e "s/(\/[^\/]+)$/\/_git\1/")"
            fi
            
            [ "$type" = "commit" ] && repo_url="$repo_url/commit/$(git rev-parse "$target")"
            [ "$type" = "pr"     ] && repo_url="$repo_url/pullrequestcreate?sourceRef=$target"
            [ "$type" = "tag"    ] && repo_url="$repo_url?version=GT$target"
            [ "$type" = "branch" ] && repo_url="$repo_url?version=GB$target"
        fi
        
        case "$lower_url" in
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
            *azure*)
                ;;
            *tfs*)
                ;;
            *)
                echo "Cannot open: not a GitHub, GitLab, Bitbucket, or Azure DevOps repository" >&2
                return 1
                ;;
        esac
        
        py "${APPDATA}/Sublime Merge/Packages/SublimeMergeOobug/open_url.py" "$repo_url";
    }; f'
