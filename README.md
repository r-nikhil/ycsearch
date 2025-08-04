# YC Search 

**Enhanced semantic search for 10,000+ Y Combinator companies (2005-2025)**

This is a modernized and significantly expanded version of the original [ycvibecheck](https://github.com/thesephist/ycvibecheck) by [@thesephist](https://github.com/thesephist). It uses _semantic similarity_ to search Y Combinator's **complete portfolio of 10,459 companies** by descriptions of ideas or verticals rather than keywords or categories.

## ✨ What's New in 2025

- **10,459 companies** (up from 4,079) - **+6,380 new companies**
- **Complete coverage**: 2005-2025 across **87 unique batches** 
- **Latest batches**: W25, S25, F24, Sp25 with hundreds of new startups
- **Normalized batch names**: Consistent `W##/S##/F##/Sp##` format
- **Fixed sorting**: Homepage now shows newest companies first
- **Python 3.13** compatibility with updated dependencies

![Screen recording of a search results page on YC Vibe Check](/static/img/screen-recording.gif)

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

### 2. **Generate Embeddings** (Required for search)
```bash
# This will take 15-30 minutes to process 10,459 companies
python server/generate.py
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

- **10,459 YC companies** from 2005-2025 across **87 unique batches**
- **Complete coverage**: Winter, Summer, Fall, and Spring batches
- **Normalized batch names**: W##, S##, F##, Sp## format
- **Latest batches**: W25 (331 cos), S25 (48 cos), F24 (190 cos), Sp25 (143 cos)
- **Embeddings**: 190MB generated with sentence-transformers

YC Search is built with [the Oak language](https://oaklang.org) and [Torus](https://github.com/thesephist/torus). It runs [sentence-transformers](https://www.sbert.net/) behind a [Flask](https://flask.palletsprojects.com/) server on the backend for semantic indexing and search. The dataset is based on [akshaybhalotia/yc_company_scraper](https://github.com/akshaybhalotia/yc_company_scraper).