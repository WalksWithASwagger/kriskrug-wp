# The Sky Smoked Back Work card apply, 2026-09-20

**Status:** Work page live. Aurora 1.6.12 footer change prepared, not deployed.
**Track:** Track A live page update plus separately versioned Track B source.
**Issue:** [#1042](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1042)

## Live change

WordPress page 2672, slug `work`, received one Creative AI Human Lab card before Photography:

- title: `The Sky Smoked Back`
- destination: `https://lightningstrike.org/`
- label: `Storm film`
- description: `A 56-second film, live browser storm, and public memory map made from one rare Vancouver lightning night.`

The apply used `scripts/add_sky_smoked_back_work_card.py`. The dry run verified page identity and the exact insert. The apply captured a mode-0600 snapshot, rechecked the page hash immediately before writing, and preserved the rest of the live body byte-for-byte after removing the inserted card.

## Verification

- WordPress modified time: `2026-09-20T18:05:25Z`
- before content SHA-256: `51f9bd21657612ec2a683550129ebc947c43e51a9a16802a783cb2732c3d9bfd`
- public cache-bypass readback: `https://kriskrug.co/work/?cb=20260920180621`
- public accessibility readback exposes exactly one `Explore The Sky Smoked Back` link between unofficial.city and Photography
- authenticated no-op rerun verified exactly one project card

## Rollback

Snapshot and rollback manifest:

- `backup/20260920T180523Z-sky-smoked-back-work-card/page-2672-before-project-card-20260920T180524Z.json`
- `backup/20260920T180523Z-sky-smoked-back-work-card/rollback-manifest.json`

Restore with Varlock from the repository root:

```bash
make varlock-run CMD='python3 scripts/add_sky_smoked_back_work_card.py --restore backup/20260920T180523Z-sky-smoked-back-work-card/page-2672-before-project-card-20260920T180524Z.json --apply'
```

## Pending release

Aurora 1.6.12 adds the same project to the sitewide Projects footer. It remains undeployed until KK approves the specific release and chooses the documented wp-admin zip or Pagely SFTP channel.
