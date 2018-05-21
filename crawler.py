    #__________ Imports

from urllib.request import *
from bs4 import BeautifulSoup
import re
import string
import os

#_________________________ Establish Variables
main_search_term = "money" #......................... Main Query
related_search = ["money", "currency", "cash", "history", "government", "trade", "barter", "gold", "silver", "food", "people", "murder", "war", "stock","exchange", "bonds"] #.............. Related Terms
root_url = "https://en.wikipedia.org"
seed_urls = ['/wiki/Money', 'wiki/Stock_exchange']
used = []
counter = 0 #..................................................  counts webpages parsed limit 500 For main loop
saved = 0   #..................................................  Number of pages saved
score = 0   #..................................................  used for ranking system -> Score must be > X to be relavent
rank_min = 2 #.................................................  The min score a URL needs to be conidered relevant 
limit = 25 #.................................................. set for limit  (how many web pages to scrape)
#__________END____________ Establish Variables



    


#______________________________________________

#_______ Write successful URLS TO FILE ________

#______________________________________________



def write_to_file(url_ext, html,counter):
    
    file_name =  'store_html/'+str(counter)+'_'+url_ext + '.html'
    
    text = html.prettify()
    # text = re.sub('[^a-zA-Z0-9-<->-!-"-*.\s]', '', text)
    print('\n Writing to File...')
    try:
        with open(file_name, 'w', encoding='utf-8') as fout:
            fout.write(text)
        return True

    except:
        return False
        

#________________________________

#__________ Main Loop ___________

#________________________________

while len(used)< limit:
    #----- Build URL -> Scrape URL -> Parse through BeautifulSoup to create object ---------------------------------
    try:
        html = urlopen(root_url + seed_urls[counter]); #... URLS  being built
        soup = BeautifulSoup(html, 'html.parser');
        #---------------------------------------------------------------------------------------------------------------
        #----------------------------            Ranking System                  ---------------------------------------
        #---------------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------------
        #.. Count Search terms located in string sections + 1 for each term found
        title = soup.title.get_text()
        title = title.replace(" ", "_")#file format
        title = title.replace(":", "_")#file format
        title = title.replace("-", "")#file format

        

        body = soup.find('div',class_ = 'mw-content-ltr')
        body_text = body.get_text().lower()
        word_count = 0 #break for loop if word count > rank_min save time make sure relevant this counts words in related_terms within doc
        #.. Loop through relavent_terms if two terms are found // break to save time
        for x in related_search:
            temp = len(re.findall(x,body_text)) #This finds all occurrences of the word
            if temp > 0:
                score = score + temp
                if word_count > rank_min:
                    break
                else:
                    word_count = word_count + 1
                
            


#.. END
                
        #.. Get elements from the HTML --> High Rank value +5 gets saved as relavent
        #............................... 
        #............................... BUILD CRAWLER SCHEMA --> this is not working
        #.. Get all the links in body div tag, store them in the seed URL list for crawling process!!
        if(counter <= 2 or counter >= len(seed_urls) -2):
            for link in body.findAll('a',href=re.compile('wiki/')):
                if saved <= limit and link not in seed_urls:
                    link_str = link.get('href')
                    #link_str = link_str.encode('utf-8')
                    link_str = str(link_str)
                    link_str = link_str.strip()
                    link_str = link_str.lower()
                    
                    #__ For some reason can only get it to work when i stack conditions not inline using or??
                    if link_str[-3:] != 'svg':
                        if link_str[-3:] != 'jpg':
                            if link_str[-3:] != 'png':
                                 if link_str[-3:] != 'giv': 
                                    seed_urls.append(link.get('href')) #.. Store the link as a new seed until we have 500 seeds
        #...............................             
            




        #.... Check Webpages Score & Report to user
        if (word_count >= rank_min) and (seed_urls[counter] not in used):
           #print(root_url + seed_urls[counter] , ' Good =', score)
           if write_to_file(title, soup, counter) == True:
               saved = saved + 1
               used.append(seed_urls[counter])
               #print('array len == ' ,len(used))
           else:
               #print('Problem writing to file')
               pass
        else:
           print(root_url + seed_urls[counter] , ' Bad = ' ,score )
    except:
        #__ If URL is not valid replace alert user and
        print('URL does not exist')
        
        

        
    counter = counter + 1
    score = 0 # reset score for next URL



    
#________________________________

#___END___ Main Loop ___________

#________________________________

input("\n \n \n \n \n \n \n \n \n \n -- Process Complete")


