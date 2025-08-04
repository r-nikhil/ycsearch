#!/usr/bin/env python3
"""
Raw Data Processing Pipeline
Converts messy external data into clean, normalized format.

Input:  data/raw/yc-raw.json (directly from external source)
Output: data/processed/yc-clean.json (normalized and deduplicated)
"""

import json
import re
from datetime import datetime

def normalize_batch_name(batch):
    """Normalize batch names to consistent W##/S##/F##/Sp## format"""
    if not batch:
        return "Unspecified"
    
    # Handle various batch name formats
    batch_patterns = [
        (r'^Winter (\d{4})$', lambda m: f'W{m.group(1)[2:]}'),
        (r'^Summer (\d{4})$', lambda m: f'S{m.group(1)[2:]}'),
        (r'^Fall (\d{4})$', lambda m: f'F{m.group(1)[2:]}'),
        (r'^Spring (\d{4})$', lambda m: f'Sp{m.group(1)[2:]}'),
        (r'^W(\d{2})$', lambda m: f'W{m.group(1)}'),  # Already correct format
        (r'^S(\d{2})$', lambda m: f'S{m.group(1)}'),  # Already correct format  
        (r'^F(\d{2})$', lambda m: f'F{m.group(1)}'),  # Already correct format
        (r'^Sp(\d{2})$', lambda m: f'Sp{m.group(1)}'), # Already correct format
    ]
    
    for pattern, replacement in batch_patterns:
        match = re.match(pattern, batch)
        if match:
            return replacement(match)
    
    # Return as-is if no pattern matches (e.g., "IK12", "Unspecified")
    return batch

def validate_raw_data(companies):
    """Validate raw data and warn about potential issues"""
    print(f"📊 Raw data analysis:")
    print(f"   • Total companies: {len(companies)}")
    
    # Check batch formats
    batch_counts = {}
    long_form_count = 0
    
    for co in companies:
        batch = co.get('batch', 'Unknown')
        batch_counts[batch] = batch_counts.get(batch, 0) + 1
        
        if re.match(r'(Winter|Summer|Fall|Spring) \d{4}', batch):
            long_form_count += 1
    
    print(f"   • Companies with long-form batch names: {long_form_count}")
    print(f"   • Unique batches: {len(batch_counts)}")
    
    # Check for duplicates
    slugs = [co.get('slug') for co in companies if co.get('slug')]
    duplicate_count = len(slugs) - len(set(slugs))
    print(f"   • Duplicate companies: {duplicate_count}")
    
    if duplicate_count > len(companies) * 0.4:  # >40% duplicates
        print("⚠️  WARNING: High duplicate rate detected!")
        
    return True

def process_raw_data():
    """Main processing function"""
    print("🔧 Processing raw YC data...")
    
    # Load raw data
    try:
        with open('data/raw/yc-raw.json', 'r') as f:
            raw_companies = json.load(f)
    except FileNotFoundError:
        print("❌ ERROR: data/raw/yc-raw.json not found!")
        print("Run the refresh script to download raw data first.")
        exit(1)
    except json.JSONDecodeError:
        print("❌ ERROR: Invalid JSON in raw data file")
        exit(1)
    
    # Validate raw data
    validate_raw_data(raw_companies)
    
    print("🧹 Cleaning and normalizing data...")
    
    # Deduplicate by slug (keep first occurrence)
    seen_slugs = set()
    clean_companies = []
    normalization_count = 0
    
    for co in raw_companies:
        # Skip duplicates
        slug = co.get('slug')
        if not slug or slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        
        # Normalize batch name
        original_batch = co.get('batch', 'Unspecified')
        normalized_batch = normalize_batch_name(original_batch)
        
        if original_batch != normalized_batch:
            normalization_count += 1
            print(f"   📝 {co.get('name', 'Unknown')}: {original_batch} → {normalized_batch}")
        
        co['batch'] = normalized_batch
        clean_companies.append(co)
    
    print(f"✅ Data cleaning completed:")
    print(f"   • {len(raw_companies)} → {len(clean_companies)} companies (removed {len(raw_companies) - len(clean_companies)} duplicates)")
    print(f"   • {normalization_count} batch names normalized")
    
    # Save processed data
    output_file = 'data/processed/yc-clean.json'
    with open(output_file, 'w') as f:
        json.dump(clean_companies, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Clean data saved to: {output_file}")
    
    # Add processing metadata
    metadata = {
        'processed_at': datetime.now().isoformat(),
        'raw_count': len(raw_companies),
        'clean_count': len(clean_companies),
        'duplicates_removed': len(raw_companies) - len(clean_companies),
        'normalizations_applied': normalization_count
    }
    
    with open('data/processed/processing-metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return clean_companies

if __name__ == "__main__":
    process_raw_data()