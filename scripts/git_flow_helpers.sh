#!/usr/bin/env bash
# Simple helper for the CONTRIBUTING workflow
set -euo pipefail

cmd=${1:-"help"}

case "$cmd" in
  new)
    # ./git_flow_helpers.sh new <type> <slug>
    type=${2:?Specify feat|fix|docs}
    slug=${3:?Specify a short branch slug}
    git checkout main
    git fetch upstream
    git merge --ff-only upstream/main
    branch="${type}/${slug}"
    git checkout -b "$branch"
    echo "\xF0\x9F\x86\x95  Created branch $branch"
    ;;
  sync)
    git checkout main
    git fetch upstream
    git merge --ff-only upstream/main
    git push origin main
    echo "\xF0\x9F\x94\x84  main is now up-to-date with upstream"
    ;;
  *)
    cat <<'USAGE'
Usage:
  ./git_flow_helpers.sh new <feat|fix|docs> <slug>   # create branch
  ./git_flow_helpers.sh sync                         # sync local & fork
USAGE
    ;;
esac
