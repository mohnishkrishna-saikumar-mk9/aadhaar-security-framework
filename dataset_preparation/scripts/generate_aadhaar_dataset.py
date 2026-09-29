import pandas as pd
import random
import hashlib
import os

def generate_random_aadhaar():
    """Generates a random 12-digit Aadhaar number as a string."""
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

def hash_aadhaar(aadhaar_number):
    """Returns the SHA-256 hash of the given Aadhaar number."""
    return hashlib.sha256(aadhaar_number.encode('utf-8')).hexdigest()

def main():
    source_file = "face_fingerprint_dataset.csv"
    output_file = "aadhaar_dataset.csv"
    total_rows = 14780
    
    if not os.path.exists(source_file):
        print(f"[ERROR] Source file {source_file} not found!")
        return
        
    print(f"Reading demographics from {source_file}...")
    df_source = pd.read_csv(source_file)
    
    # Separate by gender
    males = df_source[df_source['gender'] == 'Male'].copy().sample(frac=1).reset_index(drop=True)
    females = df_source[df_source['gender'] == 'Female'].copy().sample(frac=1).reset_index(drop=True)
    
    print(f"Available Males: {len(males)}, Available Females: {len(females)}")
    
    # We need exactly 3695 for each of the 4 combinations
    required_per_group = total_rows // 4  # 3695
    
    # Pick the exact individuals (allow replacement since we are short ~46 females)
    sampled_males = males.sample(n=required_per_group*2, replace=True).reset_index(drop=True)
    sampled_females = females.sample(n=required_per_group*2, replace=True).reset_index(drop=True)
    
    real_males = sampled_males.iloc[0:required_per_group].copy()
    fake_males = sampled_males.iloc[required_per_group:required_per_group*2].copy()
    
    real_females = sampled_females.iloc[0:required_per_group].copy()
    fake_females = sampled_females.iloc[required_per_group:required_per_group*2].copy()
    
    # Combine real and fake sets
    real_set = pd.concat([real_males, real_females])
    fake_set = pd.concat([fake_males, fake_females])
    
    # Assign Real Aadhaar Features
    real_set['aadhaar_number'] = [generate_random_aadhaar() for _ in range(len(real_set))]
    real_set['hashkey'] = real_set['aadhaar_number'].apply(hash_aadhaar)
    real_set['label'] = 'Real'
    
    # Assign Fake Aadhaar Features
    fake_set['aadhaar_number'] = [generate_random_aadhaar() for _ in range(len(fake_set))]
    # Generate a completely wrong hash for fake
    fake_set['hashkey'] = [hash_aadhaar(generate_random_aadhaar()) for _ in range(len(fake_set))]
    fake_set['label'] = 'Fake'
    
    # Combine final dataset
    final_df = pd.concat([real_set, fake_set])
    
    def format_path(user_no, folder):
        num_padded = str(int(user_no.replace('U', ''))).zfill(5)
        return f"D:\\7th Semester\\Information Security\\face-fingerprint-dataset\\{folder}\\{num_padded}.jpg"
        
    final_df['fingerprint_path'] = final_df['user_no'].apply(lambda x: format_path(x, 'fingerprint'))
    final_df['face_path'] = final_df['user_no'].apply(lambda x: format_path(x, 'face'))
    
    # Keep only the relevant columns in the requested order (paths at the end)
    final_df = final_df[['name', 'age', 'gender', 'address', 'aadhaar_number', 'hashkey', 'label', 'fingerprint_path', 'face_path']]
    
    # Shuffle perfectly
    final_df = final_df.sample(frac=1).reset_index(drop=True)
    
    # Save to CSV
    final_df.to_csv(output_file, index=False)
    
    print(f"\nSuccessfully generated {len(final_df)} rows and saved to {output_file}")
    print("\n--- Distribution Verification ---")
    print(final_df.groupby(['label', 'gender']).size())

if __name__ == "__main__":
    main()
