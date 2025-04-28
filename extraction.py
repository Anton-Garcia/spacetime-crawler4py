from bs4 import BeautifulSoup

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
def exact_detection(text):
    return False

#download the text in a file for statistics postprocessing
def download_text(text):
    return

#overhead function to extract text, then download it if necessary
def process_webpage_text(resp):
    #if no response, move onto next page
    if(resp.status != 200):
        return
    
    #extract useful text from the webpage
    webpage_text = content_extractor(resp)

    #check if the text we get is an exact duplicate from another webpage
    if(exact_detection(webpage_text)):
        return
    
    #if it is not an exact duplicate, then we should save this page
    else:
        download_text(webpage_text)