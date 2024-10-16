import re
from collections import defaultdict
import chardet
import pandas as pd

# Detect encoding
with open('parcial_1339_comments_2.txt', 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(f"Detected encoding: {encoding}")

# Now read the file with the detected encoding
with open('parcial_1339_comments_2.txt', 'r', encoding=encoding) as file:
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

print(f'Number of users: {len(matches_1)}')
print(f'Number of comments: {len(matches_2)}')

# Create a DataFrame for all raw data
df_all_raw = pd.DataFrame({'Column 1': matches_1, 'Column 2': matches_2})

# Initialize data for unique_all and voted_9
unique_all_data = []
voted_9_data = []
wrong_match = []

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
        match_2 = matches_2[i]

        # Find numbers between 1 and 10
        pattern_number = r'\b(10|[1-9])\b'
        match_2 = re.search(pattern_number, match_2)

        try:
            match_2 = int(match_2.group(1))
            print(f"Found number for match_1 '{match_1}': {match_2}")  # Debugging output
            # Update count_dict
            count_dict[match_2] += 1
            unique_all_data.append((match_1, match_2))
        except:
            comment = match_2
            match_2 = 0  # Assign 0 if not found
            wrong_match.append((match_1, comment))

# Convert unique_all_data and voted_9_data to DataFrames
df_unique_all = pd.DataFrame(unique_all_data, columns=['Column 1', 'Column 2'])
df_voted_9 = pd.DataFrame(voted_9_data, columns=['Column 1', 'Column 2'])
df_wrong_match = pd.DataFrame(wrong_match, columns=['Column 1', 'Column 2'])

# Save all three DataFrames into an Excel file with multiple tabs
with pd.ExcelWriter('matches.xlsx') as writer:
    df_all_raw.to_excel(writer, sheet_name='all_raw', index=False)
    df_unique_all.to_excel(writer, sheet_name='unique_all', index=False)
    df_wrong_match.to_excel(writer, sheet_name='wrong match', index=False)

# Print the counts of unique match_2 occurrences
print("Counts of unique match_2 occurrences:")
for number in range(1, 11):  # Loop through numbers 1 to 10
    count = count_dict[number]  # Access count_dict using an integer
    print(f'Number {number} appears {count} time(s) (counted uniquely with match_1).')
