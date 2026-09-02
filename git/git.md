- ==Git== is a distributed version control system.
- It tracks changes to files by taking snapshots of the entire project at each commit, not diffs.
- Every developer has a full copy of the repository, including its entire history.

# Set Up

- Latest Github requires SSH [[authentication]]. Follow the [official guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to create the public/private key pair and paste the public key into Github settings.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

- These are attached to every commit you make. Required before your first commit.

```bash
git config --list    # show all config values
```

# Repositories

```bash
git init              # init new repo in current directory
git clone <url>       # copy repo locally (includes full history)
```

- `git init` creates a hidden `.git/` folder that stores all version history.
- `git clone` also sets up a ==remote== called `origin` pointing to the URL you cloned from.

# The Three Areas

- Git has three areas a file passes through.

**Working directory**
- The actual files on disk. Edits happen here.
**Staging area**
- A preparation zone. Only staged changes are included in the next commit.
**Repository**
- The `.git/` folder. Stores the full commit history as a chain of snapshots.

```
+-------------+   git add    +---------+  git commit  +------------+
| Working Dir | -----------> | Staging | -----------> | Repository |
|             | <----------- |         |              |  (.git/)   |
+-------------+  git restore +---------+              +------------+
```

# Staging and Committing

```bash
git status                # show which files are modified, staged, or untracked
git add <file>            # stage a specific file
git add .                 # stage all changes in current directory
git commit -m "message"   # commit staged changes with a message
git commit --amend        # replace last commit (rewrite message or add staged files)
```

- `git status` is the most commonly used command. Run it frequently.

# HEAD

- HEAD is a pointer that tells git which commit you are currently on.
- Normally, HEAD points to a branch name, and that branch points to a commit.

```
HEAD --> main --> commit C

  A --- B --- C
              |
            main
              |
            HEAD
```

- When you make a new commit, the branch pointer moves forward, and HEAD follows because it points to the branch.

**Detached HEAD**
- HEAD can point directly to a commit instead of a branch.
- This happens when you check out a specific commit hash or tag.

```bash
git checkout abc1234      # HEAD now points to abc1234, not a branch
```

```
HEAD --> commit B (no branch)

  A --- B --- C
        |     |
      HEAD  main
```

- Commits made in detached HEAD are not on any branch. They will be garbage collected unless you create a branch from them.

```bash
git switch -c new-branch  # create a branch at current detached HEAD position
```

# Branches

- A branch is a pointer to a commit. Default branch is `main`.
- Branches are cheap. Creating one just writes a 40-character hash to a file.

```bash
git branch                 # list local branches
git branch <name>          # create new branch at current commit
git switch <name>          # move HEAD to that branch
git switch -c <name>       # create + switch in one command
git branch -d <name>       # delete branch (fails if unmerged changes)
git branch -D <name>       # force delete (discards unmerged changes)
```

- A local branch is one you created or checked out. You commit to it directly.
- A remote-tracking branch is a read-only snapshot of where a branch is on the remote. Named `origin/<branch>`.

```
local:            main          (yours, moves when you commit)
remote-tracking:  origin/main   (read-only, moves when you fetch/pull)
```

- `git fetch` updates remote-tracking branches. `git push` updates the remote, then your remote-tracking branch matches.
- `origin/main` is not a branch you can commit to. It is a local record of the remote's state.

```bash
git branch -r              # list remote-tracking branches
git branch -a              # list all branches (local + remote-tracking)
```

# Upstream Tracking

- Upstream tracking links a local branch to a remote-tracking branch so git knows where to push and pull.
- When you `git clone`, the default branch is automatically set to track `origin/main`.

```bash
git push -u origin feature          # push and set origin/feature as upstream
git branch --set-upstream-to=origin/feature   # set upstream without pushing
git branch -vv                      # show all branches with their upstream
```

- Once set, `git push` and `git pull` work without specifying a remote or branch.

# Remote Operations

- `origin` is the default remote name after cloning.

```bash
git remote -v                         # list remotes with URLs
git remote add <name> <url>           # add a new remote
```

- `git fetch` downloads new commits from the remote but does not touch your working directory or local branches. Safe.
- `git pull` runs `git fetch` then `git merge`. It modifies your local branch.

```bash
git fetch                             # download from remote, don't merge
git pull                              # fetch + merge into current branch
```

```bash
git push                              # push current branch to its upstream
git push -u origin <branch>           # push + set upstream tracking
git push origin --delete <branch>     # delete a remote branch
git push --force                      # overwrite remote history (dangerous)
git push --force-with-lease           # overwrite only if no one else pushed since your last fetch (safer)
```

- `--force` discards commits on the remote that you don't have locally. Use `--force-with-lease` instead when rewriting history after a rebase.

# Viewing History

```bash
git log                    # full commit history
git log --oneline          # compact: one line per commit
git log --oneline --graph  # visual branch/merge graph
git log -n 5               # show last 5 commits
git show <commit>          # show a specific commit's diff and metadata
```

- Each commit has a commit hash, a 40-character SHA-1 string. You only need the first 7 characters to reference it.

```bash
git log --oneline
# e4a1f2c fix login bug
# 9b3d7a1 add user model
# 2c8e5f0 initial commit
```

# Diffing

```bash
git diff                   # unstaged changes (working dir vs staging)
git diff --staged          # staged changes (staging vs last commit)
git diff main..feature     # all differences between two branches
git diff <commit>..<commit>  # differences between two commits
```

# Stashing

- ==Stash== temporarily shelves uncommitted changes so you can switch context.
- Stash stores both staged and unstaged changes, then reverts your working directory to the last commit.

```bash
git stash                  # stash all uncommitted changes
git stash pop              # apply most recent stash + remove it from stash list
git stash list             # list all stashes
git stash apply            # apply most recent stash without removing it
git stash drop             # remove most recent stash without applying
```

# Undoing Changes

```bash
git restore <file>          # discard unstaged changes in working directory
git restore --staged <file> # unstage a file (move it back from staging to working dir)
git revert <commit>         # create a new commit that undoes a past commit's changes
```

- `git revert` is safe for shared history because it adds a new commit instead of deleting one.

**git reset**
- Moves HEAD and the current branch pointer back to a specified commit, effectively erasing commits after it from the branch.

```bash
git reset --soft <commit>   # move branch pointer, keep changes staged
git reset --mixed <commit>  # move branch pointer, keep changes unstaged (default)
git reset --hard <commit>   # move branch pointer, discard all changes
```

```
before reset (on main):
  A --- B --- C --- D
                    |
                  main/HEAD

git reset --soft B:
  A --- B     (C, D changes are staged)
        |
      main/HEAD

git reset --mixed B:
  A --- B     (C, D changes are in working dir, unstaged)
        |
      main/HEAD

git reset --hard B:
  A --- B     (C, D changes are gone)
        |
      main/HEAD
```

- Use `git log --oneline` to find the commit hash you want to reset to.

```bash
git log --oneline
# d4e5f6a (HEAD -> main) break everything
# a1b2c3d last good state
# 7e8f9a0 initial commit

git reset --hard a1b2c3d   # go back to "last good state"
```

- `--hard` is destructive. Uncommitted changes are permanently lost.
- `--soft` is useful when you want to redo commits. Changes from the erased commits stay staged so you can recommit them.

# Tags

- A tag is a named reference to a specific commit, typically used for release versions.

**Lightweight tag**
- Just a name pointing to a commit. No metadata.
**Annotated tag**
- Stores tagger name, date, and a message. Preferred for releases.

```bash
git tag v1.0                     # lightweight tag at current commit
git tag -a v1.0 -m "release 1"  # annotated tag
git push origin v1.0             # push a specific tag to remote
git push --tags                  # push all tags
```

# .gitignore

- A `.gitignore` file tells git which files to never track.
- Placed in the repository root.

```
node_modules/
*.log
.env
dist/
__pycache__/
```

- Patterns use glob syntax. `/` at the end means directory only. `*` matches any characters.
- Files already tracked are not affected by `.gitignore`. You must untrack them first.

```bash
git rm --cached <file>     # stop tracking a file without deleting it from disk
```

# Workflow

- Standard flow from cloning a repo to opening a pull request.

```bash
# 1. clone the repo
git clone https://github.com/user/repo.git
cd repo

# 2. create a feature branch
git switch -c feature/login

# 3. make edits, then stage and commit
git add auth.py
git commit -m "add login endpoint"

# 4. push the branch and set upstream
git push -u origin feature/login

# 5. open a pull request on GitHub (or use gh cli)
# after PR is reviewed and merged:

# 6. switch back to main and pull the merged changes
git switch main
git pull
```
