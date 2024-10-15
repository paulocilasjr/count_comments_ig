import re
from collections import defaultdict
import chardet
import pandas as pd

# Detect encoding
with open('parcial_1309_comments.txt', 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(f"Detected encoding: {encoding}")

# Now read the file with the detected encoding
with open('parcial_1309_comments.txt', 'r', encoding=encoding) as file:
    text = file.read()
    print("File is loaded")

# Create a regular expression pattern for the first match
pattern_1 = r'<span class="_ap3a _aaco _aacw _aacx _aad7 _aade" dir="auto">(.*?)</span>'
# Create a regular expression pattern for the second match
pattern_2 = r'18px;">([^<]+?)</span></div></div>'

# Find all matches for both patterns
matches_1 = re.findall(pattern_1, text)
matches_2 = re.findall(pattern_2, text)

# Remove 'dallmgamesstudio' from matches_1
matches_1 = [match for match in matches_1 if match != 'dallmgamesstudio']

print(f'number of users: {len(matches_1)}')

# Create a DataFrame for all raw data
df_all_raw = pd.DataFrame({'Column 1': matches_1, 'Column 2': matches_2})
print(df_all_raw)
print("saving csv")

# Initialize data for unique_all and voted_9
unique_all_data = []
voted_9_data = []

# Initialize a dictionary to count occurrences
count_dict = defaultdict(int)
unique_matches_1 = set()  # To track unique match_1 values

# Iterate using index
for i in range(len(matches_1)):
    match_1 = matches_1[i]
    
    # Check if match_1 is unique
    if match_1 not in unique_matches_1:
        # Add match_1 to the set of unique matches
        unique_matches_1.add(match_1)

        # Get the corresponding match_2 based on index
        match_2 = matches_2[i] if i < len(matches_2) else None

        # Check if match_2 is valid and contains a number from 1 to 10
        if match_2 and match_2.isdigit() and 1 <= int(match_2) <= 10:
            count_dict[match_2] += 1
            unique_all_data.append((match_1, match_2))  # Add to unique_all_data

            # Additional check for match_2 == 9
            if int(match_2) == 9:
                voted_9_data.append((match_1, match_2))  # Add to voted_9_data

# Convert unique_all_data and voted_9_data to DataFrames
df_unique_all = pd.DataFrame(unique_all_data, columns=['Column 1', 'Column 2'])
df_voted_9 = pd.DataFrame(voted_9_data, columns=['Column 1', 'Column 2'])

# Save all three DataFrames into an Excel file with multiple tabs
with pd.ExcelWriter('matches.xlsx') as writer:
    df_all_raw.to_excel(writer, sheet_name='all_raw', index=False)
    df_unique_all.to_excel(writer, sheet_name='unique_all', index=False)
    df_voted_9.to_excel(writer, sheet_name='voted_9', index=False)

# Print the counts of unique match_2 occurrences
print("Counts of unique match_2 occurrences:")
for number in range(1, 11):  # Loop through numbers 1 to 10
    count = count_dict[str(number)]  # Convert number to string for lookup
    print(f'Number {number} appears {count} time(s) (counted uniquely with match_1).')
