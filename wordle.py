#system that will algorithmically determine the best wordle game, and the most likely next word

#we start with out starter word, whatever that may be, ideally the most statistically common word in the dictionary, with the most common letters

#we input the results, each letter will either be wrong, right, or right in the wrong place.
#based on this we create a new, narrower list with the new rules applied, so no words with x letters, must have y letter in z place, and must have q letters
#from here, we calculate the next most statistically common word, and try that one, then repeat

# input -> narrow -> common

#basically just fancy guesswork but it works

#will calculate the most statistically common word within a list
#*** issue: statistically common does not mean appears often, simply that it's letters are common, eerie for example has the most common letter 3 times but is not a very common word ***
def commonality_calc(word_list, commonality_weights):

    #based on the commonality weights, determines which words are more statistically common or not
    #this is calculated by taking the percentage chance of x letter appearing in y spot, and adding it to the running % total
    #([running % total] / 5)  gives us the average commonality of the word, the most common word is the next choice

    commonality_results = []

    for word in word_list:
        
        running_total = 0

        #for each letter in the word, using i here for convenience
        for i in range(5):
            
            letter = word[i]
            commonality_dict = commonality_weights[i]

            commonality = commonality_dict[letter]

            running_total += commonality

        #gives the word a final commonality score
        word_commonality = round((running_total / 5), 2)
        commonality_results.append((word, word_commonality))

    #simply ordering the results, bubble sort, don't need to pay much attention to this
    switch = True
    switch_count = 0
    while switch:
        for i in range(len(commonality_results) -1):
            try:
                
                current_p = commonality_results[i][1]
                next_p = commonality_results[i+1][1]
                
                if current_p < next_p:
                    temp = commonality_results[i]

                    commonality_results[i] = commonality_results[i+1]
                    commonality_results[i+1] = temp

                    switch_count += 1

            except:
                pass

        if switch_count == 0:
            switch = False
        else:
            switch_count = 0

    return commonality_results


#calculates and returns a weight list that associates each letters % chance of being present in each place of a word
def commonality_weight_calc(word_list):
    #tallies the amount of x letter found in y position of a word, saves it to a list of dictionaries
    #percentage appearance is calculated as: (appearences / length of list) * 100

    word_list_length = len(word_list)

    #these 5 dictionaries within the weights array will hold the alphabetical characters next to their appearences/% probability
    weights = [{}, {}, {}, {}, {}]
    
    #used to populate the weight dictionary
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    #populating the weight dictionary with default values
    for i in range(len(alphabet)):
        for j in range(5):
            weights[j][alphabet[i]] = 0
            j += 1
        i += 1


    #iterating through the word list and adding occurances
    for word in word_list:
        
        #for each letter in the word, using i here for ease
        for i in range(5):

            letter = word[i]

            #increments the weight
            weights[i][letter] += 1
            

    #converting to % 
    for dictionary in weights:
        
        for letter in alphabet:
            
            #calculates the percentage appearance
            dictionary[letter] = round(((dictionary[letter] / word_list_length) * 100), 2)

    return weights


#take a word, and its associated results taken from wordle
#this is done as -> word: ailed
#                -> rslt: 01201
#where 0 = incorrect, 1 = correct, and 2 = correct in wrong spot
#then returns the rule setas a dictionary: 
# rules{
#   exclude : [a, b, c]
#   include : [d, e, f]
#   include_at : [(g, 0), (h, 1), (i, 2)]
#}
def word_input(rules):
    print("0-grey, 1-green, 2-yellow")
    word    = input("word : ")
    results = input("rslt : ")

    if results == "11111":
        print("---Yippee!---")
        start()

    #generating the rules based on the results given
    for i in range(5):
        word_letter = word[i]
        new_rule = int(results[i])

        #letter is incorrect
        if new_rule == 0:

            include_at_check = False
            for rule in rules["include_at"]:
                if rule[0] == word_letter:
                    include_at_check = True

            if (word_letter not in rules["include"]) and (not include_at_check):
                rules["exclude"].append(word_letter)
        
        #letter is correct
        elif new_rule == 1:
            rules["include_at"].append((word_letter, i))

        #letter is correct but in the wrong place
        elif new_rule == 2:
            rules["include"].append(word_letter)
            rules["exclude_at"].append((word_letter, i))

    return rules


#according to the rules, removes items from the word list that do not fit the criteria
def narrow(word_list, rules):

    #------------
    #
    # add system to exclude false doubles, for example, word has 1 E, not 2, as we've tested against a second one
    # basically must have X of Y rule
    #
    #------------


    new_word_list = []

    exclude = rules["exclude"]
    include = rules["include"]
    include_at = rules["include_at"]
    exclude_at = rules["exclude_at"]

    valid_word = True

    #going through each word and applying the rules
    for word in word_list:

        #appling exclude    
        for letter in exclude:
            if letter in word:
                valid_word = False

        #applying include
        for letter in include:
            if letter not in word:
                valid_word = False

        #applying include_at
        for position in include_at:
            letter = position[0]
            i = position[1]

            if word[i] != letter:
                valid_word = False

        #applying exclude_at
        for position in exclude_at:
            letter = position[0]
            i = position[1]

            if word[i] == letter:
                valid_word = False
        
        #if the valid word toggle has not been flipped, it appends the word to the new list
        if valid_word:
            new_word_list.append(word)
        
        valid_word = True

    return new_word_list


def start():
    #read the word list file to get our first wordlist, and some basic formatting to prevent weirdness
    with open("extended_list.txt", "r") as file:
        word_list = []
        for line in file:
            word_list.append(line.strip())

    print("---word list parsed---")

    #calculate out commonality data
    commonality_weights = commonality_weight_calc(word_list)

    print("---weights calculated---")

    rules = {
        "exclude"    : [],
        "include_at"    : [],
        "include" : [],
        "exclude_at" :  []
    }

    print("---blank ruleset set---")
    print()

    #simply loops so we know what to do
    while True:
        print("=====================================================")
        #takes input and generates our rules
        rules = word_input(rules)

        #---debug code that shows the rule set---
        print("exclude    : " + str(rules["exclude"]))
        print("include    : " + str(rules["include"]))
        print("include_at : " + str(rules["include_at"]))
        print("exclude_at : " + str(rules["exclude_at"]))

        #updates the wordlist
        word_list = narrow(word_list, rules)

        #for word in word_list:
        #    print(word)

        #recalculating our commonality weights after each run
        try:
            commonality_weights = commonality_weight_calc(word_list)
        except:
            print(word_list)
            print("error - no possible words")
        


        #calculates the most common word
        results = commonality_calc(word_list, commonality_weights)

        print("---TOP 5---")
        for i in range(5):
            #in a try catch in case there are less than 5 possibilities
            try:
                result = results[i]
                word = result[0]
                avg_commonality = result[1]
                print(word + " | " + str(avg_commonality) + "%")
            except:
                pass

start()