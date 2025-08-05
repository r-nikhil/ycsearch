# YC Search - Project Specification

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technical Architecture](#technical-architecture)
3. [Core Features](#core-features)
4. [User Interface & Experience](#user-interface--experience)
5. [Data Models & Business Logic](#data-models--business-logic)
6. [Authentication & Authorization](#authentication--authorization)
7. [API Documentation](#api-documentation)
8. [Configuration & Environment](#configuration--environment)
9. [Testing & Quality Assurance](#testing--quality-assurance)
10. [Development & Deployment](#development--deployment)

## 1. Project Overview

### Project Name
**YC Search**

### Description
YC Search is a semantic search engine that enables users to discover Y Combinator companies through natural language queries. It provides intelligent search capabilities over 5,480+ YC companies from 2005-2025 using AI-powered semantic similarity matching rather than traditional keyword-based search.

### Core Value Proposition
Solves the problem of ineffective keyword-based search by allowing users to search for companies using natural language descriptions of ideas, verticals, or business concepts. Users can find relevant companies even when they don't know exact terminology or company names.

## 2. Technical Architecture

### Technology Stack
- **Frontend**: Oak programming language, Torus.js (reactive framework), vanilla JavaScript
- **Backend**: Python Flask web server
- **AI/ML**: sentence-transformers library with all-mpnet-base-v2 model
- **Data Processing**: Python with JSON-based data pipeline
- **Styling**: CSS with CSS custom properties for theming
- **Deployment**: uWSGI for production serving

### Architecture Pattern
**Client-Server Architecture** with semantic search pipeline:
- Single-page application (SPA) frontend built with Oak/Torus
- RESTful Flask API backend
- ML-powered semantic similarity engine
- File-based data storage with JSON documents
- Preprocessing pipeline for data normalization and embedding generation

### Database/Storage
- **File-based JSON storage** (no traditional database)
- **Data files**:
  - `data/raw/yc-raw.json` - External source data
  - `data/processed/yc-clean.json` - Normalized, deduplicated data
  - `data/yc-embedded.json` - Companies with semantic embeddings
- **Backup system**: Automatic timestamped backups before data refresh

### External Dependencies
- **Y Combinator Data**: Via akshaybhalotia/yc_company_scraper repository
- **Hacker News API**: For fetching company-related news stories
- **Hugging Face Models**: sentence-transformers model hosting
- **YC Directory**: For additional company metadata scraping

## 3. Core Features

### Semantic Search Engine
- **Description**: Natural language search over YC company descriptions using AI embeddings
- **User Journey**: User types query → system encodes query → finds similar companies via cosine similarity → returns ranked results
- **Technical Implementation**: Uses sentence-transformers to generate embeddings, scipy for similarity calculations
- **API Endpoints**: `GET /search?text=query&batch=filter&show_inactive=bool&n=limit`

### Company Discovery & Filtering
- **Description**: Browse and filter companies by batch, status, and other criteria
- **User Journey**: Users can filter by specific YC batches (W25, S24, etc.) or company status (Active, Acquired, etc.)
- **Technical Implementation**: Client-side filtering of search results with URL state management
- **API Endpoints**: Same `/search` endpoint with filtering parameters

### Interactive Company Profiles
- **Description**: Expandable company cards with detailed information, news, and related links
- **User Journey**: Click company → expand details → view news/links → find similar companies
- **Technical Implementation**: Dynamic content loading with external API calls for news and metadata
- **API Endpoints**: `GET /company?slug=company-slug`

### Autocomplete & Search Suggestions
- **Description**: Real-time search suggestions based on company names and descriptions
- **User Journey**: User types → sees relevant company suggestions → can select to populate search
- **Technical Implementation**: Client-side fuzzy matching against preloaded company names/descriptions
- **API Endpoints**: `GET /preloads.js` for suggestion data

### Batch-based Company Organization
- **Description**: Companies organized by YC batch with consistent naming (W25, S24, F23, etc.)
- **User Journey**: Users can explore companies from specific time periods or cohorts
- **Technical Implementation**: Automated batch name normalization during data processing
- **API Endpoints**: Batch data provided via `/preloads.js`

### Related News Integration
- **Description**: Shows Hacker News stories and YC Directory news for each company
- **User Journey**: Expand company → view recent news → click to read full stories
- **Technical Implementation**: Client-side API calls to HN Algolia API and YC directory scraping
- **API Endpoints**: External HN API, internal company metadata endpoint

## 4. User Interface & Experience

### UI Framework/Library
- **Oak Language**: Functional programming language that compiles to JavaScript
- **Torus.js**: Reactive UI framework for component-based interfaces
- **Custom CSS**: Hand-crafted styles with CSS custom properties for theming

### Key Pages/Views
- **Homepage**: Search interface with welcome message and filtering options
- **Search Results**: Paginated list of companies with expandable details
- **Company Details**: Expanded view with full description, news, links, and metadata
- **No additional pages** - single-page application design

### Navigation Flow
1. **Landing** → Welcome message with search suggestions
2. **Search Input** → Type query or select from autocomplete
3. **Results View** → Browse filtered/ranked company list
4. **Company Focus** → Expand individual companies for details
5. **Related Discovery** → "More like this" to find similar companies

### Responsive Design
- **Mobile-first CSS** with responsive breakpoints
- **Adaptive layouts** for search interface and company cards
- **Touch-friendly** interactions for mobile devices
- **Keyboard navigation** support for accessibility

### Accessibility Features
- **Keyboard navigation** through search results
- **Focus management** for screen readers
- **Semantic HTML** structure with proper headings
- **Color contrast** compliance with WCAG guidelines
- **Skip links** and proper tab order

## 5. Data Models & Business Logic

### Core Data Entities

#### Company Entity
```json
{
  "id": "unique_identifier",
  "name": "Company Name",
  "slug": "url-friendly-name",
  "batch": "W25",
  "status": "Active|Acquired|Public|Inactive",
  "one_liner": "Brief description",
  "long_description": "Detailed description",
  "website": "https://example.com",
  "team_size": 50,
  "location": "San Francisco, CA",
  "industry": "Technology",
  "subindustry": "AI/ML",
  "tags": ["AI", "B2B"],
  "top_company": false,
  "nonprofit": false,
  "former_names": ["Previous Name"],
  "small_logo_thumb_url": "https://...",
  "description_embedding": [0.1, 0.2, ...]
}
```

#### Batch Entity
- **Format**: Consistent naming (W##, S##, F##, Sp##)
- **Validation**: Regex pattern `^(W|S|F|Sp)\d{2}$|^IK\d{2}$|^Unspecified$`
- **Sorting**: Reverse chronological order (newest first)

#### News Entity
```json
{
  "title": "News Title",
  "url": "https://...",
  "date": "2025-01-01",
  "objectID": "hn_story_id",
  "points": 150,
  "num_comments": 45
}
```

### Relationships
- **Company ↔ Batch**: Many-to-one (companies belong to batches)
- **Company ↔ News**: One-to-many (companies have multiple news stories)
- **Company ↔ Embeddings**: One-to-one (each company has one embedding vector)

### Business Rules

#### Data Quality Rules
- **Deduplication**: Companies deduplicated by slug during processing
- **Batch Normalization**: All batch names converted to standard format
- **Required Fields**: Name, slug, and batch are mandatory
- **Embedding Coverage**: Minimum 80% of companies must have embeddings

#### Search Logic
- **Semantic Ranking**: Results ranked by cosine similarity to query embedding
- **Status Filtering**: Inactive companies hidden by default
- **Batch Filtering**: Optional filtering by specific YC batch
- **Result Limiting**: Default 25 results, maximum 50

#### Data Pipeline Rules
- **Raw Data Separation**: External data never overwrites processed data
- **Backup Creation**: Automatic backups before any data refresh
- **Validation Gates**: All data validated before deployment
- **Processing Metadata**: Track processing statistics and timestamps

### Data Flow
```
External Source → data/raw/ → process_raw_data.py → data/processed/ → generate.py → data/yc-embedded.json → Flask API → Frontend
```

## 6. Authentication & Authorization

### Authentication Method
**No authentication required** - public read-only application

### User Roles/Permissions
**Single public role** - all users have identical read-only access to all data

### Security Measures
- **HTTPS enforcement** for production deployment
- **Input sanitization** for search queries
- **Rate limiting** considerations for production
- **No user data collection** - privacy-focused design
- **Static file serving** for frontend assets
- **CORS headers** for API access

## 7. API Documentation

### API Type
**RESTful HTTP JSON API**

### Base URL
- **Development**: `http://localhost:5001`
- **Production**: Configured via deployment

### Key Endpoints

#### Search Companies
```
GET /search
Parameters:
  - text (string, optional): Search query
  - batch (string, optional): Filter by YC batch (e.g., "W25")
  - show_inactive (boolean, optional): Include inactive companies
  - n (integer, optional): Number of results (default: 25, max: 50)
Response: JSON array of company objects
```

#### Get Company Details
```
GET /company
Parameters:
  - slug (string, required): Company URL slug
Response: JSON company object with additional metadata
```

#### Get Preloaded Data
```
GET /preloads.js
Response: JavaScript file containing YC_BATCHES and YC_NAMES_DESC constants
```

#### Serve Static Files
```
GET /
GET /css/*
GET /js/*
GET /img/*
Response: Static frontend assets
```

### Request/Response Formats
- **Content-Type**: `application/json`
- **Character Encoding**: UTF-8
- **Date Format**: ISO 8601 for timestamps
- **URL Encoding**: Standard percent encoding for parameters

### Error Handling
- **HTTP Status Codes**: 200 (success), 404 (not found), 500 (server error)
- **Error Response Format**: Plain text error messages
- **Client-side Handling**: User-friendly error display with retry options
- **Logging**: Server-side error logging for debugging

## 8. Configuration & Environment

### Environment Variables
- **FLASK_APP**: Application entry point (`app.py`)
- **FLASK_ENV**: Development/production mode
- **PORT**: Server port (default: 5001)

### Deployment Requirements
- **Python 3.7+** with pip package manager
- **190MB+ disk space** for embeddings file
- **2GB+ RAM** for sentence-transformers model
- **Internet access** for initial data download and model loading

### Third-party Integrations
- **Hugging Face**: Model hosting and downloads
- **YC Company Scraper**: Raw data source
- **Hacker News API**: News story integration
- **YC Directory**: Additional company metadata

## 9. Testing & Quality Assurance

### Testing Framework
**Custom validation scripts** rather than traditional unit tests

### Test Coverage
- **Data Validation**: `scripts/validate_data.py` ensures data quality
- **Format Validation**: Batch name format compliance
- **Duplicate Detection**: Company deduplication verification
- **Embedding Coverage**: Minimum embedding threshold checks
- **Integration Testing**: End-to-end data pipeline validation

### Quality Tools
- **Python**: Built-in JSON validation and error handling
- **Data Pipeline**: Automated validation at each processing stage
- **Manual QA**: Visual inspection of search results and UI
- **Production Monitoring**: Error tracking and performance monitoring

## 10. Development & Deployment

### Development Setup
```bash
# Clone repository
git clone https://github.com/manassaloi/ycsearch.git
cd ycsearch

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download and process data
./refresh_yc_data.sh

# Start development server
export FLASK_APP=app.py
flask run --port 5001
```

### Build Process
- **Oak compilation**: `oak build --web` generates JavaScript bundle
- **Asset bundling**: Static files served directly by Flask
- **No complex build pipeline** - direct file serving
- **CSS preprocessing**: None required (vanilla CSS)

### Deployment Strategy
- **Production Server**: uWSGI with Flask application
- **Static Files**: Served directly by web server
- **Data Pipeline**: Scheduled refresh scripts for data updates
- **Service Configuration**: systemd service file (`ycsearch.service`)
- **Domain Setup**: Reverse proxy configuration

### Monitoring & Logging
- **Application Logs**: Flask built-in logging
- **Error Tracking**: Custom error handlers with user feedback
- **Performance Monitoring**: Response time tracking
- **Data Quality Monitoring**: Validation script outputs
- **Uptime Monitoring**: External service monitoring

---

*This specification was generated based on codebase analysis as of August 2025. The project continues to evolve with regular data updates and feature improvements.*
