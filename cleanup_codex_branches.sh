#!/usr/bin/env bash
set -euo pipefail

OWNER="sunwoopark0512"          # repository owner
REPO="Auto_Pipeline"            # repository name
DAYS=7                           # prune branches unused for this many days
TOKEN="${GITHUB_TOKEN:-}"       # GitHub token, required for API calls

api() {
  curl -s -H "Authorization: Bearer $TOKEN" \
       -H "Accept: application/vnd.github+json" "$@"
}

# Fetch codex branches
mapfile -t branches < <(
  api "https://api.github.com/repos/$OWNER/$REPO/branches?per_page=100" \
  | jq -r '.[].name' | grep '-codex/'
)

echo "Found ${#branches[@]} codex branches."

# Check each branch
for br in "${branches[@]}"; do
  # Determine pull request state if exists
  pr_state=$(api \
      "https://api.github.com/repos/$OWNER/$REPO/pulls?state=all&head=$OWNER:$br" \
      | jq -r '.[0].state // empty')

  # Get date of last commit
  last_date=$(api "https://api.github.com/repos/$OWNER/$REPO/commits/$br" \
      | jq -r '.commit.author.date')
  last_ts=$(date -d "$last_date" +%s)
  threshold_ts=$(date -d "$DAYS days ago" +%s)

  if [[ "$pr_state" == "closed" || "$last_ts" -lt "$threshold_ts" ]]; then
    echo "🗑  Deleting $br  (PR:$pr_state  last:$last_date)"
    api -X DELETE "https://api.github.com/repos/$OWNER/$REPO/git/refs/heads/$br"
  fi
 done

echo "✅  Cleanup done."
