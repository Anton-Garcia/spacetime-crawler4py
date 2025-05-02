import sys
import string

#this is the list of all alpha-numeric characters
ALPHANUM = list(string.ascii_letters + string.digits)

'''
This function runs in linear time:
This function is a replacement for regex's split function, where we are splitting on each
non-alphanumeric character. Each char is only looked at once, and checking if the char is
in the ALHANUM array is an O(1) operation. Appending strings is O(m), but since m, the length
of the longest sequence in the line, is most likely upper bounded by n, the number of chars
in the line, we say that the function runs in O(n) time, where n is the number of chars in
the line.
'''
def split(line):
    word_array = []
    curr_word = ""
    #iterate through all characters
    for character in line:
        #if the character is alphanumeric, add it to the current word
        if(character in ALPHANUM):
            curr_word += character

        #if the character is not alphanumeric, add the current word to the array and reset
        else:
            if(curr_word != ""):
                word_array.append(curr_word)
                curr_word = ""

    #catch the last word when you hit end of line
    if(curr_word != ""):
        word_array.append(curr_word)

    return word_array

'''
This function runs in linear time:
Each line in the file is visited once, and each character in the line is looked at once.
The split function runs in O(m) time, where m is the number of characters per line,
which is upper bounded by (or equal to) the number of characters in the file. Appending
to a list takes O(1), and making a string lower is linear compared to the size of the
word (which is, in most cases, smaller than the size of the file) So,the function runs
in O(n) time, where n is the number of characters in the file. 
'''
def tokenize(TextFilePath):
    #see if the file itself exists
    try:
        with open(TextFilePath, 'r') as file:
            #create a list to store the tokens
            word_list = list()

            #grab each line
            for line in file:
                #split the line into words
                words = split(line)

                #add each word to the set
                for word in words:
                    word_list.append(word.lower())
            
            #return the list of words
            return word_list
        
    #catch error where file is not found
    except FileNotFoundError:
        print(f"Sorry, the file {TextFilePath} does not exist.")
        exit()


'''
This function runs in linear time:
The list words, containing n words, is looped through once. The dictionary operations
are on average constant time (hash-map), so the overall time complexity is O(n), 
where n is the number of words in the list.
'''
def computeWordFrequencies(words):
    #create a dictionary to store word frequencies
    word_freqencies = dict()

    #loop through the list and add the words to the dictionary
    for word in words:
        #check to see if the word is already in the dictionary
        #if so, increase the frequency in the dictionary
        if word in word_freqencies:
            current_freq = word_freqencies[word]
            word_freqencies[word] = current_freq + 1

        #otherwise, just add the word with frequency 1
        else:
            word_freqencies[word] = 1
    
    return word_freqencies

'''
This function runs in linear-logarithmic time:
Python's sorted() function uses Timsort, which runs in O(n log n) time (I had to
look this up), where n is the number of items in the dictionary. Iterating through
the dictionary once also gives an O(n) time, but it is upper bounded by the sorting.
So, the function runs in O(n log n) time, where n is the number of items in word_frequencies
'''
def frequency_print(word_frequencies, amount, file):
    #sort the list of words by frequency (item[1]), decreasing (reverse=True)
    sorted_freq = sorted(word_frequencies.items(), key=lambda item: item[1], reverse=True)
    
    #print them out
    #MODIFIED FOR ASSIGNMENT 2 SO IT PRINTS A VARIABLE AMOUNT IF NECESSARY
    #MODIFIED TO PRINT TO A FILE - THAT IS THE ONLY USE CASE IN THIS PROHECT   
    if(amount == -1):
        for word, freq in sorted_freq:
            file.write(f"{word} - {freq}\n")

    else:
        for word, freq in sorted_freq[:amount]:
            file.write(f"{word} - {freq}\n")

'''
The program runs in linear-logarithmic time:
Given the runtimes of the functions, the main program runs in linear-logarithmic time,
on average. Overall, the sorting in the frequency_print function takes O(n log n) time,
where n is the number of UNIQUE words in the file. Although tokenize runs in O(m) time,
where m is the TOTAL number of words in the file, I believe that in most cases 
O(n log n) will upper bound O(m) with the current definitions of n and m. There are
some cases where this may not be true, such as a file that repeats one word continuously
but I believe that in general, this is true.
'''
if __name__ == "__main__":
    if len(sys.argv) == 2:
        text_file = sys.argv[1]
        word_list = tokenize(text_file);
        word_freq_dict = computeWordFrequencies(word_list);
        frequency_print(word_freq_dict);
    
    elif len(sys.argv) > 2:
        print("Error: Too many arguments! Please provide a single argument with the desired file path")

    else:
        print("Error: No Arguments Provided! Please provide a single argument with the desired file path")