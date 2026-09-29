"""
Update aadhaar_dataset.csv with SOCOFing fingerprints.
- Use 7390 Real fingerprints (6000 original + 1390 duplicated)
- Use 7390 Fake fingerprints (from Altered-Hard)
- Overwrite `fingerprint_path` and add `fingerprint_label` column.
- Balance perfectly across the 4 main groups (Aadhaar Real/Fake x Gender).
"""

import os
import random
import pandas as pd

CSV_PATH = r"D:\7th Semester\Information Security\aadhaar_dataset.csv"
REAL_DIR = r"D:\7th Semester\Information Security\SOCOFing\Real"
FAKE_DIR = r"D:\7th Semester\Information Security\SOCOFing\Altered\Altered-Hard"

random.seed(42)

# Load Real fingerprints
real_files = sorted([f for f in os.listdir(REAL_DIR) if f.endswith('.BMP')])
# Duplicate 1390 random images
real_duplicates = random.choices(real_files, k=1390)
real_paths = [os.path.join(REAL_DIR, f) for f in real_files + real_duplicates]
random.shuffle(real_paths)
print(f"Total Real fingerprints ready: {len(real_paths)}")

# Load Fake fingerprints
fake_files = sorted([f for f in os.listdir(FAKE_DIR) if f.endswith('.BMP')])
fake_paths = [os.path.join(FAKE_DIR, f) for f in random.sample(fake_files, 7390)]
print(f"Total Fake fingerprints ready: {len(fake_paths)}")

df = pd.read_csv(CSV_PATH)
df['fingerprint_label'] = 'Real'  # Default

real_idx = 0
fake_idx = 0

# Balance counts: (Real_count, Fake_count) for each group
group_balances = {
    ('Real', 'Male'): (1847, 1848),
    ('Real', 'Female'): (1848, 1847),
    ('Fake', 'Male'): (1847, 1848),
    ('Fake', 'Female'): (1848, 1847),
}

for (label, gender), (r_count, f_count) in group_balances.items():
    mask = (df['label'] == label) & (df['gender'] == gender)
    indices = df[mask].index.tolist()
    
    # Shuffle indices so assignment is random within the group
    random.shuffle(indices)
    
    # Assign Real
    for i in range(r_count):
        idx = indices[i]
        df.at[idx, 'fingerprint_path'] = real_paths[real_idx]
        df.at[idx, 'fingerprint_label'] = 'Real'
        real_idx += 1
        
    # Assign Fake
    for i in range(r_count, r_count + f_count):
        idx = indices[i]
        df.at[idx, 'fingerprint_path'] = fake_paths[fake_idx]
        df.at[idx, 'fingerprint_label'] = 'Fake'
        fake_idx += 1

df.to_csv(CSV_PATH, index=False)

print("\n=== COMPLETE! ===")
print("New Label Distribution:")
print(df.groupby(['label', 'gender', 'fingerprint_label']).size().to_string())
print(f"\nTotal Real assigned: {real_idx}")
print(f"Total Fake assigned: {fake_idx}")
