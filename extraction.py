def content_extractor(resp):
    #first, check if response is valid
    if(resp.status != 200):
        return ""
    else:
        #create beautiful soup object to parse html content of the webpage
        soup_parser = BeautifulSoup(resp.raw_response.content, "lxml-xml")

        # try to get text from main, article, or body
        target = soup_parser.find('main') or soup_parser.find('article') or soup_parser.body
        if target:
            return target.get_text(seperator='\n', strip=True)
        else:
            return ""