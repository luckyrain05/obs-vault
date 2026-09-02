
- The ==GitHub API== allows programmatic access to [[git|GitHub]] resources (repos, issues, PRs, users, etc.).
- Supports both [[api#GraphQL|graphql]] and [[api#REST|rest]] format.

# Authentication

```bash
# personal access token (PAT) in header
curl -H "Authorization: token ghp_xxxxxxxxxxxx" https://api.github.com/user

# GitHub CLI handles auth automatically
gh auth login
```

- PATs are generated in GitHub Settings > Developer Settings > Personal Access Tokens.
- ==Scopes== control what the token can access (`repo`, `read:org`, `workflow`, etc.).
- Fine-grained tokens let you restrict access to specific repositories.

# REST API

- Base URL: `https://api.github.com`.
- Standard REST verbs: `GET`, `POST`, `PATCH`, `DELETE`.

```bash
# list repos for a user
curl https://api.github.com/users/<username>/repos

# get a specific repo
curl https://api.github.com/repos/<owner>/<repo>

# create an issue
curl -X POST -H "Authorization: token <PAT>" \
  -d '{"title":"bug","body":"description"}' \
  https://api.github.com/repos/<owner>/<repo>/issues

# list pull requests
curl https://api.github.com/repos/<owner>/<repo>/pulls
```

# Pagination

- Responses are paginated by default (30 items per page).
- Use `?page=2&per_page=100` query params to navigate. Max 100 per page.
- The `Link` header contains URLs for `next`, `prev`, `first`, `last` pages.

# Rate Limits

- Authenticated: 5000 requests/hour.
- Unauthenticated: 60 requests/hour.
- Check remaining quota with `X-RateLimit-Remaining` response header.

# GitHub CLI

- `gh` is the official CLI tool that wraps the API.

```bash
gh repo clone <owner>/<repo>
gh issue list
gh issue create --title "bug" --body "description"
gh pr list
gh pr create --title "feature" --body "adds X"
gh pr checkout <number>         # fetch + switch to PR branch locally
gh pr merge <number>
gh pr review <number> --approve
```

```bash
# direct API calls through gh (auto-authenticated)
gh api repos/<owner>/<repo>/issues
gh api graphql -f query='{ viewer { login } }'
```

# GraphQL API

- Single endpoint: `https://api.github.com/graphql`.
- Request only the fields you need in one query instead of multiple REST calls.

```bash
curl -X POST -H "Authorization: bearer <PAT>" \
  -d '{"query":"{ viewer { login repositories(first:5) { nodes { name } } } }"}' \
  https://api.github.com/graphql
```

- All GraphQL requests use `POST`. The query goes in the JSON body.
- Useful when you need nested or related data that would require several REST calls.

# Webhooks

- ==Webhooks== push events from GitHub to your server instead of polling the API.
- Configured per-repo in Settings > Webhooks.
- GitHub sends a `POST` request to your URL on events like `push`, `pull_request`, `issues`.
- Payload is JSON. Verify authenticity with the `X-Hub-Signature-256` header using your webhook secret.
