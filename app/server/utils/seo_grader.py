import re
import  os
import math
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from textblob import TextBlob as tb
from requests.exceptions import ReadTimeout
from collections import defaultdict, Counter

import spacy
nlp = spacy.load('en_core_web_md')

serp_key = os.getenv("SERP_API_KEY")

additional_stopwords = ["arent", "cant", "couldnt", "didnt", "doesnt", "dont", "hadnt", "hasnt", "havent", "hed", "hell", "hes", "heres", "hows", "id", "ill", "im", "ive", "isnt", "its", "lets", "mustnt", "shant", "shed", "shell", "shes", "shouldnt", "thats", "theres", "theyd", "theyll", "theyre", "theyve", "wasnt", "wed", "well", "were", "weve", "werent", "whats", "whens", "wheres", "whos", "whys", "wont", "wouldnt", "youd", "youll", "youre", "youve"] 


def text_blob(text):
    return tb(text)

def clean(text):

    # removing paragraph numbers
    text = re.sub('[0-9]', '', str(text))
    text = re.sub('[0-9]+.\t', '', str(text))
    # removing new line characters
    text = re.sub('\n ', '', str(text))
    text = re.sub("'", '', str(text))
    # removing apostrophes
    text = re.sub("'s", '', str(text))
    # removing hyphens
    text = re.sub("-", ' ', str(text))
    text = re.sub("— ", '', str(text))
    # removing quotation marks
    text = re.sub('\"', '', str(text))
    # removing salutations
    text = re.sub("Mr\.", 'Mr', str(text))
    text = re.sub("Mrs\.", 'Mrs', str(text))
    # removing any reference to outside text
    text = re.sub("[\(\[].*?[\)\]]", "", str(text))
    text = re.sub(r'[^\w\s]','', str(text))

    return tb(text.strip())

def average_word_count(text_list: list):
    length_list = len(text_list)
    average_length = len([ word for text in text_list for word in text.split() if text ]) / (length_list if length_list else 1)
    return average_length

def clear_text(text_list: list, remove_stopwords= False, remove_noise= False, remove_empty= True, lower= True):

    if remove_empty:
        text_list = [ text for text in text_list if text ]
    
    if lower:
        text_list = [ text.lower() for text in text_list ]

    if remove_noise:
        text_list = [ clean(text) for text in text_list ]

    if remove_stopwords:
        text_list = removeStopwords(text_list= text_list)

    return text_list

def removeStopwords(text_list: list):

    # Create list of word tokens after removing stopwords
    new_text_list = []
    for text in text_list:
        new_word_list = []
        for word in text.words:
            lexeme = nlp.vocab[str(word)]
            if lexeme.is_stop == False and word not in additional_stopwords:
                new_word_list.append(word)

        new_text = ' '.join(new_word_list)
        new_text_list.append(tb(new_text))

    return new_text_list

def extract_attribute(key: str, datas: list):

    values = []
    for data in datas:
        try:
            link = data[key]
        except KeyError as err:
            # Item not present
            link = ''
        values.append(link)

    return values

def get_organic_results(attributes, **params):
    search = GoogleSearch(params)
    results = search.get_dict()
    if 'error' in results: 
        raise Exception ("Error Fetching Google Autocompletions")
    return { attribute: results[attribute] for attribute in attributes if attribute in results }

def find_main_container(h1_tag):
    if h1_tag.parent.select_one('img'):
        return h1_tag.parent
    else:
        return find_main_container(h1_tag.parent)

def get_search_suggesstions(api_key: str, query: str):
    params = {
        "engine": "google_autocomplete",
        "q": query,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    if 'error' in results: 
        raise Exception ("Error Fetching Google Autocompletions")
    return results 

def scrap_organic_results(query: str, top_pages_to_reference: int = 3, api_key: str = serp_key):
    ret = {}
    try:
        results = get_organic_results(['organic_results', 'related_searches', 'related_questions'],
            q=query,
            # location = "Seattle-Tacoma, WA, Washington, United States",
            hl="en",
            gl="us",
            google_domain="google.co.in",
            num=top_pages_to_reference,
            safe="active",
            api_key=api_key
        )
    except Exception:
        return
    
    links = extract_attribute( key='link', datas= results['organic_results'] )
    web_content = gather_content(search_links=links, tags= ['content', 'headings'])
    ret['texts'] = web_content['content']
    ret['headings'] = web_content['headings']

    titles = extract_attribute( key='title', datas= results['organic_results']  )
    titles = [tb(result) for result in titles]
    ret['titles'] = titles

    descriptions = extract_attribute( key='snippet', datas= results['organic_results']  )
    descriptions = [ tb(result) for result in descriptions ]
    ret['descriptions'] = descriptions

    if 'related_questions' in results:
        questions = extract_attribute( key='question', datas= results['related_questions']  )
        questions = [ tb(result) for result in questions ]
        ret['questions'] = questions

        questions_snippets = extract_attribute( key='snippet', datas= results['related_questions']  )
        questions_snippets = [ tb(result) for result in questions_snippets ]
        ret['questions_snippets'] = questions_snippets

        questions_titles = extract_attribute( key='title', datas= results['related_questions']  )
        questions_titles = [ tb(result) for result in questions_titles ]
        ret['questions_titles'] = questions_titles

    if 'related_searches' in results:
        search_queries = extract_attribute( key='query', datas= results['related_searches']  )
        search_queries = [ tb(result) for result in search_queries ]
        ret['related_searches'] = search_queries

    return ret

def extract_text_blobs_web(html_doc, tag, perform_lower_case: bool = True):

    content = tb("")
    # paragraphs = html_doc.find_all('p')
    
    h1_tag = html_doc.find('h1')
    try:
        article_container = find_main_container(h1_tag)

        if tag == "content":
            html_elements = article_container.find_all('p')
        elif tag == "headings":
            html_elements_h2 = article_container.find_all('h2')
            html_elements_h3 = article_container.find_all('h3')
            html_elements = html_elements_h2 if len(html_elements_h2) > len(html_elements_h3) else html_elements_h3

        for paragraph in html_elements:

            # Information Extraction #4 – Rule on Adjective Noun Structure
            paragraph = clean(text=paragraph.text)
            content = content + " " + paragraph.lower() if perform_lower_case else paragraph
    except AttributeError as err:
        pass

    return content 

def extract_text_blobs_text(text, perform_lower_case: bool = True):
    content = tb("")
    paragraphs = [ item.strip() for item in text.split("\n\n") if item.strip() ]
    for paragraph in paragraphs:

        # Information Extraction #4 – Rule on Adjective Noun Structure
        paragraph = clean(text=paragraph)
        content = content + " " + paragraph.lower() if perform_lower_case else paragraph

    return content

def get_html_doc(link):
    try:
        website = requests.get(link, timeout=5)
        return BeautifulSoup(website.content, 'lxml')
    except ReadTimeout:
        return None

def gather_content(search_links: list, tags= ['content', 'headings']):

    content_blobs_lists = defaultdict(lambda: [])
    for search_link in search_links:

        html_doc = get_html_doc(search_link)
        if not html_doc:
            continue

        for tag in tags:
            content_blob = extract_text_blobs_web(html_doc=html_doc, tag= tag)
            content_blobs_lists[tag].append(content_blob)

    return content_blobs_lists

def obtain_common_terms(list_content, short= False):
    '''
    If Topic is True,
        Returns a Dict Object with word suggesstions based on score from 0 - 100
    '''

    all_common_text = []
    for paragraph_blob in list_content:
        for sentence in paragraph_blob.sentences:
            if short:
                sentence_phrases_list = []
                # sentence_phrases_list = str(sentence).split(" ")
                wordlist_singlegram = sentence.ngrams(n= 1)
                wordlist_singlegram = [ ' '.join(items) for items in wordlist_singlegram ]
                sentence_phrases_list.extend(wordlist_singlegram)
                
                wordlist_bigrams = sentence.ngrams(n= 2)
                wordlist_bigrams = [ ' '.join(items) for items in wordlist_bigrams ]
                sentence_phrases_list.extend(wordlist_bigrams)

                wordlist_trigrams = sentence.ngrams(n= 3)
                wordlist_trigrams = [ ' '.join(items) for items in wordlist_trigrams ]
                sentence_phrases_list.extend(wordlist_trigrams)
                
            else:
                sentence_phrases_list = rule3_mod(text=str(sentence))

            sentence_phrases_list = [ str(sentence) for sentence in sentence_phrases_list ]
            all_common_text.extend(sentence_phrases_list)

    all_common_text_counter = Counter(all_common_text)
    # if topic:
    #     temp_counter = all_common_text_counter.copy()
    #     for word, count in all_common_text_counter.items():
    #         if count == 1:
    #             del temp_counter[word]
    #         else:
    #             temp_counter[word] = ( count/ len(list_content) ) * 100
    #     all_common_text_counter = temp_counter
        
    return all_common_text_counter

def filter_group(same_phrase_confidences_group: dict):

    filtered_suggesstions = []
    if not same_phrase_confidences_group:
        return filtered_suggesstions
    
    for common_word, phrases_subset_list in same_phrase_confidences_group.items():
        subsets_confidences = [ subset[1] for subset in phrases_subset_list ]
        max_confidennce = max(subsets_confidences)
        max_confident_index = subsets_confidences.index(max_confidennce)
        phrase, confidence, overall_score = phrases_subset_list[max_confident_index]
        filtered_suggesstions.append( (phrase, confidence, overall_score) )

    return filtered_suggesstions

def group_suggesstions(suggesstions: list, index= 0):

    same_phrase_confidences_group = defaultdict(lambda: [])
    
    if not suggesstions:
        return same_phrase_confidences_group
    phrases = [ suggesstion[0].split()[index] for suggesstion in suggesstions ]
    phrases_counter = Counter(phrases)
    
    for phrase, confidence, overall_score in suggesstions:
        overall_phrase_count = phrases_counter[phrase.split()[0]]
        same_phrase_confidences_group[phrase.split()[index]].append( (phrase, confidence, overall_score) )

    return same_phrase_confidences_group

def remove_subsets(suggesstions: list, using_first_word= True):
    
    if using_first_word:
        same_phrase_confidences_group = group_suggesstions(suggesstions, index= 0)
    else:
        same_phrase_confidences_group = group_suggesstions(suggesstions, index= -1)

    filtered_suggesstions = filter_group(same_phrase_confidences_group)
    return filtered_suggesstions

def suggest_words(reference_counter, organic_counter, num_compares= 1, topic= False, content_threshold = 40, topic_threshold= 70, repeat_threshold_for_n_articles = 50, remove_duplicates= True):
    suggesstions = {}
    suggesstions_high, suggesstions_recommended = [], []
    
    # Topic suggesstions
    reference_words = reference_counter.keys()
    organic_counter_temp = organic_counter.copy()
    
    for word, count in organic_counter.items():
            
        average_word_count = count/num_compares
        if average_word_count > reference_counter[word]:
            # Topic
            if topic:
                confidence = (count/num_compares) * 100
                if confidence > topic_threshold:
                    suggesstions_recommended.append( (word, 0, 1) )
                continue
    
            # Description and Content
            else:
                if not int(average_word_count):
                    confidence = (count/ num_compares) * 100
                    if confidence > content_threshold:
                        suggesstions_recommended.append((word, reference_counter[word], reference_counter[word]+1))
                        # suggesstions_recommended.append( f'{word}, Confidence [ {confidence} % ]' )
                else:
                    suggesstions_high.append( (word, reference_counter[word], math.ceil(average_word_count)) )
                    # suggesstions_high.append( f' {word}, Count [ {reference_counter[word]}/ {average_word_count} ]' )
        else:
            del organic_counter_temp[word]

    if remove_duplicates:
        suggesstions_high = remove_subsets(suggesstions_high, using_first_word= True)
        suggesstions_high = remove_subsets(suggesstions_high, using_first_word= False)
        suggesstions_recommended = remove_subsets(suggesstions_recommended, using_first_word= True)
        suggesstions_recommended = remove_subsets(suggesstions_recommended, using_first_word= False)

    suggesstions['Highly Recommended'] = suggesstions_high 
    suggesstions['Recommended'] = suggesstions_recommended

    return suggesstions

def suggest_words_bkp(reference_counter, organic_counter, num_compares= 1, topic= False, content_threshold = 40, topic_threshold= 70, repeat_threshold_for_n_articles = 50, remove_duplicates= True):
    suggesstions = {}
    suggesstions_high, suggesstions_recommended = [], []
    
    # Topic suggesstions
    reference_words = reference_counter.keys()
    organic_counter_temp = organic_counter.copy()
    
    for word, count in organic_counter.items():
            
        if word not in reference_words and ( count > 1 and count != reference_counter[word] ):
            # Topic
            if topic:
                confidence = (count/num_compares) * 100
                if confidence > topic_threshold:
                    suggesstions_recommended.append( (word, 0, 1) )
                continue
    
            # Description and Content
            else:
                average_word_count = count//num_compares
                if not average_word_count:
                    confidence = (count/ num_compares) * 100
                    if confidence > content_threshold:
                        suggesstions_recommended.append((word, 0, 1))
                        # suggesstions_recommended.append( f'{word}, Confidence [ {confidence} % ]' )
                else:
                    suggesstions_high.append((word, reference_counter[word], average_word_count))
                    # suggesstions_high.append( f' {word}, Count [ {reference_counter[word]}/ {average_word_count} ]' )
        else:
            del organic_counter_temp[word]

    if remove_duplicates:
        suggesstions_high = remove_subsets(suggesstions_high, using_first_word= True)
        suggesstions_high = remove_subsets(suggesstions_high, using_first_word= False)
        suggesstions_recommended = remove_subsets(suggesstions_recommended, using_first_word= True)
        suggesstions_recommended = remove_subsets(suggesstions_recommended, using_first_word= False)

    suggesstions['Highly Recommended'] = suggesstions_high 
    suggesstions['Recommended'] = suggesstions_recommended

    return suggesstions

def suggest_word_count(reference_word_count, organic_word_count):
    suggesstions = {}
    suggesstions['Reference Article Count'] = reference_word_count
    suggesstions['Organic Article Count'] = organic_word_count
    word_count_difference = reference_word_count - organic_word_count
    if word_count_difference == 0:
        suggesstions['Suggesstion'] = f'Perfect Word count'
    elif word_count_difference > 0:
        suggesstions['Suggesstion'] = f'Remove {word_count_difference} unncessary words'
    elif word_count_difference < 0:
        suggesstions['Suggesstion'] = f'Add {abs(word_count_difference)} words'

    return suggesstions

def suggest_primary_keyword_density(paragraph, primary_keyword, n=100):
    suggesstion = {}
    reference_para_wordlist = paragraph.split()
    reference_para_length = len(reference_para_wordlist)

    num_chunks = reference_para_length//n
    
    count = 0
    for chunk in range(num_chunks):
        if primary_keyword not in reference_para_wordlist[ n * chunk : n * (chunk + 1) ]:
            count += 1
    
    suggesstion['Keyword count in First Para'] = (primary_keyword, count, num_chunks)
    return suggesstion

def calculate_overall_word_score(reference_word_count, organic_word_count):
    word_difference = reference_word_count - organic_word_count
    if word_difference > 0 or word_difference == 1 or organic_word_count == 0:
        return 100
    else:
        return ( reference_word_count/ organic_word_count ) * 100
        
def calculate_overall_score(suggesstions):
    included_count, included_score = 0, 0
    total_count, total_score= 0, 0
    for criteria, suggesstion in suggesstions.items():
        if criteria == "Highly Recommended":
            for word, score, total in suggesstion:
                included_count += score
                total_count += total
        elif criteria == "Recommended":
            for word, score, total in suggesstion:
                included_score += score
                total_score += total
    
    count_percentage = (included_count/ total_count) * 100 if total_count else 100
    score_percentage = (included_score/ total_score) * 100 if total_score else 100

    effective_average = (count_percentage * 0.7 + score_percentage * 0.3)
    return effective_average