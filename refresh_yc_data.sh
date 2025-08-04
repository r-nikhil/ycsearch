#!/bin/bash
set -e  # Exit on any error

echo "🔄 Starting YC data refresh pipeline..."

# 1. Backup current processed data
echo "📦 Backing up current data..."
timestamp=$(date +"%Y%m%d_%H%M%S")
if [ -f "data/processed/yc-clean.json" ]; then
    cp data/processed/yc-clean.json data/backups/yc-clean-${timestamp}.json
    echo "✅ Backup saved: data/backups/yc-clean-${timestamp}.json"
fi

# 2. Download fresh raw data (NEVER overwrites processed data)
echo "⬇️  Downloading fresh raw data..."
wget 'https://github.com/akshaybhalotia/yc_company_scraper/raw/main/data/yc_essential_data.json' -O data/raw/yc-raw.json

# 3. Activate virtualenv
source .venv/bin/activate

# 4. Process raw data through normalization pipeline
echo "🔧 Processing raw data through normalization pipeline..."
python server/process_raw_data.py

# 5. Generate embeddings from clean processed data
echo "🧠 Generating embeddings from clean data..."
python server/generate.py

echo "✅ Data refresh pipeline completed successfully!"
echo "📊 Run 'python scripts/validate_data.py' to verify data quality"

