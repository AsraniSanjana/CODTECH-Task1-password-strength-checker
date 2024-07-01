# n=4, each of the 4 places can have 26 choices, so it would be 26*26*26*26 = 456,976 possible combinations of words.
import os

from itertools import product

def generate_combinations(length):
    # Define the alphabet
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    # Generate all combinations with repetition of the given length
    combos = product(alphabet, repeat=length)
    
    # Convert each combination tuple to a string
    combos = [''.join(c) for c in combos]
    
    return combos

def save_combinations_to_file(combinations, filename):
    with open(filename, 'w') as f:
        for combination in combinations:
            f.write(combination + '\n')

def main():
    # Input length from user
    length = int(input("Enter the desired length: "))
    
    # Generate the combinations
    combinations = generate_combinations(length)
    
    # Save to file
    filename = os.path.join("txt files", f'length{length}-AlphaCombinations.txt')
    save_combinations_to_file(combinations, filename)
    
    print(f"Generated {len(combinations)} combinations and saved to '{filename}'")

if __name__ == "__main__":
    main()
