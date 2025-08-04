import json
import re
from sentence_transformers import SentenceTransformer

# Generate embeddings from clean processed data
# Raw data processing is handled by server/process_raw_data.py

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Load clean processed data (already deduplicated and normalized)
try:
    with open('data/processed/yc-clean.json', 'r') as yc_file:
        yc_companies = json.load(yc_file)
        print(f'Loaded {len(yc_companies)} clean companies from processed data')
except FileNotFoundError:
    print("❌ ERROR: data/processed/yc-clean.json not found!")
    print("Run 'python server/process_raw_data.py' first to process raw data.")
    exit(1)

for i, co in enumerate(yc_companies):
    print(f'{i}/{len(yc_companies)}', co['name'])
    
    description = co.get('long_description') or co.get('one_liner')
    if not description:
        print(f'{co["name"]} has no long_description or one_liner, skipping semantic indexing')
        continue
    embedding = model.encode(description.strip())
    co['description_embedding'] = embedding.tolist()

# Validate data quality before saving
batch_formats = set(co['batch'] for co in yc_companies)
invalid_batches = [b for b in batch_formats if not re.match(r'^(W|S|F|Sp)\d{2}$|^IK\d{2}$|^Unspecified$', b)]

if invalid_batches:
    print(f"❌ ERROR: Invalid batch formats found: {invalid_batches}")
    print("All batches should be in W##/S##/F##/Sp## format")
    exit(1)

print(f"✅ Data validation passed: {len(batch_formats)} unique batches, all properly formatted")

with open('data/yc-embedded.json', 'w') as embeddings_file:
    json.dump(yc_companies, embeddings_file)

print("\n" + "="*50)
print("🔄 Running data validation...")
import subprocess
try:
    result = subprocess.run(['python', 'scripts/validate_data.py'], 
                          capture_output=True, text=True, cwd='.')
    print(result.stdout)
    if result.returncode != 0:
        print("❌ Data validation failed!")
        print(result.stderr)
    else:
        print("✅ Data generation and validation completed successfully!")
except FileNotFoundError:
    print("⚠️  Validation script not found - skipping validation")
print("="*50)

