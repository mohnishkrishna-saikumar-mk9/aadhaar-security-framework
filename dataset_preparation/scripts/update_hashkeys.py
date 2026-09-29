import pandas as pd
import hashlib

CSV_PATH = r"D:\7th Semester\Information Security\aadhaar_dataset.csv"

print("Loading dataset...")
df = pd.read_csv(CSV_PATH)

print("Updating hashkey column based on the new Aadhaar numbers...")
new_hashes = []
for idx, row in df.iterrows():
    # Get the new aadhaar number as string
    aadhaar_str = str(row['aadhaar_number'])
    
    # Calculate SHA-256
    hash_obj = hashlib.sha256(aadhaar_str.encode())
    credential_hash = hash_obj.hexdigest()
    
    new_hashes.append(credential_hash)

df['hashkey'] = new_hashes

print("Saving updated dataset with correct hash keys...")
df.to_csv(CSV_PATH, index=False)
print("Done. Hash keys updated successfully.")
