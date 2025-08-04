# YC Search Deployment Guide

## Critical Data Pipeline Process

**⚠️ NEVER manually edit `data/yc-embedded.json` - all changes must go through the pipeline!**

### Data Regeneration Checklist

Before regenerating embeddings (`python server/generate.py`):

- [ ] **Backup current data**: `cp data/yc-embedded.json data/yc-embedded.json.backup`
- [ ] **Verify source data**: Check `data/yc.json` for expected format
- [ ] **Run generation**: `python server/generate.py`
- [ ] **Verify validation passes**: Should see "✅ Data generation and validation completed successfully!"
- [ ] **Test locally**: Start server and verify batch dropdown shows W##/S##/F## format
- [ ] **Check for duplicates**: Search for known companies (e.g., "Striga") - should appear only once
- [ ] **Restart server**: Always restart after regenerating data

### What the Pipeline Does

1. **Loads raw data** from `data/yc.json`
2. **Deduplicates** by company slug (first occurrence wins)
3. **Normalizes batch names**: "Winter 2025" → "W25", "Summer 2023" → "S23"
4. **Generates embeddings** for semantic search
5. **Validates output** format and consistency
6. **Saves clean data** to `data/yc-embedded.json`

### Validation Checks

The pipeline automatically validates:
- ✅ Batch format consistency (W##/S##/F##/Sp## only)
- ✅ No duplicate company slugs
- ✅ Required fields present (name, slug, batch)
- ✅ Embedding coverage >80%

### Troubleshooting

**"Invalid batch formats found"**: 
- Check `normalize_batch_name()` function in `server/generate.py`
- New batch formats may need pattern additions

**"Duplicate company slugs found"**:
- Issue with external data source
- Deduplication logic may need adjustment

**Server showing old batch names**:
- Restart Flask server: `pkill -f "flask run" && flask run --port 5001`
- Server loads data at startup, not dynamically

### Emergency Recovery

If bad data is generated:
1. Stop server: `pkill -f "flask run"`
2. Restore backup: `cp data/yc-embedded.json.backup data/yc-embedded.json`
3. Restart server: `flask run --port 5001`
4. Debug pipeline before regenerating

## Never Do This ❌

- Don't manually edit `data/yc-embedded.json`
- Don't skip validation
- Don't deploy without testing locally
- Don't assume server auto-reloads data (it doesn't!)

## Always Do This ✅

- Run full pipeline for any data changes
- Validate before deploying
- Test batch dropdown format
- Test search for known duplicates
- Restart server after data regeneration