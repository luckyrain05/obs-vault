[[git]]
[[git merges]]

- A ==worktree== is an additional working directory linked to the same repository.
- By default, a git repo has one worktree (the main working directory). `git worktree` lets you check out multiple branches simultaneously in separate directories on disk.
- All worktrees share the same `.git` data (commits, branches, stash). A commit made in any worktree is visible from all others.
- A branch cannot be checked out in two worktrees at the same time.

# Creating a Worktree

```bash
git worktree add ../feature-branch feature    # check out 'feature' in ../feature-branch
git worktree add ../hotfix -b hotfix          # create new branch 'hotfix' in ../hotfix
git worktree add ../review abc123             # check out specific commit (detached HEAD)
```

- First argument is the path where the new working directory is created.
- Second argument is an existing branch name, or use `-b` to create a new branch.
- Omitting the branch name creates a new branch matching the directory name.

# Managing Worktrees

```bash
git worktree list              # show all worktrees with their branches and HEAD commits
git worktree remove ../hotfix  # delete a worktree directory (must have no uncommitted changes)
git worktree remove --force ../hotfix  # delete even with uncommitted changes
git worktree prune             # clean up stale references to manually deleted worktree directories
```

- If you delete the worktree directory manually (e.g., `rm -rf ../hotfix`), run `git worktree prune` to clean up git's internal tracking.

# Use Cases

- Review a PR while keeping your current work untouched.
- Run tests on another branch without stashing or committing unfinished work.
- Work on a hotfix while a long build runs on your main worktree.
