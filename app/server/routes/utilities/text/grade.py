from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from server.models.text.grade import Grade, SEOGrade

# from server.utils.utilities.text.grade import Grading

from server.models.main import ResponseModel, ErrorResponseModel

router = APIRouter()

# from server.utils.utilities.text import errant
# from server.utils.utilities.text.gramformer import Gramformer

from server.utils.seo_grader import scrap_organic_results, suggest_words, extract_text_blobs_text, calculate_overall_score, suggest_primary_keyword_density, suggest_word_count
from server.utils.seo_grader import  obtain_common_terms, text_blob, clear_text, get_search_suggesstions, extract_attribute, average_word_count, calculate_overall_word_score

from server.utils.seo_grader import scrap_organic_results, extract_text_blobs_text, suggest_words, obtain_common_terms, text_blob, removeStopwords, calculate_overall_score
from collections import Counter
import os

# annotator = errant.load('en')
# gramformer = Gramformer(annotator, use_gpu=False)

# @router.post('/grade')
# def calculate_grade_(grade: Grade):

#     grading = Grading( annotator= annotator, gramformer= gramformer )
#     scores = grading.calculate_grammer_score(text= grade.text, weights= [ weight for attribute, weight in jsonable_encoder(grade).items() if attribute != 'text' ])

#     return ResponseModel(scores, "Overall and grammer scores!")

# @router.post('/grammer')
# def correct_grammer_(grade: Grade):

#     grading = Grading( annotator= annotator, gramformer= gramformer )
#     corrected_text = grading.correctGrammer(text= grade.text)

#     return ResponseModel(corrected_text, "Corrected Grammer")

@router.post("/seo_grade")
def grade(seo_grade: SEOGrade):

    overall_suggesstions, overall_suggesstions_scores = {}, {}

    # Get Scrapped content by google search
    scapping_results = scrap_organic_results(query=seo_grade.topic, top_pages_to_reference=seo_grade.num_pages)
    if not scapping_results:
        return {
            "Message" : "Serp API Plan expired!"
        }

    # ################################  Titles  ################################
    # Reference Title
    reference_titles_list, organic_titles_list = [], []

    reference_titles_list = clear_text(text_list= [ text_blob(seo_grade.topic) ], remove_stopwords= True, remove_noise= True, remove_empty= True, lower= True)
    reference_titles_list.extend(reference_titles_list)
    # pprint(f'\n\n\nReference Titles : {[str(item) for item in reference_titles_list]}')

    # Organic Title
    organic_titles_list = clear_text(text_list= scapping_results['titles'], remove_stopwords= True, remove_noise= True  , remove_empty= True, lower= True)
    organic_titles_list.extend(organic_titles_list)
    # pprint(f'\n\n\nOrganic Titles : {[str(item) for item in organic_titles_list]}')
    
    # Organic Google Questions
    if 'questions' in scapping_results:
        organic_related_questions_list = clear_text(text_list= scapping_results['questions'], remove_stopwords= True, remove_noise= True, remove_empty= True, lower= True)
        organic_titles_list.extend(organic_related_questions_list)
        # pprint(f'\n\n\nOrganic Questions : {[str(item) for item in organic_related_questions_list]}')
        
    # Organic Google Questions Titles
    if 'questions_titles' in scapping_results:
        organic_related_questions_titles_list = clear_text(text_list= scapping_results['questions_titles'], remove_stopwords= True, remove_noise= True, remove_empty= True, lower= True)
        organic_titles_list.extend(organic_related_questions_titles_list)
        # pprint(f'\n\n\nOrganic Questions -> Titles : {[str(item) for item in organic_related_questions_titles_list]}')
    
    # Organic Related Searches
    if 'related_searches' in scapping_results:
        organic_related_searches_list = clear_text(text_list= scapping_results['related_searches'], remove_stopwords= True, remove_noise= True, remove_empty= True, lower= True)
        organic_titles_list.extend(organic_related_searches_list)
        # pprint(f'\n\n\Related Searches : {[str(item) for item in organic_titles_list]}')

    # Organic Google Search Suggesstions
    try:
        organic_suggesstions = get_search_suggesstions(api_key=os.getenv('SERP_API_KEY'), query=seo_grade.topic)
    
        organic_suggesstions_list = extract_attribute( key='value', datas= organic_suggesstions['suggestions'] )
        organic_suggesstions_list = clear_text(text_list= organic_suggesstions_list, remove_stopwords= True, remove_noise= True  , remove_empty= True, lower= True)
        organic_titles_list.extend(organic_suggesstions_list)
    except Exception as err:
        pass

    # pprint(f'\n\n\Search Suggesstions : {[str(item) for item in organic_suggesstions_list]}')

    # pprint(f'\n\n\n reference_titles_list : {[str(item) for item in reference_titles_list]}')
    # pprint(f'\norganic_titles_list : {[str(item) for item in organic_titles_list]}')

    ################################  Title Suggesstions  ################################

    # Obtain common terms
    reference_titles_counter = obtain_common_terms(list_content= reference_titles_list, short= True)
    organic_titles_counter = obtain_common_terms(list_content= organic_titles_list, short= True)

    # Generate Suggesstions
    suggesstions = suggest_words(reference_counter= reference_titles_counter, organic_counter= organic_titles_counter, num_compares= len(organic_titles_list), topic= True, remove_duplicates= True)
    overall_suggesstions['Titles Suggesstions'] = suggesstions
    overall_suggesstions_scores['Titles Suggesstions Score'] = calculate_overall_score(suggesstions)



    # ################################  Content  ################################
    # Reference Content
    reference_contents_list, organic_contents_list = [], []
    reference_contents_length_list, organic_contents_length_list = [], []
    

    reference_content_list = [ extract_text_blobs_text(text=seo_grade.text) ]
    reference_content_average_word_length = average_word_count(text_list= reference_content_list)
    reference_contents_length_list.append(reference_content_average_word_length)

    reference_content_list = clear_text(text_list= reference_content_list, remove_stopwords= True, remove_noise= True, remove_empty= True, lower= True)
    reference_contents_list.extend(reference_content_list)
    
    
    # Organic  Content
    organic_content_list = scapping_results['texts']
    organic_content_word_length = average_word_count(text_list= organic_content_list)
    organic_contents_length_list.append(organic_content_word_length)

    organic_content_list = clear_text(text_list= organic_content_list, remove_stopwords= True, remove_noise= True, remove_empty= True, lower= True)
    organic_contents_list.extend(organic_content_list)
    

    # Organic Meta Descriptions
    organic_descriptions_list = clear_text(text_list= scapping_results['descriptions'], remove_stopwords= True, remove_noise= True, remove_empty= True, lower= True)
    organic_contents_list.extend(organic_descriptions_list)

    # Organic Headings
    organic_headings_list = clear_text(text_list= scapping_results['headings'], remove_stopwords= True, remove_noise= True, remove_empty= True, lower= True)
    organic_headings_word_length = average_word_count(text_list= organic_headings_list)
    organic_contents_length_list.append(organic_headings_word_length)
    
    organic_contents_list.extend(organic_headings_list)
    
    # Organic Google Question Answers
    if 'questions_snippets' in scapping_results:
        organic_related_questions_snippets_list = clear_text(text_list= scapping_results['questions_snippets'], remove_stopwords= True, remove_noise= True, remove_empty= True, lower= True)
        organic_contents_list.extend(organic_related_questions_snippets_list)


    ################################  Content Suggesstions  ################################
    # Obtain common terms
    reference_contents_counter = obtain_common_terms(list_content= reference_contents_list, short= True)
    organic_contents_counter = obtain_common_terms(list_content= organic_contents_list, short= True)
    
    # Content Length
    reference_contents_length_list_average = sum(reference_contents_length_list) // len(reference_contents_length_list)
    organic_contents_length_list_average = sum(organic_contents_length_list) // len(organic_contents_length_list)
    overall_suggesstions['Content Length Suggesstions'] = suggest_word_count(reference_contents_length_list_average, organic_contents_length_list_average)
    overall_suggesstions_scores['Content Length Score'] = calculate_overall_word_score(reference_contents_length_list_average, organic_contents_length_list_average)
    
    # Generate Suggesstions
    suggesstions = suggest_words(reference_counter= reference_contents_counter, organic_counter= organic_contents_counter, num_compares= seo_grade.num_pages, remove_duplicates= True)
    overall_suggesstions['Content Suggesstions'] = suggesstions
    overall_suggesstions_scores['Content Suggesstions Score'] = calculate_overall_score(suggesstions)


    ################################  Primary Keyword in First Para  ################################
    all_titles_list = reference_titles_list.copy()
    all_titles_list.extend(organic_titles_list)
    all_titles_counter = obtain_common_terms(list_content= all_titles_list, short= True)
    primary_keyword = all_titles_counter.most_common(n = 1)[0][0]

    try:
        reference_para = reference_content_list[0]
    except  IndexError:
        reference_para = ''
    suggesstions = suggest_primary_keyword_density(paragraph= reference_para, primary_keyword= primary_keyword, n= 100)
    overall_suggesstions['Primary Keyword Suggesstions'] = suggesstions


    ################################  Main Score  ################################
    overall_article_score = ( sum(list(overall_suggesstions_scores.values())) / len(overall_suggesstions_scores) )
    overall_suggesstions_scores['Overall Article Score'] = overall_article_score
    return overall_suggesstions, overall_suggesstions_scores
