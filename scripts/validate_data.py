#!/usr/bin/env python3
"""
Data validation script to ensure consistency in YC company data.
Run this after any data generation to verify quality.
"""

import json
import re
import sys

def validate_yc_data(file_path='data/yc-embedded.json'):
    """Validate YC data for consistency and quality."""
    print(f"🔍 Validating {file_path}...")
    
    try:
        with open(file_path, 'r') as f:
            companies = json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: {file_path} not found. Run 'python server/generate.py' first.")
        return False
    except json.JSONDecodeError:
        print(f"❌ ERROR: {file_path} is not valid JSON.")
        return False
    
    errors = []
    
    # 1. Validate batch format consistency
    batches = set(co.get('batch', 'Unknown') for co in companies)
    invalid_batches = [b for b in batches if not re.match(r'^(W|S|F|Sp)\d{2}$|^IK\d{2}$|^Unspecified$', b)]
    
    if invalid_batches:
        errors.append(f"Invalid batch formats: {invalid_batches}")
    
    # 2. Check for duplicates by slug
    slugs = [co.get('slug') for co in companies if co.get('slug')]
    duplicate_slugs = set([slug for slug in slugs if slugs.count(slug) > 1])
    
    if duplicate_slugs:
        errors.append(f"Duplicate company slugs found: {list(duplicate_slugs)[:5]}...")
    
    # 3. Validate required fields
    required_fields = ['name', 'slug', 'batch']
    missing_fields = []
    
    for i, co in enumerate(companies[:100]):  # Sample first 100
        for field in required_fields:
            if not co.get(field):
                missing_fields.append(f"Company {i}: missing {field}")
    
    if missing_fields:
        errors.append(f"Missing required fields: {missing_fields[:3]}...")
    
    # 4. Validate embeddings exist
    companies_with_embeddings = [co for co in companies if co.get('description_embedding')]
    embedding_ratio = len(companies_with_embeddings) / len(companies)
    
    if embedding_ratio < 0.8:  # At least 80% should have embeddings
        errors.append(f"Low embedding coverage: {embedding_ratio:.1%} (expected >80%)")
    
    # Report results
    if errors:
        print("❌ VALIDATION FAILED:")
        for error in errors:
            print(f"  • {error}")
        return False
    else:
        print(f"✅ VALIDATION PASSED:")
        print(f"  • {len(companies)} companies processed")
        print(f"  • {len(batches)} unique batches")
        print(f"  • {len(companies_with_embeddings)} companies with embeddings ({embedding_ratio:.1%})")
        print(f"  • 0 duplicates found")
        return True

if __name__ == "__main__":
    success = validate_yc_data()
    sys.exit(0 if success else 1)