import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from utils import get_urlhash
import shelve

#valid domains for urls
DOMAIN = ["ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu"]
#blacklisted url hashes
BLACKLIST = []

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


# url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
def extract_next_links(url, resp):
    #list to store the links
    all_links = list()

    #first, check if the response was okay
    #if we can't get the page, then we can't get any links
    #return empty list
    if(resp.status != 200):
        return all_links
    
    #otherwise, continue to look through the content
    else:
        #create a BeautifulSoup object to parse the html content of the webpage
        soup_parser = BeautifulSoup(resp.raw_response.content, "lxml-xml")

        #locate all anchor tags, <a>
        for link in soup_parser.find_all('a'):
            href = link.get('href')
            if href:
                defragmented_link = defragment(href)
                all_links.append(defragmented_link)
        
    return all_links


def defragment(url):
    #find the index of the # symbol that denotes a fragment
    index_of_pound = url.find("#")

    #if -1, then there is no fragment, just return the url
    if(index_of_pound == -1):
        return url
    
    #otherwise, return the substring without the fragment
    else:
        return url[0 : index_of_pound]
        

def is_valid(url):   
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        #check if the url is blacklisted - do not attempt to download the webpage from these - 
        #either because they are duplicates, or low information yielding webpages
        elif get_urlhash(url) in BLACKLIST:
            return False
        
        #checks to make sure url's hostname is within our domain
        #iterate through all domains using the any function()
        #not any -> not any of the .endswith() return true
        elif not any(parsed.hostname.endswith(domain) for domain in DOMAIN):
            return False
        
        #checks valid domain name with starting path (for last case today.uci.edu/department/information_computer_sciences/)
        elif(parsed.hostname.endswith("today.uci.edu") and parsed.path.startswith("/department/information_computer_sciences/") == False):
            return False

        #checks extension type; we dont want files that we can't read
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
        
    except TypeError:
        print ("TypeError for ", parsed)
        raise
    