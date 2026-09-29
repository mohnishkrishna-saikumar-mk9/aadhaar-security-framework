import pandas as pd
import random
from collections import Counter

CSV_PATH = r"D:\7th Semester\Information Security\aadhaar_dataset.csv"

def generate_valid_aadhaar():
    while True:
        # Generate 12 random digits
        first_digit = str(random.randint(1, 9))
        remaining = "".join([str(random.randint(0, 9)) for _ in range(11)])
        num_str = first_digit + remaining
        
        # Check that no digit appears more than 2 times
        counts = Counter(num_str)
        if all(count <= 2 for count in counts.values()):
            return num_str

print("Loading dataset...")
df = pd.read_csv(CSV_PATH)

print("Generating new realistic Aadhaar numbers...")
# We need to maintain uniqueness for identities if possible, but the user just asked for valid formats.
# Let's generate a unique set of Aadhaar numbers
unique_numbers = set()
while len(unique_numbers) < len(df):
    unique_numbers.add(generate_valid_aadhaar())

new_aadhaar_list = list(unique_numbers)
random.shuffle(new_aadhaar_list)

df['aadhaar_number'] = new_aadhaar_list

print("Saving updated dataset...")
df.to_csv(CSV_PATH, index=False)
print("Done. All Aadhaar numbers have been updated to realistic 12-digit values.")
