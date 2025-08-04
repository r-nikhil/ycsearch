# YC Search 

**Enhanced semantic search for 5,480+ Y Combinator companies (2005-2025)**

This is a modernized and significantly expanded version of the original [ycvibecheck](https://github.com/thesephist/ycvibecheck) by [@thesephist](https://github.com/thesephist). It uses _semantic similarity_ to search Y Combinator's **complete portfolio of 5,480 companies** by descriptions of ideas or verticals rather than keywords or categories.

## ✨ What's New in 2025

- **5,480 companies** (deduplicated from 10,459 raw entries - ~47% were duplicates!)
- **Complete coverage**: 2005-2025 across **87 unique batches** 
- **Latest batches**: W25, S25, F24, Sp25 with hundreds of new startups
- **Normalized batch names**: Consistent `W##/S##/F##/Sp##` format
- **Fixed sorting**: Homepage now shows newest companies first
- **Data quality improvements**: Automatic deduplication during embedding generation
- **Python 3.13** compatibility with updated dependencies

> ⚠️ **Important**: Embeddings are not included in this repository due to size (190MB). You must run `python server/generate.py` before using the search functionality.

Unlike the simple text search box in YC's [startup directory](https://www.ycombinator.com/companies), semantic search means this search bar doesn't need you to get the keywords exactly right, only close enough to what startups are building, to find them.

## 🏃‍♂️ Quick Start

### 1. **Clone & Setup**
```bash
git clone https://github.com/manassaloi/ycsearch.git
cd ycsearch
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. **Get YC Data** (⚠️ **REQUIRED** - Not included in repo)
```bash
# Option A: Use refresh script (downloads + processes + generates embeddings)
./refresh_yc_data.sh

# Option B: Manual steps
wget 'https://github.com/akshaybhalotia/yc_company_scraper/raw/main/data/yc_essential_data.json' -O data/raw/yc-raw.json
python server/process_raw_data.py  # Clean & normalize
python server/generate.py          # Generate embeddings (10-15 min)
```

### 3. **Run the Server**
```bash
export FLASK_APP=app.py
flask run --port 5001
```

### 4. **Start Searching!**
Visit `http://localhost:5001` and search for:
- `"AI startups"` → Latest AI companies across all batches
- `"climate change"` → Environmental tech companies  
- `"fintech"` → Financial technology startups
- `"W25"` → Filter by specific batch

## 📊 Dataset Details

- **5,480 YC companies** from 2005-2025 across **87 unique batches**
- **Complete coverage**: Winter, Summer, Fall, and Spring batches
- **Normalized batch names**: W##, S##, F##, Sp## format
- **Latest batches**: W25 (331 cos), S25 (48 cos), F24 (190 cos), Sp25 (143 cos)
- **Embeddings**: 190MB generated locally (⚠️ **not included in repo** - run `python server/generate.py`)

## 🔧 Data Pipeline & Quality

**Safe data pipeline prevents corruption and ensures consistency:**

- **📁 Data Separation**: Raw external data ≠ processed clean data
- **🔄 Deduplication**: Removes ~47% duplicate entries from source data
- **📝 Batch Normalization**: Converts "Winter 2025" → "W25" for consistency  
- **✅ Automatic Validation**: Format compliance and data integrity checks
- **💾 Automatic Backups**: Timestamped backups before any data refresh
- **🛡️ Overwrite Protection**: Raw data downloads never overwrite clean data

**Pipeline Flow:**
```
External Source → data/raw/ → process_raw_data.py → data/processed/ → generate.py → search
```

For complete pipeline details, see [PIPELINE.md](./PIPELINE.md) | For deployment, see [DEPLOYMENT.md](./DEPLOYMENT.md).

## 🏗️ Architecture

YC Search is built with [the Oak language](https://oaklang.org) and [Torus](https://github.com/thesephist/torus). It runs [sentence-transformers](https://www.sbert.net/) behind a [Flask](https://flask.palletsprojects.com/) server on the backend for semantic indexing and search. The dataset is based on [akshaybhalotia/yc_company_scraper](https://github.com/akshaybhalotia/yc_company_scraper).
