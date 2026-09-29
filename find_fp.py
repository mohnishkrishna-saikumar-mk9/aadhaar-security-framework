import pandas as pd
from authentication.fingerprint_pad import FingerprintPAD

pad = FingerprintPAD()
df = pd.read_csv('D:/7th Semester/Information Security/aadhaar_dataset.csv')

for idx, row in df[df['fingerprint_label'] == 'Real'].head(20).iterrows():
    res = pad.detect_liveness(row['fingerprint_path'])
    if res['status'] == 'GENUINE':
        print(f"Row {idx+1}: Name: {row['name']}, Aadhaar: {row['aadhaar_number']}")
        print(f"  Face: {row['face_path']}")
        print(f"  Fingerprint: {row['fingerprint_path']}")
        break
