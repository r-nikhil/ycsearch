import json
from sentence_transformers import SentenceTransformer

# works with JSON sourced from https://github.com/akshaybhalotia/yc_company_scraper

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

with open('data/yc.json', 'r') as yc_file:
    yc_companies_raw = json.load(yc_file)
    
    # Deduplicate by slug, keeping the first occurrence
    seen_slugs = set()
    yc_companies = []
    for co in yc_companies_raw:
        if co['slug'] not in seen_slugs:
            seen_slugs.add(co['slug'])
            yc_companies.append(co)
    
    print(f'Deduplicated: {len(yc_companies_raw)} → {len(yc_companies)} companies')
    
    for i, co in enumerate(yc_companies):
        print(f'{i}/{len(yc_companies)}', co['name'])
        description = co.get('long_description') or co.get('one_liner')
        if not description:
            print(f'{co["name"]} has no long_description or one_liner, skipping semantic indexing')
            continue
        embedding = model.encode(description.strip())
        co['description_embedding'] = embedding.tolist()

    with open('data/yc-embedded.json', 'w') as embeddings_file:
        json.dump(yc_companies, embeddings_file)

