# CLAUDE.md - Development Guide for AI Assistants

## 🎯 Project Overview
**YC Search** - Semantic search over 5,480+ Y Combinator companies (2005-2025) using Oak language + Python Flask backend.

## 🚨 Critical Information (READ FIRST!)

### Tech Stack
- **Frontend**: Oak language → compiles to JavaScript
- **UI Framework**: Torus.js (reactive components)
- **Backend**: Python Flask (port 5001)
- **AI/ML**: sentence-transformers with all-mpnet-base-v2 model
- **Data**: JSON files with semantic embeddings (190MB)

### Build System (ESSENTIAL!)
```bash
# ALWAYS use Makefile commands:
make build    # oak build --entry src/app.js.oak --output static/js/bundle.js --web
make watch    # auto-rebuild on Oak file changes
make serve    # flask run (port 5001)
make fmt      # format Oak code

# HTML loads /js/bundle.js (NOT main.js!)
# Never manually run oak build commands - use the Makefile!
```

## 📁 Critical File Structure

```
YCSearch/
├── static/
│   ├── index.html          # Loads /js/bundle.js
│   ├── js/
│   │   ├── bundle.js       # ⚠️ THIS is what HTML loads!
│   │   ├── main.js         # ❌ Ignore this (wrong output)
│   │   └── torus.min.js
│   └── css/main.css
├── src/
│   └── app.js.oak          # Main frontend code
├── lib/
│   ├── torus.js.oak        # UI framework
│   └── search.js.oak       # Search logic
├── data/
│   ├── raw/yc-raw.json     # External source (messy)
│   ├── processed/yc-clean.json  # Deduplicated/normalized
│   └── yc-embedded.json    # Final embeddings (190MB)
├── server/
│   ├── app.py              # Flask backend
│   ├── generate.py         # Creates embeddings
│   └── process_raw_data.py # Cleans raw data
└── Makefile               # ⚠️ READ THIS FIRST!
```

## ⚡ Quick Start Protocol

### For ANY change to frontend:
```bash
# 1. Edit Oak files in src/ or lib/
# 2. Build using Makefile:
make build
# 3. Verify bundle.js was updated:
ls -la static/js/bundle.js
# 4. Test on http://localhost:5001
```

### For data changes:
```bash
# Never edit data/yc-embedded.json directly!
# Use the safe pipeline:
./refresh_yc_data.sh        # Full refresh
# OR manual steps:
python server/process_raw_data.py  # Clean raw data
python server/generate.py         # Generate embeddings
```

## 🔧 Development Workflow

### Starting Development
```bash
# 1. Start server (in terminal 1):
make serve

# 2. Watch for changes (in terminal 2):
make watch

# 3. Edit files in src/app.js.oak
# 4. Changes auto-build and appear at http://localhost:5001
```

### Common Tasks
```bash
# Frontend changes:
vim src/app.js.oak    # Edit Oak code
make build           # Compile to bundle.js
# Server auto-serves updated bundle.js

# CSS changes:
vim static/css/main.css  # Direct editing
# No build needed - Flask serves directly

# Backend changes:
vim server/app.py    # Edit Python
# Restart: Ctrl+C, then `make serve`
```

## 🚨 Common Mistakes to Avoid

### ❌ Wrong Build Commands
```bash
# NEVER do this:
oak build --entry src/app.js.oak --output static/js/main.js --web

# ALWAYS do this:
make build
```

### ❌ Wrong File References
- HTML loads `/js/bundle.js` (not main.js)
- Always verify: `grep "bundle\|main" static/index.html`

### ❌ Data Pipeline Violations
- Never edit `data/yc-embedded.json` directly
- Always use `python server/generate.py` for embeddings
- Always restart server after data changes

### ❌ Server Assumptions
- Server runs on port 5001 (not 5000)
- Server doesn't auto-reload data (restart required)
- Flask serves static files directly (no webpack/vite)

## 📋 Pre-Change Checklist

Before making ANY changes:
```bash
# 1. Understand the system:
cat Makefile                    # Build commands
grep -r "bundle\|main" static/  # File references
ls static/js/                   # What files exist

# 2. Read relevant docs:
cat PROJECT_SPECIFICATION.md   # Architecture
cat DEPLOYMENT.md              # Critical processes
cat PIPELINE.md                # Data flow

# 3. Verify current state:
lsof -i :5001                  # Server running?
ls -la static/js/bundle.js     # Bundle exists?
```

## 🎯 Architecture Quick Reference

### Frontend (Oak/Torus)
- **Single Page App** with reactive components
- **State Management**: Global `State` object
- **Routing**: URL state management (no router)
- **Styling**: Vanilla CSS with custom properties
- **Build**: Oak → JavaScript compilation

### Backend (Flask)
- **Port**: 5001 (not 5000!)
- **Endpoints**: `/search`, `/company`, `/preloads.js`
- **Static Files**: Served directly by Flask
- **Data Loading**: At startup only (restart required for changes)

### Data Pipeline
```
External → raw/ → process_raw_data.py → processed/ → generate.py → embeddings
```
- **Never skip steps** in the pipeline
- **Always validate** after generation
- **Always backup** before regeneration

## 🛠️ Debugging Common Issues

### Frontend not updating?
```bash
# Check build output:
make build
ls -la static/js/bundle.js
grep -A5 -B5 "your-change" static/js/bundle.js

# Hard refresh browser:
Ctrl+Shift+R or Cmd+Shift+R
```

### Search not working?
```bash
# Check embeddings exist:
ls -la data/yc-embedded.json   # Should be ~190MB
python server/generate.py      # Regenerate if missing
```

### Wrong batch names showing?
```bash
# Data pipeline issue:
python server/process_raw_data.py  # Clean data
python server/generate.py         # Generate embeddings
pkill -f flask && make serve      # Restart server
```

## 📖 Documentation Hierarchy

1. **CLAUDE.md** (this file) - Quick development reference
2. **Makefile** - Build commands and shortcuts  
3. **PROJECT_SPECIFICATION.md** - Complete architecture
4. **DEPLOYMENT.md** - Critical deployment processes
5. **PIPELINE.md** - Data pipeline details
6. **README.md** - User-facing setup guide

## 🎉 Success Patterns

### For UI Changes:
1. Edit `src/app.js.oak`
2. Run `make build`
3. Verify in browser at `localhost:5001`
4. Check `static/js/bundle.js` was updated

### For Data Changes:
1. Use `./refresh_yc_data.sh` OR pipeline scripts
2. Verify `data/yc-embedded.json` exists (~190MB)
3. Restart Flask server
4. Test search functionality

### For Deployment:
1. Read `DEPLOYMENT.md` first
2. Follow data pipeline checklist
3. Use `make build` for frontend
4. Restart server after any data changes

---

**⚠️ Remember**: This project has excellent documentation - always check the relevant .md files before making assumptions!