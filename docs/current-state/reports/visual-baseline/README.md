# Visual-baseline artifact retention

The run directories in this folder contain local, gitignored PNG captures.
The top-level `manifest-*.json`, `diff-*.json`, and `report-*.md` files are the
tracked audit record and are never removed by `visual-prune`.

After a deploy window closes, retain the newest baseline and the newest complete
pre/post diff pair. Preview the exact local deletion set first:

```bash
make visual-prune KEEP=2 DRY_RUN=1
```

`KEEP` is a minimum directory count. If a retained candidate has a tracked diff,
its referenced baseline is retained too, so pair integrity can increase the
actual number kept. Put the dry-run paths and sizes through KK for approval,
then repeat the command without `DRY_RUN=1`.
