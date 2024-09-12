# import re
# import nltk
# import spacy
# from spacy.lang.en import English
# import enchant

# verbose = False

# # Load English tokenizer, tagger, parser, NER and word vectors
# nlp = English()
# nlp.add_pipe('sentencizer')
# nlp = spacy.load('en_core_web_md')

# class Grading:
#     def __init__(self, annotator, gramformer, punctuations= "!#$%&'()*+,-/.:;<=>?@[\]^_`{|}~"):
#         self.annotator = annotator
#         self.punctuations = punctuations
#         self.gramformer = gramformer
    
#     def removeStopwords(self, text):
        
#         # Create list of word tokens after removing stopwords
#         new_word_list =[]

#         for word in self.getWordTokens(text):
#             lexeme = nlp.vocab[word]
#             if lexeme.is_stop == False:
#                 new_word_list.append(word)

#         sentence = ' '.join(new_word_list)
#         if verbose:
#             print(f'\nRemoved Stopwords Sentence: {sentence}')
        
#         return sentence

#     def getWordTokens(self, text):

#         #  "nlp" Object is used to create documents with linguistic annotations.
#         my_doc = nlp(text)

#         # Create list of word tokens
#         word_tokens_list = token_list = []
#         for token in my_doc:
#             word_tokens_list.append(token.text)

#         if verbose:
#             print(f'\nWord Tokens List: {token_list}')
        
#         return word_tokens_list
    
#     def getUniqueWords(self, allWords):
#         uniqueWords = [] 
#         for i in allWords:
#             if not i in uniqueWords:
#                 uniqueWords.append(i)

#         if verbose:
#             print(f'\nUnique Words only: {uniqueWords}')

#         return uniqueWords
    
#     def wordRepetitionAccuracy(self, all_words, unique_words):
        
#         total_word_length = len(all_words)
#         unique_word_length = len(unique_words)
#         accuracy = unique_word_length / total_word_length

#         if verbose:
#             print(f'Total_word_length: {total_word_length}. Unique_word_length: {unique_word_length}')
#             print(f'Word Repetition Accuracy: {accuracy}')
        
#         return accuracy
    
#     def removePunctuations(self, text):
#         text_punctuation_less = ''.join([ txt for txt in text if txt not in self.punctuations])
#         if verbose:
#             print(f'Text after removing punctuation marks: {text_punctuation_less}')

#         return text_punctuation_less

#     def preprocess(self, text):
#         text = text.replace("\\n", '').replace("\\t", '')
#         text = re.sub('â€™',"'",text)
#         text = re.sub('â€™',"'",text)

#         text_preprocessed = self.removePunctuations(text)

#         if verbose:
#             print(f'\n Prepocesses Text: {text_preprocessed}')

#         return text_preprocessed
    
#     def seperateCharacters(self, text):
#         characters_list = [ char for char in text ]

#         if verbose:
#             print(f'\Seperated Characters: {characters_list}')

#         return characters_list

#     def seperateWords(self, text):
#         words = nltk.word_tokenize(text)
#         words_list = [ word for word in words if word not in self.seperateCharacters(self.punctuations) ]

#         if verbose:
#             print(f'\nSeperated Words: {words_list}')

#         return words_list

#     def seperateSentences(self, text):
#         doc = nlp(text)
#         sentence_list = list(doc.sents)

#         if verbose:
#             print(f'\nSeperated Sentences: {sentence_list}')

#         return sentence_list

#     def clarityAccuracy(self, article_syllables_count, article_words, sentence_list):
        
#         redability_score = 206.835 - 1.015 * (len(article_words)/ len(sentence_list)) - 84.6 * ( article_syllables_count/len(article_words) )
#         redability_score = redability_score/100
#         redability_score = 1 if redability_score >1 else (0 if redability_score < 0 else redability_score)
#         return redability_score

#     def lemmatize(self, text_preprocessed):
#         text = nlp(text_preprocessed) 
#         text_lemmatized = " ".join([token.lemma_ for token in text])

#         if verbose:
#             print(f'\nLemmetized to root words: {text_lemmatized}')

#         return text_lemmatized

#     def coherenceAccuracy(self, sentences, dependent_average_score= None, default_score_for_single_sentence= 1):
#         coherence_ = 0

#         if len(sentences) == 1 or len(sentences) == 0:
#             return dependent_average_score if dependent_average_score else default_score_for_single_sentence

#         sentences  = [sentence.text for sentence in sentences]
#         sentence_embeddings = [ nlp(sentence) for sentence in sentences ]
#         for selected_sentence_index, selected_embedding in enumerate(sentence_embeddings):
#             if verbose:
#                 print(f'-> Sentence Index: {selected_sentence_index}')
            
#             embedding_similarities = []
#             for comparision_sentence_index, comparision_sentence_embedding in enumerate(sentence_embeddings):
#                 if verbose:
#                     print(f'Comparing with: {comparision_sentence_index}')
                
#                 if selected_embedding == comparision_sentence_embedding:
#                     if verbose:
#                         print(f'Neglecting same sentence!')
#                 else:
#                     embedding_similarity = selected_embedding.similarity(comparision_sentence_embedding)
#                     if verbose:
#                         print(f'Embedding Similarity: {embedding_similarity}')
#                     embedding_similarities.append(embedding_similarity)
        
#             max_score = max(embedding_similarities)
#             if max_score > 0.8:
#                 coherence_ += 1
#             else:
#                 coherence_ += max_score
#         coherence_score = coherence_/ len(sentences)
#         if verbose:
#             print(f'\nText Coherence Accuracy: {coherence_score}')
            
#         return coherence_score

#     def correctGrammer(self, text):
#         corrected_grammer = self.gramformer.correct(str(text), max_candidates=1)
#         return corrected_grammer
        
#     def grammerAccuracy(self, sentences):
        
#         sentences = [i.text for i in sentences]
#         corrected_sentences = []

#         for influent_sentence in sentences:
            
#             corr_sentences = self.gramformer.correct(str(influent_sentence), max_candidates=1)
#             if verbose:
#                 print("[Input] ", influent_sentence)
            
#             for corrected_sentence in corr_sentences:
#                 if verbose:
#                     print("-" *100)
#                     print("[Correction] ",corrected_sentence)

#                 corrected_sentences.append(corrected_sentence)
        
#         score = 0
#         for original_sentence, corrected_sentence in zip(sentences, corrected_sentences):

#             if verbose:
#                 print(f'\noriginal_sentence: {original_sentence}, type: {type(original_sentence)}')
#                 print(f'\ncorrected_sentence: {corrected_sentence}, type: {type(corrected_sentence)}')
            

#             common_accuracy = self.getCommonWordsAccuracy(original_sentence, corrected_sentence)
#             score += common_accuracy

#         accuracy_percentage = score/ len(sentences)
#         if verbose:
#             print(f'\Grammar Accuracy: {score}')

#         return abs( accuracy_percentage )

#     def gradCompute(self, attributes: list, weights: list):

#         if verbose:
#             print(f'\nAttribure Accuracies used to Measure Overall Score: {attributes}')
#             print(f'\nGradients used to Measure Overall Score: {weights}')
        
#         overall_score = 0
#         for attribute_score, attribute_weight in zip(attributes, weights):
#             weighted_score = attribute_score * attribute_weight
#             overall_score += weighted_score
#             if verbose:
#                 print(f'\nWeighted Score: {weighted_score}, Attribute Score: {attribute_score}, Attribute Weight: {attribute_weight}')
#         overall_score *= 100
#         if verbose:
#             print(f'\nPercentage Score: {overall_score}')

#         return overall_score

#     def getCommonWordsAccuracy(self, text1, text2):
#         text1_words = self.getWordTokens( self.removePunctuations( text1) )
#         text2_words = self.getWordTokens( self.removePunctuations( text2) )

#         count = 0
#         for token_word1 in text1_words:
#             if token_word1 in text2_words:
#                 text2_words.remove(token_word1)
#                 count += 1

#         common_accuracy = count/len(text1_words)

#         if verbose:
#             print(f'Common words Accuracy [Considered Words only in Original Sentence]: {common_accuracy}')

#         common_accuracy -= ( 0.3 * len(text2_words) )

#         if verbose:
#             print(f'Total words: {len(text1_words)}')
#             print(f'Extra words: {len(text2_words)}')
#             print(f'Punish for extra words not considering: { 0.3 * len(text2_words)}')
#             print(f'Common words Accuracy [Including Words left in Corrected Sentence]: {common_accuracy}')
#         return common_accuracy

#     def count_syllables(self, words):
#         syllable_count = 0
#         for word in words:
#             syllable_count += len(
#                 re.findall('(?!e$)[aeiouy]+', word, re.I) +
#                 re.findall('^[^aeiouy]*e$', word, re.I)
#             )
        
#         return syllable_count

#     def word_meanings_score(self, text):

#         # It accepts stopword removed text, and then it checks each words meaning
#         word_list = [i for i in text.split(" ") if len(i.strip())]
#         en_dictionary_uk = enchant.Dict("en_UK")
#         en_dictionary_us = enchant.Dict("en_US")
#         is_word_score = 0
#         irelevant_words = []
#         for word in word_list:
#             try:
#                 if en_dictionary_us.check(word) or en_dictionary_uk.check(word):
#                     is_word_score += 1
#                 else:
#                     raise Exception
#             except:
#                 irelevant_words.append(word)
#                 pass

#         word_meaning_percentage = ( (is_word_score*100)/(len(word_list)) )/100
#         word_meaning_percentage = 1 if word_meaning_percentage >1 else (0 if word_meaning_percentage < 0 else word_meaning_percentage)
#         return word_meaning_percentage

#     def calculate_grammer_score(self, text, weights):
        
#         # Word Repetition
#         text_preprocessed = self.preprocess(text= text)
#         text_removed_stopwords = self.removeStopwords(text= text_preprocessed)
#         text_lemmatized = self.lemmatize(text_preprocessed= text_removed_stopwords)
#         word_tokens_list = self.getWordTokens(text = text_lemmatized)
#         word_repetition_accuracy =self.wordRepetitionAccuracy(all_words= word_tokens_list, unique_words = self.getUniqueWords(word_tokens_list))

#         # Readability/ Clarity
#         article_words= self.seperateWords(text= text)
#         sentence_list= self.seperateSentences(text= text)
#         article_syllables_count = self.count_syllables(words= article_words)
#         clearity_accuracy =self.clarityAccuracy(article_syllables_count= article_syllables_count, article_words= article_words, sentence_list= sentence_list)

#         # Grammer Score
#         sentence_list= self.seperateSentences(text= text)
#         grammer_score = self.grammerAccuracy(sentence_list)

#         # Word Meaning Checker
#         word_meaning_accuracy = self.word_meanings_score(text_removed_stopwords)
        
#         #Context Coherence
#         coherance_accuracy = self.coherenceAccuracy(self.seperateSentences(text= text), dependent_average_score= (clearity_accuracy + grammer_score + word_meaning_accuracy)/3)

#         # Compute Text Score
#         percentage_score =self.gradCompute(attributes= [word_repetition_accuracy, clearity_accuracy, coherance_accuracy, grammer_score, word_meaning_accuracy], weights= weights )

#         scores = {
#             "Word Repetition Accuracy" : word_repetition_accuracy,
#             "Clearity Accuracy" : clearity_accuracy,
#             "Coherance Accuracy" : coherance_accuracy,
#             "Grammer Accuracy": grammer_score,
#             "Word meaning Accuracy": word_meaning_accuracy,
#             "Overall Text Score" : percentage_score
#         }

#         return scores