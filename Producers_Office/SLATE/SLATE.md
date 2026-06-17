# Active Slate

Managed by `artifacts/production/slate_manager.py`. Max **10** concurrent titles.

## Seed command
```bash
python artifacts/production/slate_manager.py seed
python artifacts/production/slate_manager.py list
```

## Priority order (default seed)
1. Henry II — PI_Story test scenes
2. History — 20-scene ingest
3. GFE — Phase 2 staged production
4. MAGAZINE — Casting plate pass
5. Talent Agency — Performance studies → agency_ready

## Producer rules
- New project requires Legal Gate **GREEN** or **YELLOW** before slate add
- **RED** = not on slate, period
- Director cannot override slate cap without Producer sign-off