# CODTECH-Task1-password-strength-checker

✅ Instructions to run this code:

💠 guess-pswd_only-alpha.py 
generates the txt files of all possible combinations of alphabets for the inputted length. eg.: length3-AlphaCombinations.txt
(UNREPEATED)

similarly, 
💠 guess-pswd_only-numeric.py 
generates the txt files of all possible combinations of numbers for the inputted length. eg.: length3-NumericCombinations.txt

the words in these txt files are checked to be the part of the password.

。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。

🔵 The pswd strength is calculated on the basis of:

1🔹 personal details provided like dob, name, pet's name

i.e. for eg. 
if name or reversed name or substring of them is in pswd: score-4
dob is part of pswd: score-4
if pet name is in pswd: score-2

2🔹 pswd is found in all potential combinations generated files: score-2

3🔹 pswd is in dictionary: score-2

4🔹 length is too small (less than 5): score=5
。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。

➡️ Out of a maximum score of 15, based on these conditions, the calculated score signifying the pswd strength is printed.
