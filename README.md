# Wordle_Algorithm
A small algorithm that roughly predicts the next most likely word when playing the popular game "wordle".

Works by:

-Taking an input of the 5 letter word entered

-inputting numbers for each letter depending on the result in wordle, where:

      -1 = correct (green)
      
      -2 = correct in the wrong place (yellow)
      
      -0 = incorrect (grey)
      
      so for example, the word "ailed" might return ->Green(a), Yellow(i), Grey(l), Grey(e), Yellow(d)
      
      so you would enter "ailed", then "12002"

-The algorithm itself works by taking a word list and calculating the probability of a letter appearing in each spot, this gives a weight to each letter in each position

-Each word then has a commonality generated as the product of all of it's letter weighting, for example:

      - word "ailed"
      
      - a in 1st = 0.05 (5%)
      
      - i in 2nd = 0.02 (2%)
      
      - l in 3rd = 0.06 (6%)
      
      - e in 4th = 0.01 (1%)
      
      - d in 5th = 0.03 (3%)
       
      commonality of "ailed" = 0.05 * 0.02 * 0.06 * 0.01 * 0.03 = x

-The commonality of each word is calculated when the program is first ran, or can be calculated after each cycle, both work reasonably well.

-When a user enters a word into the algorithm, it generates a rule list of:
      -excluded letters (grey)
      -letters excluded at a specific point but included in the word as a whole (yellow)  
      -letters included at a specific point (green)

-these rules are then given to the narrowing function which reduces the size of the word list by filtering it through these rules.

-after that is done, the word list is ranked in order of commonality, with the most likely word being put forward.

- INPUT -> GENERATE RULES -> NARROW LIST -> CALCULATE COMMONALITY(or dont) -> RANK WORDS -> PROMPT USER

---
NOTES

This algorithm doesn't nescesarily solve for the most likely word, as this is somewhat impossible, as the word is functionally random.
However, it can decipher the most commonly structured word.
In doing this, the player is more likely to enter a word that has at least one correct letter (be it green or yellow)
This means that, if of the available words left to a user, 50% of them begin with an R, logically, your next word should begin with an R, and if of them, 50% had the next letter A, you should choose a word that goes RA.

This algorithm is quite crude, and does not work particularly well, but it is a lot faster than a human brain, and finds the word the majority of the time. I'm sure a statistician would have a word or two to say about my methods, but it was a fun and interesting exercise.
