from numpy import NaN
import pandas as pd
import random

##CSV based on wordlist found online. Data could be improved by adding in relative frequency of each
## word being used in regular speech
words = pd.read_csv("words.csv")

global l1_values
global l2_values
global l3_values
global l4_values
global l5_values

l1_values = words["L1"].value_counts()
l2_values = words["L2"].value_counts()
l3_values = words["L3"].value_counts()
l4_values = words["L4"].value_counts()
l5_values = words["L5"].value_counts()

# calculates common letter score. This is the measure of how much a letter in a given position appears
#Could implement dynamicly changing value counts in the function so after every guess the values updates
# also could be done with a loop probably
def calculate_CL_Score(row):
    #probably a better way to do this without an array, but hey it works!
    cl_array = []
    cl_array.append(l1_values.loc[row["L1"]])
    cl_array.append(l2_values.loc[row["L2"]])
    cl_array.append(l3_values.loc[row["L3"]])
    cl_array.append(l4_values.loc[row["L4"]])
    cl_array.append(l5_values.loc[row["L5"]])

    #This removes score for double letters. Without this it tends to overrate double letter words
    if row["double"] == True:
        d_l = double_index(row["word"])
        cl_array[d_l] = cl_array[d_l]/2

    return sum(cl_array)

#first guess should not include double letters, double letter category is added
def calc_double(str):
    double_letter = False
    for i in range(0,len(str)):
        for j in range(i+1, len(str)):
            if str[i] == str[j]:
                double_letter = True

    return double_letter

# finds the index of the second double letter. I didn't want to put this in the above function and
# mess with the lambda function
def double_index(str):
    double = NaN
    for i in range(0,len(str)):
        for j in range(i+1, len(str)):
            if str[i] == str[j]:
                double = str[i]
                return j

    return -1

#one of these is definitely redundant
def not_contains(str, c):
    if c in str:
        return False
    else:
        return True

def contains(str, c):
    if c in str:
        return True
    else:
        return False


words["double"] = words.apply(lambda row: calc_double(row["word"]), axis=1) 

words["cl_score"] = words.apply(lambda row: calculate_CL_Score(row), axis=1)

no_double = words[words["double"]==False]

#word is just the word guessed. Letter status is an array displaying which letters are in which position
#letter_status: [y,g,r,r,y]
# g=letter is in the right position
# y=letter in the word but wrong position
# r=letter not in word
def guessCheck(word, letter_status, guess_df):
    words_cp = guess_df
    for i in range(0,len(letter_status)):
        col_name = "L" + str(i+1)

        if letter_status[i] == "g":
            words_cp = words_cp[words_cp[col_name] == word[i]]
        elif letter_status[i] == "y":
            words_cp = words_cp[words.apply(lambda row: contains(row["word"],word[i]), axis=1)]
            words_cp = words_cp[words_cp[col_name] != word[i]]
        else:
            #don't remove double letters if they come back grey
            words_cp = words_cp[words.apply(lambda row: not_contains(row["word"],word[i]), axis=1)]

    return words_cp

#function that tries to take as many letters out of the pool as possible
# currently the main guess function tends to get stuck on finding every letter in the right place
# this can lead to a situation where there are more options than guesses
def elim_letters(word, letter_status, guess_df):
    words_cp = guess_df
    for i in range(0,len(letter_status)):
        col_name = "L" + str(i+1)

        if letter_status[i] == "g":
            words_cp = words_cp[words_cp[col_name] == word[i]]
        elif letter_status[i] == "y":
            words_cp = words_cp[words_cp[col_name] != word[i]]
        else:
            #don't remove double letters if they come back grey
            words_cp = words_cp[words.apply(lambda row: not_contains(row["word"],word[i]), axis=1)]
    #will need to change. Don't want to permenantly eliminate double letters
    return words_cp

guess = words
quit = False


while quit == False:

    word_guess = input("Enter word guessed: ")

    if word_guess == "complete":
        guess = words
        continue

    if word_guess == "QUIT":
        quit = True
        break

    status = input("Enter letter status: ")
    status_array = []

    guessType =  0 #int(input("Enter Guess Type (0 for guessing word. 1 for elimnating letters): "))

    for i in status: ##could be changed to a list cast
        status_array.append(i)
    if guessType == 0:
        guess = guessCheck(word_guess,status_array,guess)
        #code used to change cl_score based on remaining words
        #gives higher priority to letters 
        l1_values = guess["L1"].value_counts()
        l2_values = guess["L2"].value_counts()
        l3_values = guess["L3"].value_counts()
        l4_values = guess["L4"].value_counts()
        l5_values = guess["L5"].value_counts()

        guess.drop('cl_score', inplace=True, axis=1)
        guess["cl_score"] = guess.apply(lambda row: calculate_CL_Score(row), axis=1)
    else:
        guess = elim_letters(word_guess,status_array,guess)

    possible_guess = guess.sort_values("cl_score",ascending=False).head(10)
    #print(guess.sort_values("cl_score",ascending=False).head(10))
    print(possible_guess["word"].head(10))
    print("Total Possible words: " + str(len(guess.index)))

def test_letter_status(guess_word,correct_word):
    status = ""

    for i in range(0,len(guess_word)):
        if guess_word[i] == correct_word[i]:
            status += "g"
        elif contains(correct_word,guess_word[i]):
            status += "y"
        else:
            status += "r"

    return status

def test_Eff(guess_df):
    guess = guess_df
    index = random.randint(0, 11429)
    correct_word = guess_df.at[index,"word"]
    guess_word = "cares" #guess_df.at[random.randint(0, 11429),"word"]
    guess_num = 0
    correct = False

    while correct == False:
        if(guess_num == 20): correct = True
        status = test_letter_status(guess_word,correct_word)

        #print("guess: " + str(guess_num) + " " +  guess_word + " " + correct_word)

        if status == "ggggg":
            correct = True
        guess = guessCheck(guess_word,status,guess)

        l1_values = guess["L1"].value_counts()
        l2_values = guess["L2"].value_counts()
        l3_values = guess["L3"].value_counts()
        l4_values = guess["L4"].value_counts()
        l5_values = guess["L5"].value_counts()

        guess.drop('cl_score', inplace=True, axis=1)
        guess["cl_score"] = guess.apply(lambda row: calculate_CL_Score(row), axis=1)
        guess = guess.sort_values("cl_score",ascending=False)
        guess_word = guess.iloc[0,0]
        guess_num += 1
    return guess_num

# freq = {}

# for i in range(0,1000):
#     guess_num = test_Eff(guess)
#     if (guess_num in freq):
#         freq[guess_num] += 1
#     else:
#         freq[guess_num] = 1

# for key, value in freq.items():
#     print ("% d : % d"%(key, value))