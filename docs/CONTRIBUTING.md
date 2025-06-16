# Contributing & Manual Pull-Request Workflow  
_Last updated: 2025-06-16_

This repository is mirrored into a read-only QA environment, so `git push` from here will always fail.  
To contribute code, **work locally** and follow the steps below.

## 0. One-time local setup
```bash
# clone your personal fork (recommended) or the main repo
git clone git@github.com:<your-username>/<repo>.git
cd <repo>

# add the canonical upstream so you can stay in sync
git remote add upstream git@github.com:<org>/<repo>.git
```

## 1. Keep your fork up-to-date

```bash
git fetch upstream
git checkout main
git merge --ff-only upstream/main
git push origin main   # keep GitHub fork current
```

## 2. Create a focused feature branch

```bash
git checkout -b feat/<short-slug>
```

| Branch prefix | Use for           | Example             |
| ------------- | ----------------- | ------------------- |
| **feat/**     | new functionality | `feat/cli-uploader` |
| **fix/**      | bug fixes         | `fix/typo-readme`   |
| **docs/**     | docs only         | `docs/contributing` |

## 3. Stage and commit

```bash
# verify you have no stray changes
git status

# add the files you actually changed
git add path/to/file1 path/to/file2

# commit using Conventional Commits
git commit -m "feat(cli): add initial uploader skeleton"
```

## 4. Push to your fork

```bash
git push --set-upstream origin feat/<short-slug>
```

## 5. Open the Pull Request

1. Visit `https://github.com/<your-username>/<repo>/pulls`.
2. Click **“Compare & pull request”**.
3. Target branch **`main`** in **`<org>/<repo>`**.
4. Fill in the PR template ⁠— include **why**, **what changed**, and screenshots/CI links if useful.
5. Submit. CI/CD will run automatically; once reviewers approve and **merge**, the downstream deployment pipeline will pick up `main` and redeploy.

## 6. Post-merge housekeeping

```bash
# back on your workstation
git checkout main
git pull upstream main   # grab the merge commit
git push origin main     # keep your fork aligned
```

---

### Troubleshooting

| Symptom                           | Likely Cause                             | Fix                                                            |
| --------------------------------- | ---------------------------------------- | -------------------------------------------------------------- |
| `fatal: unable to access ... 403` | Trying to push to `upstream` (read-only) | Push to `origin` instead                                       |
| CI fails after PR                 | lint/tests broken                        | Rebase onto latest `upstream/main`, fix, force-push            |
| “Nothing compares” page on GitHub | Wrong base/compare repos                 | Ensure **base** = `<org>/<repo>` and **compare** = your branch |

---

### Quick-start with helper script

If you prefer fewer keystrokes, run `./scripts/git_flow_helpers.sh new feat my-slug` to spin up a prepared feature branch, or `./scripts/git_flow_helpers.sh sync` to fast-forward your local `main`.

Happy hacking! 🙂
