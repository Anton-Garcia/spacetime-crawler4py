from pathlib import Path
import doctools
from nltk.corpus import stopwords
import string

#folder path of all documents downloaded from crawling
folder_path = Path("text_content")

#used for token filtering - we only want relevant words, not random tokens
STOPWORDS = set(stopwords.words("english"))
PUNCTUATION = set(string.punctuation)

#one file for each url; same number of files as number of urls downloaded
total_files = 0

#variable to hold the length of the longest file, in words, and its url
longest_file = 0
longest_file_url = ""

#dictionary to hold all words and their frequencies
master_token_count = dict()

#dictionary to hold all subdomains and their number of pages
subdomains = dict()

def file_reader():
    #allows function to use the values of the global variables, not local ones
    global total_files, longest_file, longest_file_url, master_token_count, subdomains

    for file in folder_path.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            #####FINDING THE NUMBER OF DOCUMENTS##### 
            total_files += 1
            
            #####FINDING THE LONGEST DOCUMENT#####    

            #When we turned the urls into files, we had to change the / to avoid bad filenames
            #this retuns the name back to the original url
            url_name = file.name.replace('_', '/');

            #feading the file directly into the tokenize method gives a list of 
            #all tokens in the file
            tokenized = doctools.tokenize(file)
            length_of_file = len(tokenized)

            #keep track of which file is the longest
            if(length_of_file > longest_file):
                longest_file = length_of_file
                longest_file_url = url_name

            #####FINDING MOST COMMON WORDS######

            #get the frequency of all tokens in the document, and add them to the master dictionary
            document_token_count = doctools.computeWordFrequencies(tokenized)
            dictionary_adder(master_token_count, document_token_count)

            #####FINDING SUBDOMAIN PAGE COUNTS#####
            
            #first, extract the subdomain from the url
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
        #Filters out stopwords, punctuation, and other tokens like 's
        if word in STOPWORDS or word in PUNCTUATION or word.startswith("'"):
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


def report_writer():
   with open("report.txt", 'w') as file:
        #go through all pages and collect all metrics
        file_reader()
        #remove stopwords from the token dictionary
        dictionary_sanitizer(master_token_count)

        file.write(f"Total number of files downloaded: {total_files}\n\n")

        file.write(f"URL of the longest file: {longest_file_url}\n")
        file.write(f"Length of the longest file: {longest_file}\n\n")

        file.write("Top 50 most common words:\n")
        doctools.frequency_print(master_token_count, 50, file)

        file.write("\nSubdomain Frequencies:\n")
        doctools.frequency_print(subdomains, -1, file)


if __name__ == "__main__":
    report_writer()
