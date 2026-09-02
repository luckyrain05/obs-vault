[[git]]

- [[git]] supports several ways to integrate changes from one branch into another.
- All merge operations start from the branch you want to merge ==into==.

# Fast-Forward Merge

- Happens when the target branch has no new commits since the source branched off.
- Git moves the branch pointer forward. No merge commit created.

```
before:
            main
              |
  A --- B --- C --- D --- E
                          |
                        feature

after (git merge feature from main):
                          main
                            |
  A --- B --- C --- D --- E
                          |
                        feature
```

```bash
git switch main
git merge feature        # fast-forward, no merge commit
```

- Use `--no-ff` to force a merge commit even when fast-forward is possible.

# Three-Way Merge

- Happens when both branches have new commits since they diverged.
- Git finds the ==merge base== (common ancestor), compares both branches against it, and creates a ==merge commit== with two parents.

```
before:
              main
                |
  A --- B --- C --- F
                \
                 D --- E
                       |
                     feature

merge base = C

after (git merge feature from main):
                       main
                         |
  A --- B --- C --- F --- G    <-- merge commit, two parents: F and E
                \       /
                 D --- E
                       |
                     feature
```

```bash
git switch main
git merge feature       # creates merge commit G
```

# Merge Conflicts

- A ==merge conflict== occurs when both branches modified the same lines in the same file.
- Git cannot auto-resolve, so it pauses the merge and marks the conflicted files.

```bash
git switch main
git merge feature
# CONFLICT (content): Merge conflict in app.py
# Automatic merge failed; fix conflicts and then commit the result.
```

- `git status` shows conflicted files under "Unmerged paths".

```bash
git status
# Unmerged paths:
#   both modified:   app.py
```

# Conflict Markers

- Git inserts ==conflict markers== into the file to show both versions.

```
<<<<<<< HEAD
code from current branch (main)
=======
code from incoming branch (feature)
>>>>>>> feature
```

- `<<<<<<< HEAD` to `=======` is the current branch's version.
- `=======` to `>>>>>>>` is the incoming branch's version.

# Resolving Conflicts

1. Open the conflicted file in your editor.
2. Find all `<<<<<<<` markers.
3. Decide what the final code should be. Keep one side, both, or write something new.
4. Delete all `<<<<<<<`, `=======`, and `>>>>>>>` marker lines.
5. Stage the resolved file and commit.

```bash
# after editing app.py to resolve:
git add app.py
git commit                  # completes the merge (default message provided)
```

- To abort a merge and return to the state before `git merge`:

```bash
git merge --abort
```

- To see the diff during a conflict:

```bash
git diff                    # shows conflict markers in unstaged files
git diff --ours             # diff between merge result and current branch
git diff --theirs           # diff between merge result and incoming branch
```

# Multi-File Conflicts

- When multiple files conflict, resolve each one individually.

```bash
git status                  # lists all conflicted files
# fix each file...
git add file1.py file2.py   # stage all resolved files
git commit                  # one commit resolves the entire merge
```

# Squash Merge

- ==Squash merge== takes all commits from a branch and combines them into one staged changeset. No merge commit, no branch history preserved.

```bash
git switch main
git merge --squash feature
git commit -m "add feature"
```

- Useful when a feature branch has many small/messy commits and you want one clean commit on main.

# Rebase

- ==Rebase== replays commits from one branch onto another, rewriting history to produce a linear sequence.

```
before:
  A --- B --- C           main
                \
                 D --- E  feature

after (git rebase main from feature):
  A --- B --- C                main
                \
                 D' --- E'     feature
```

- D' and E' are new commits with new hashes. They have the same diffs as D and E but different parents.

```bash
git switch feature
git rebase main          # replay feature commits on top of main
```

- After rebasing, a fast-forward merge from main is possible.

```bash
git switch main
git merge feature        # fast-forward since main is a direct ancestor of feature
```

# Rebase Conflict Resolution

- If conflicts occur during rebase, git pauses at each conflicting commit.

```bash
# git rebase main
# CONFLICT in app.py

# 1. resolve the conflict in your editor
# 2. stage the fix
git add app.py

# 3. continue to the next commit
git rebase --continue

# or cancel the entire rebase
git rebase --abort
```

- Unlike merge conflicts (resolved once), rebase may pause multiple times since it replays commits one by one.
- Rebase rewrites commit hashes. Never rebase commits already pushed to a shared remote unless you coordinate with your team.

# Interactive Rebase

- ==Interactive rebase== lets you edit, reorder, squash, or drop commits before replaying them.

```bash
git rebase -i HEAD~4     # interactively edit the last 4 commits
```

- Opens an editor with a list of commits and actions.

```
pick a1b2c3d add login page
pick d4e5f6a fix typo
pick 7g8h9i0 add logout button
pick j1k2l3m update styles
```

**pick**
- Keep the commit as-is.
**reword**
- Keep the commit but edit its message.
**squash**
- Combine this commit into the one above it. Both messages are merged.
**drop**
- Delete the commit entirely.

- Change `pick` to the desired action, save and close the editor. Git replays the commits with your modifications.

```
pick a1b2c3d add login page
squash d4e5f6a fix typo           # combine with "add login page"
pick 7g8h9i0 add logout button
drop j1k2l3m update styles        # remove this commit
```

# Rebase vs Merge

- Both integrate changes. They differ in how the history looks.

```
merge: preserves branch structure
  A --- B --- C --- F --- G
                \       /
                 D --- E

rebase: linear history
  A --- B --- C --- F --- D' --- E'
```

- Merge is non-destructive. Original commits stay intact.
- Rebase rewrites history. Cleaner log, but dangerous on shared branches.
- Common pattern: rebase your feature branch onto main locally, then merge with fast-forward on main.

# Cherry-Pick

- ==Cherry-pick== applies a single commit from another branch onto the current branch.

```bash
git cherry-pick <commit-hash>
```

- Creates a new commit with a new hash but the same diff.
- Conflicts are resolved the same way as a merge conflict.
