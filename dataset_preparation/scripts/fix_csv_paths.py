import pandas as pd
import os

CSV_PATH = r"D:\7th Semester\Information Security\aadhaar_dataset.csv"

# Load the CSV
df = pd.read_csv(CSV_PATH)

# Helper function to correct paths to point inside dataset_preparation/sources
def fix_path(path):
    if not isinstance(path, str):
        return path
        
    # Replace old paths with the new location
    # Replace SOCOFing
    if "Information Security\\SOCOFing" in path:
        path = path.replace("Information Security\\SOCOFing", "Information Security\\dataset_preparation\\sources\\SOCOFing")
    
    # Replace face-fingerprint-dataset
    if "Information Security\\face-fingerprint-dataset" in path:
        path = path.replace("Information Security\\face-fingerprint-dataset", "Information Security\\dataset_preparation\\sources\\face-fingerprint-dataset")
        
    # Replace stylegan_faces
    if "Information Security\\stylegan_faces" in path:
        path = path.replace("Information Security\\stylegan_faces", "Information Security\\dataset_preparation\\sources\\stylegan_faces")
        
    return path

# Apply the fix to the path columns
df['face_path'] = df['face_path'].apply(fix_path)
df['fingerprint_path'] = df['fingerprint_path'].apply(fix_path)

# Save the updated CSV
df.to_csv(CSV_PATH, index=False)
print("CSV paths updated successfully.")
print(df[['face_path', 'fingerprint_path']].head(2).values)
