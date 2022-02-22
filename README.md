# worleSolver

This is a quick program written to help me cheat at guessing wordle words. The interface is pretty clunky, and the wordlist still includes words that aren't valid guesses. Future improvements will probably be made to improve the algorithm and have a web based display interface. Most words can be guessed within 4 tries using exclusively guesses from the top 10 list of words generated.

Frequency table for number of guess required to guess a randomly generated word out of the 11430 5 letter words in the language. There was a total of 1000 simulations of guessing words run to get this data.
 2 :   21
 3 :   152
 4 :   337
 5 :   237
 6 :   132
 7 :   80
 8 :   22
 9 :   6
 10 :  10
 11 :  2
 13 :  1

 In this trial 87.9% of all words we guessed within 6 attempts. The guesses were taken from the top of the list of remaining words ordered by the common letter score that was generated from the remaining list of words after each guess. Each initial guess was the word "cares" which has the highest cl_score out of the initial list. I don't have a full list of the guesses done for each test, but in my experience with manual testing, high guess counts are probably a result of getting common suffixes guessed ("-are","-res"), and having to go through a large amount of words for the last few letters. It may be that using an initial guess that tends to have a really popular letter structure actually reduces accuracy since it further emphasizes this common suffix/prefix issue. 
