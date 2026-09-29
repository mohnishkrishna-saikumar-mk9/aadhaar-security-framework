import sqlite3
import os
import pandas as pd
import random

BASE_DIR = r"D:\7th Semester\Information Security\aadhaar-inspired-security"
DB_PATH = os.path.join(BASE_DIR, "database", "identity_system.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")
METADATA_PATH = os.path.join(BASE_DIR, "data", "metadata", "identities.csv")

def init_db():
    # Remove existing db to start fresh
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Execute schema
    with open(SCHEMA_PATH, 'r') as f:
        cursor.executescript(f.read())
        
    print("Database schema created.")
    
    # Populate initial identities
    df = pd.read_csv(METADATA_PATH)
    
    identities_data = []
    demo_details_data = []
    seen_hashes = set()
    
    for _, row in df.iterrows():
        identity_id = row['identity_id']
        credential_hash = row['credential_hash']
        
        if credential_hash in seen_hashes:
            continue
            
        seen_hashes.add(credential_hash)
        identities_data.append((identity_id, credential_hash))
        
        # Create synthetic demo details
        demo_details_data.append((
            identity_id,
            f"Demo User {identity_id}",
            random.randint(18, 70),
            random.choice(["M", "F"]),
            "ACTIVE",
            "VERIFIED"
        ))
        
    # Insert identities
    cursor.executemany(
        "INSERT INTO identity (identity_id, credential_hash) VALUES (?, ?)", 
        identities_data
    )
    
    # Insert demo details
    cursor.executemany(
        "INSERT INTO demo_details (identity_id, name, age, gender, service_status, verification_status) VALUES (?, ?, ?, ?, ?, ?)",
        demo_details_data
    )
    
    conn.commit()
    conn.close()
    print(f"Populated {len(identities_data)} identities into the database.")

if __name__ == "__main__":
    init_db()
