# Branch cleanup (Nov 7 2026)

Rules used: delete a remote branch only if fully merged into `origin/main`, 0 commits ahead, not `main`/`master`/`deploy`, and not pushed to in the last 2 hours. Delete a local branch only if merged and nothing unpushed. Never force. Everything below is reversible.

## Eligible for deletion (remote)
| Branch | Tip SHA | Last push | Restore command |
|---|---|---|---|
| `backend` | `ca6c2e41eba795756d9aa9972ed5d80ff5f4be40` | about 2 h 18 min before this run | `git push origin ca6c2e41eba795756d9aa9972ed5d80ff5f4be40:refs/heads/backend` |

Status: the delete was **attempted from a terminal without GitHub credentials, so it did not run**. Run it yourself (GitHub: Branches page, trash icon, or `git push origin --delete backend`).

## Merged, but kept for now (pushed less than 2 hours ago)
`backend-refine` (`f6455f7`, 108 min), `fix-render-bom` (`b92f322`, 119 min), `catalogue` (`ede6531`, 85 min), `problems` (`5f21bdc`, 43 min), `frontend` (remote `02e1b16`, 39 min), `progress-hooks` (`680ad26`, 8 min). All are fully merged into `main`; they become eligible once they are 2 hours old.

## Not touched
- `deploy` (`686a468`): merged, but Render may track it. Check the Render dashboard (Settings, Branch). If Render uses `main` or something else, delete with `git push origin --delete deploy` (restore: `git push origin 686a468:refs/heads/deploy`).
- Local `frontend` (`15ddfd1`): merged into `main`, but it has 3 commits not on `origin/frontend` (all of them are in `main`), so the rule says keep. `git branch -d frontend` is safe if you want it gone.
