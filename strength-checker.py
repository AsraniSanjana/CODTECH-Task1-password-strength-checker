import os
import re
import calendar

def find_matching_substrings(substrings, password):
    matches = []
    for substring in substrings:
        if len(substring) >= 3 and substring.lower() in password.lower():
            matches.append(substring)
    return matches

def generate_substrings(text, min_length=3):
    substrings = set()
    length = len(text)
    for i in range(length):
        for j in range(i + min_length, length + 1):
            substrings.add(text[i:j])
    return substrings

def generate_reverse_substrings(text, min_length=4):
    substrings = set()
    length = len(text)
    for i in range(length):
        for j in range(i + min_length, length + 1):
            substrings.add(text[i:j][::-1])
    return substrings

def generate_dob_combinations(dob):
    # Assuming dob is in the format DDMMYYYY
    day = dob[:2]
    month = dob[2:4]
    year = dob[4:]
    
    dob_combinations = set()
    
    # Different combinations of DOB
    dob_combinations.add(year)
    dob_combinations.add(month)
    dob_combinations.add(day)
    dob_combinations.add(year + month)
    dob_combinations.add(month + day)
    dob_combinations.add(year + day)
    dob_combinations.add(year + month + day)
    dob_combinations.add(day + month + year)
    
    # Add month name
    month_name = calendar.month_name[int(month)].lower()
    dob_combinations.add(month_name)
    
    return dob_combinations

def is_password_in_dictionary(password, dictionary_file):
    with open(dictionary_file, 'r') as file:
        common_passwords = file.read().splitlines()
    password_length = len(password)
    all_matches = []
    
    # Check if dictionary file exists for the given password length
    if os.path.exists(dictionary_file):
        for word in common_passwords:
            substrings = generate_substrings(word, password_length)
            matching_substrings = find_matching_substrings(substrings, password)
            if matching_substrings:
                all_matches.extend(matching_substrings)
    
    if all_matches:
        return all_matches, len(all_matches) * 2
    return [], 0

def is_password_in_combinations(password, filenames):
    all_matches = []
    password_length = len(password)
    # print(password_length)
    
    # Check if combination files exist for the given password length
    for filename in filenames:
        # Extract the expected length from the filename
        match = re.search(r'length(\d+)-', filename)
        # print(match)
        if match:
            expected_length = int(match.group(1))
            if password_length == expected_length and os.path.exists(os.path.join('txt files', filename)):
                with open(os.path.join('txt files', filename), 'r') as file:
                    combinations = file.read().splitlines()
                for combo in combinations:
                    substrings = generate_substrings(combo, password_length)
                    matching_substrings = find_matching_substrings(substrings, password)
                    if matching_substrings:
                        all_matches.extend(matching_substrings)
    
    if all_matches:
        return all_matches, len(all_matches) * 2
    return [], 0

def calculate_password_strength(password, full_name, dob, pet_name, filenames):
    score = 15
    explanations = []

    # Check substrings of full name
    if full_name:
        substrings = generate_substrings(full_name, 5)
        reverse_substrings = generate_reverse_substrings(full_name)
        matching_substrings = find_matching_substrings(substrings, password)
        if matching_substrings:
            score -= 4
            explanations.append(f"contains substrings of the full name: {', '.join(matching_substrings)}")
        else:
            matching_substrings = find_matching_substrings(reverse_substrings, password)
            if matching_substrings:
                score -= 4
                explanations.append(f"contains reverse substrings of the full name: {', '.join(matching_substrings)}")

    # Check combinations of DOB
    if dob:
        dob_combinations = generate_dob_combinations(dob)
        matching_substrings = find_matching_substrings(dob_combinations, password)
        if matching_substrings:
            score -= 4
            explanations.append(f"contains combinations of the DOB: {', '.join(matching_substrings)}")

    # Check pet's name directly in password
    if pet_name and pet_name.lower() in password.lower():
        score -= 2
        explanations.append(f"contains the pet's name '{pet_name}'")

    # Check if password is in dictionary
    dictionary_file = os.path.join('txt files', 'dictionary.txt')
    matching_substrings, deduction = is_password_in_dictionary(password, dictionary_file)
    if matching_substrings:
        # score -= deduction
        score -= 2
        explanations.append(f"matches common passwords in dictionary: {', '.join(matching_substrings)}")

    # Check if password is in specified combination files
    combination_files = []
    password_length = len(password)
    
    # Construct filenames based on password length
    for filename in filenames:
        combination_files.append(filename)
    
    matching_substrings, deduction = is_password_in_combinations(password, combination_files)
    if matching_substrings:
        score -= deduction
        explanations.append(f"matches words in combination files: {', '.join(matching_substrings)} and deducted {deduction} points")

    # Check password length and deduct points for lengths less than 5
    if len(password) < 5:
        score = 5
        explanations.append(f"password length is less than 5")

    # Ensure final score is within range of 0 to 15
    score = max(0, min(15, score))
    
    return score, explanations

def read_demographics(filename='demographics.txt'):
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
    demographics = {}
    for line in lines:
        if ': ' in line:
            key, value = line.split(': ', 1)
            demographics[key.lower()] = value
    return demographics

def main():
    # Read demographics from file
    demographics = read_demographics(os.path.join('txt files', 'demographics.txt'))
    
    full_name = demographics.get('full name', '')
    dob = demographics.get('dob', '').replace('.', '')
    pet_name = demographics.get('pets name', '')

    # Input password from user
    password = input("Enter the password: ")
    
    # Define the combination filenames
    combination_files = [
        'length4-AlphaCombinations.txt',
        'length4-NumericCombinations.txt',
        'length5-AlphaCombinations.txt',
        'length5-NumericCombinations.txt'
    ]
    
    # Calculate the password strength
    score, explanations = calculate_password_strength(password, full_name, dob, pet_name, combination_files)
    
    # Print the results
    print(f"Final score: {score}/15")
    for explanation in explanations:
        print(explanation)

if __name__ == "__main__":
    main()
