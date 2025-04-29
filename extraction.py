from bs4 import BeautifulSoup
from utils import get_texthash

seen_text = set()

#extracts useful text from the webpage response
def content_extractor(resp):
    #first, check if response is valid
    if(resp.status != 200):
        return ""

    else:
        #create beautiful soup object to parse html content of the webpage
        soup_parser = BeautifulSoup(resp.raw_response.content, "lxml-xml")

        #try to get text from <main>
        main_content = soup_parser.find("main")
        if(main_content):
            return main_content.get_text(seperator='\n', strip=True)
    
        #if there is no <main>, check for <article>
        else:
            article_content = soup_parser.find("article")
            if(article_content):
                return article_content.get_text(seperator='\n', strip=True)
            
            #if there is no <main> or <article>, use whole body
            else:
                #decompose/remove <script> and <style> tags that provide 
                #useless information before we grab the text
                for invalid in soup_parser.find_all(["script", "style"]):
                    invalid.decompose()

                return soup_parser.get_text(seperator='\n', strip=True)

#exact textual detection via hashing for blacklist
#low information value detection for blacklist
def blacklist_detection(text):
    #if the text retrieved from the webpage is blank, then
    #we can say that it is low-value and can be blacklisted
    if text == "":
        return True
    
    #hash the text obtained to see if we get an exact match
    hashed_text = get_texthash(text)

    if hashed_text in seen_text:
        return True

    else:
        seen_text.add(hashed_text)
        return False

#download the text in a file for statistics postprocessing
def download_text(text, url_name):
    folder_path = 'text_content'
    file_name = url_name
    full_path = f'{folder_path}/{file_name}'
    with open(full_path, 'w') as file:
        file.write(text)

#overhead function to extract text, then download it if necessary
def process_webpage_text(resp):
    #if no response, move onto next page
    if(resp.status != 200):
        return
    
    #extract useful text from the webpage
    webpage_text = content_extractor(resp)

    #check if the text we get is an exact duplicate from another webpage
    if(blacklist_detection(webpage_text)):
        with open('blacklist.txt', 'a') as file:
            file.write(resp.url)
            file.write('\n')
    
    #if it is not an exact duplicate, then we should save this page
    else:
        download_text(webpage_text, resp.url)