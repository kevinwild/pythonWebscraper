#__________ Imports

from bs4 import BeautifulSoup
import string
import os
# natrual language text kit 3rd party download
# used this for stop words and tokenizing
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#__________ 

#__________ Variables
directory = 'store_html' #_____________ CHANGE THIS VARIABLE TO OUTPUT
my_name = "KevinWildermuth"
stop_words = set(stopwords.words("english")) #__ Declare stop words
#__________ Variables




def write_to_file(data, size, name):
    print('\n\n writing to file \n\n')
    file_name = name + '-'+ my_name +'.txt'
    with open(file_name, 'w') as fout:
        text = 'Index Size:  ' + str(size) + '\n\n\n'
        fout.write(text)
        # write .. INDEX
        for k in data:
            text = k + ' ' + str(data[k]) + '\n'
            try:
                fout.write(text)
            except:
                pass
    choice = input('Would you like to write vocabular list to file? (Y)es or (N)o  ? \n\n ....')
    choice = choice.lower()
    unique_counter = 0
    if(choice[0] == 'y'):
        file_name = 'vocabulary-' + my_name + '.txt' 
        with open(file_name, 'w', encoding='utf-8') as fout:
            for k in data:
                unique_counter += 1
                text = k + '\n ' 
                try:
                    fout.write(text)
                except ZeroDivisionError:
                    pass
            text = "\n\n\n Total Unique Terms = "+ str(unique_counter) 
            fout.write(text)
        
    print('File Write Complete')



#____________________________________
#____________________________________ Frequence based Function
#____________________________________

def build_freqbased_index():
    inverted_index = dict()# create empty inverted index
    document_id = 0 # keeps track of current document
    for file_name in os.listdir(directory):
        document_id = document_id + 1
        #__ Store the document ID and name for later use
        text = file_name + ' = ' + str(document_id) + '\n\n'
        with open('freq_page_link.txt', 'a') as fout:
            fout.write(text)
            
        file_path = directory + '/' + file_name
        temp_storage = dict() #.. hold words and count append in inverded index
         #.. Increment Document Count
        print("Currently processing document, ", document_id)

        
        with open(file_path, 'r', encoding='utf-8') as fout:
            soup = BeautifulSoup(fout, 'html.parser')
            for paragraph in soup.find_all('p'):
                paragraph = paragraph.get_text()#__ Remove HTML within <p>
                paragraph = paragraph.lower()
                tokens = word_tokenize(str(paragraph))
                tokens = [w for w in tokens if not w in stop_words] #__ Tokenize and remove all stop words in NLTK
                for word in tokens:
                    if word not in temp_storage:
                        temp_storage[word] = 1
                    else:
                        temp_storage[word] += 1
            #__ Insert temp_storage into main inverted_list
            for k, v in temp_storage.items():
                if k not in inverted_index:
                    inverted_index[k] = []
                
                inverted_index[k].append([document_id,v])
                    
    doc_size = len(inverted_index) #__ used in output file
    write_to_file(inverted_index,doc_size,'freq_index')
    print('\n\n\n\n\n Total Documents Indexed: ' + str(document_id))
    print('\n\n\n\n\n --------- Process complete \n\n\n')
#____________________________________
#______________  END  _______________ 
#____________________________________
                    

    
#____________________________________
#____________________________________ Position based Function
#____________________________________

def build_pos_index():
    inverted_index = dict()# create empty inverted index
    document_id = 0 # keeps track of current document
    for file_name in os.listdir(directory):
        document_id = document_id + 1 #.. Increment Document Count
        #__ Store the document ID and name for later use
        text = file_name + ' = ' + str(document_id) + '\n\n'
        with open('pos_page_link.txt', 'a') as fout:
            fout.write(text)            
        file_path = directory + '/' + file_name
        temp_storage = dict() #.. hold words and count append in inverded index
        pos_counter = 0 # count word positions
        print("Currently processing document, ", document_id)
        
        with open(file_path, 'r', encoding='utf-8') as fout:
            soup = BeautifulSoup(fout, 'html.parser')
            for paragraph in soup.find_all('p'):
                paragraph = paragraph.get_text()#__ Remove HTML within <p>
                paragraph = paragraph.lower()
                tokens = word_tokenize(str(paragraph))
                tokens = [w for w in tokens if not w in stop_words] #__ Tokenize and remove all stop words in NLTK
                for word in tokens:
                    pos_counter += 1
                    temp_storage[word] = pos_counter
            #__ Insert temp_storage into main inverted_list
            for k, v in temp_storage.items():
                if k not in inverted_index:
                    inverted_index[k]= []
                
                inverted_index[k].append([document_id,v])
                        
    doc_size = len(inverted_index) #__ used in output file
    write_to_file(inverted_index,doc_size,'pos_index')
    print('\n\n\n\n\n Total Documents Indexed: ' + str(document_id))
    print('\n\n --------- Process complete \n\n\n')
    
#___________________
#___________________  GUI
#___________________
    
while True:
    try:
        print('Which Index would you like to run? Enter exit to quit. \n\n---- (P)osition Based Index \n---- (F)requency Based Index \n\n')
        option = input('...............  ')
        option = option.lower()
        if(option[0] == 'f'):
            print('\n\n')
            build_freqbased_index()
        elif(option[0] == 'p'):
            print('\n\n')
            build_pos_index()
        elif(option[0] == 'e'):
            print('\n\n\n\n\n\n\n Good bye...')
            break
        else:
            print("\n\n Not an option, please  try again. \n\n")
            
    except:
        print("\n\n Fail: Not an option, please try again. \n\n")





    
    
