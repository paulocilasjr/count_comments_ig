
import re
from collections import defaultdict
import chardet

# Detect encoding
with open('comments_ig.txt', 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(f"Detected encoding: {encoding}")

# Now read the file with the detected encoding
with open('comments_ig.txt', 'r', encoding=encoding) as file:
    text = file.read()
    print("File is loaded")

# Create a regular expression pattern for the first match
pattern_1 = r'<span class="_ap3a _aaco _aacw _aacx _aad7 _aade" dir="auto">(.*?)</span>'
# Create a regular expression pattern for the second match
pattern_2 = r'18px;">([^<]+?)</span></div></div>'

print("Pattern loaded")

# Find all matches for both patterns
matches_1 = re.findall(pattern_1, text)
matches_2 = re.findall(pattern_2, text)

# Remove 'dallmgamesstudio' from matches_1
matches_1 = [match for match in matches_1 if match != 'dallmgamesstudio']

# Print the number of matches found
print(f'Number of matches_1: {len(matches_1)}')
print(f'Number of matches_2: {len(matches_2)}')

# Confirm that the number of matches is equal
if len(matches_1) == len(matches_2):
    print("The number of matches_1 is equal to the number of matches_2.")
else:
    print("The number of matches_1 is NOT equal to the number of matches_2.")

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

# Print the counts of unique match_2 occurrences
print("Counts of unique match_2 occurrences:")
for number in range(1, 11):  # Loop through numbers 1 to 10
    count = count_dict[str(number)]  # Convert number to string for lookup
    print(f'Number {number} appears {count} time(s) (counted uniquely with match_1).')

