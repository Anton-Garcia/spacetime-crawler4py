from pathlib import Path
import doctools

folder_path = Path("text_content")
STOPWORDS = [
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could",
    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for",
    "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's",
    "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
    "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't",
    "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
    "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when",
    "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
]

#one file for each url; same number of files as number of urls downloaded
total_files = 0;

#variable to hold the length of the longest file, in words
longest_file = 0;

#dictionary to hold all words and their frequencies
master_token_count = dict()

#dictionary to hold all subdomains and their number of pages
subdomains = dict()

def file_reader():
    #allows function to use the values of the global variables, not local ones
    global total_files, longest_file, master_token_count, subdomains

    for file in folder_path.iterdir():
        #####FINDING THE NUMBER OF DOCUMENTS##### 
        total_files += 1
        
        #####FINDING THE LONGEST DOCUMENT#####    

        #feading the file directly into the tokenize method gives a list of 
        #all tokens in the file
        tokenized = doctools.tokenize(file)
        length_of_file = len(tokenized)

        #keep track of which file is the longest
        if(length_of_file > longest_file):
            longest_file = length_of_file

        #####FINDING MOST COMMON WORDS######

        #get the frequency of all tokens in the document, and add them to the master dictionary
        document_token_count = doctools.computeWordFrequencies(tokenized)
        dictionary_adder(master_token_count, document_token_count)

        #####FINDING SUBDOMAIN PAGE COUNTS#####
          
        #When we turned the urls into files, we had to change the / to avoid bad filenames
        #this retuns the name back to the original url
        url_name = file.name.replace('_', '/');
        subdomain = sub_extracter(url_name)

        #if the subdomain is already in the dictionary, we've ran into another page in the
        #subdomain. Add one to the count of pages
        if subdomain in subdomains.keys():
            subdomains[subdomain] += 1
        
        #if the subdomain is not in the dictionary, we've found a new subdomain. Add it to
        #the dictionary, with a page count of 1
        else:
            subdomains[subdomain] = 1

        
#function to add two dictionaries together
def dictionary_adder(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1:
            dict1[key] +=  value
        
        else:
            dict1[key] = value
    
    return dict1

#function to clean stopwords out of dictionary
def dictionary_sanitizer(dictionary):
    for word in list(dictionary):
        if word in STOPWORDS:
            del dictionary[word]

#extracts the subdomain of the url
def sub_extracter(url):
    #in our crawl, we only accept schemes of https or http, so we
    #only check for these two scenarios, and remove them accordingly
    if(url.startswith("https://")):
        url = url[8:]
        
        #if the page is not the root, it has a /...
        #we dont have to worry about fragments (#) or
        #queries (?) because we removed them. Finds the 
        #end of the subdomain accordingly
        stop_index = url.find("/")
        if(stop_index != -1):
            return url[:stop_index]
        
        else:
            return url
    
    #same as the above example except accounts for the
    #missing s in https
    else:
        url = url[7:]
        stop_index = url.find("/")
        if(stop_index != -1):
            return url[:stop_index]
        
        else:
            return url



if __name__ == "__main__":
    #go through all pages and collect all metrics
    file_reader()
    #remove stopwords from the token dictionary
    dictionary_sanitizer(master_token_count)

    print("Total number of files downloaded: ", total_files)

    print("Length of the longest file: ", longest_file)

    print("Top 50 most common words:")
    doctools.frequency_print(master_token_count, 50)

    print("Subdomain Frequencies:")
    doctools.frequency_print(subdomains, -1)
