# YC Search Data Pipeline

## Overview

This project implements a **safe data pipeline** that prevents the data corruption issues you experienced. The pipeline separates raw external data from processed data, ensuring your clean normalized data never gets accidentally overwritten.

## Directory Structure

```
data/
├── raw/                    # External source data (re-downloadable)
│   └── yc-raw.json        # Direct from GitHub scraper
├── processed/             # Clean, normalized data (protected)
│   ├── yc-clean.json     # Deduplicated & normalized
│   └── processing-metadata.json
├── backups/               # Automatic backups
│   └── yc-clean-YYYYMMDD_HHMMSS.json
└── yc-embedded.json       # Final embeddings for search
```

## Pipeline Flow

```
External Source → Raw Data → Processing → Clean Data → Embeddings → Search
     ↓              ↓           ↓           ↓           ↓          ↓
GitHub/scraper → raw/ → process_raw_data.py → processed/ → generate.py → search
```

## Commands

### Safe Data Refresh
```bash
# This will NEVER overwrite your clean data
./refresh_yc_data.sh
```

### Manual Steps
```bash
# 1. Download raw data
wget 'https://...' -O data/raw/yc-raw.json

# 2. Process raw data (deduplicate + normalize)
python server/process_raw_data.py

# 3. Generate embeddings from clean data
python server/generate.py

# 4. Validate everything worked
python scripts/validate_data.py
```

## What Was Fixed

### The Problem
- External scraper data has messy format: "Winter 2021", "Summer 2023"
- External data contains ~47% duplicates
- Old pipeline directly overwrote clean data with messy external data
- Running `./refresh_yc_data.sh` destroyed local improvements

### The Solution
- **Raw data** stays in `data/raw/` (re-downloadable, messy)
- **Processed data** in `data/processed/` (clean, protected)
- **Automatic backups** before any data refresh
- **Built-in validation** catches format regressions
- **Pipeline separation** prevents accidental overwrites

## Data Quality Guarantees

✅ **Batch names**: Consistent `W##/S##/F##/Sp##` format  
✅ **No duplicates**: Deduplicated by company slug  
✅ **Validation**: Format compliance checks  
✅ **Backups**: Automatic timestamped backups  
✅ **Separation**: Raw vs processed data isolation  

## Recovery

If something goes wrong:
```bash
# List available backups
ls data/backups/

# Restore from backup
cp data/backups/yc-clean-20250105_012345.json data/processed/yc-clean.json

# Regenerate embeddings
python server/generate.py
```

## Monitoring

The pipeline automatically:
- Validates batch format consistency
- Checks for duplicate entries  
- Reports data quality metrics
- Creates processing metadata
- Runs post-generation validation

This ensures you'll never lose clean data again and prevents the regression you experienced.