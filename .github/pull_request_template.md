## What

<!-- One-paragraph summary. -->

## Why

<!-- What gap or bug is this closing? -->

## How to verify

```bash
make install
make test
make validate
make bench-stub
```

## Checklist

- [ ] `make test` is green
- [ ] `make validate` reports 60/60 (or more, if you added tasks)
- [ ] New task files are under `tasks/<category>/` and follow `tasks/schema.json`
- [ ] No new dependencies without updating `pyproject.toml`
- [ ] No new top-level files without a reason
