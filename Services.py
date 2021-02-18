import json
import pandas as pd
import numpy as np
import re
import spacy
import PyPDF2

import Models

from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def define_topic(PATH, file_path: str, is_pdf) -> json:
    '''
    Takes a file path of a pdf and returns json containing the 
    main topic and all the tag words related to the pdf text
    '''
    if is_pdf :
        # extract text
        text = extract_text_from_pdf(file_path)
    else :
        with open(file_path, encoding="utf8") as file:
            text = file.read()

    # retrieve models
    nmf_model = load(f'nmf_model.joblib')
    nmf_model.regularization='both'
    tfidf = load(f'tfidf.joblib')

    # fit the text into the model
    dtm = tfidf.transform([text])
    topics_result = nmf_model.transform(dtm)[0]

    # define the main topic
    # TODO : to be changed once we have labeled the topics
    main_topic_number = topics_result.argmax()
    

    # get the tags of the 4 most dominent topics
    tags = get_tags(nmf_model, tfidf, topics_result)

    # return json file
    jsonStr = json.dumps(Models.ArticleWrapper(file_path, f'Topic {main_topic_number}',tags).__dict__)
    return jsonStr

def get_tags(nmf_model, tfidf, topic_results):
    topics = get_topics(nmf_model, tfidf)
    topics = [topics[i] for i in topic_results.argsort()[-4:]]
    tags_to_return = []
    for topic in topics:
        temp_tags = []
        df = topic.tags
        df = df[~df['Name'].isin(['ai', 'artificial', 'intelligence'])]
        temp_tags.extend(df[df['Weight'] > 2]['Name'])
        if len(temp_tags) < 3:
            temp_tags.extend(df[(df['Weight'] > 1.5) & (df['Weight'] <= 2)]['Name'])
        if len(temp_tags) < 3:
            temp_tags.extend(df[(df['Weight'] > 1) & (df['Weight'] <= 1.5)]['Name'])
        if len(temp_tags) < 3:
            temp_tags.extend(df.iloc[-2:]['Name'])
        temp_tags = list(set(temp_tags))
        tags_to_return.extend(temp_tags)
    return tags_to_return

def get_topics(nmf_model, tfidf):
    topics = nmf_model.components_
    tag_names = tfidf.get_feature_names()
    returned_topics = []
    i = 1
    for topic in topics:
        names = [tag_names[i] for i in topic.argsort()[-15:]]
        weight = [topic[i].round(4) for i in topic.argsort()[-15:]]
        d = {'Name' : names, 'Weight' : weight}
        df = pd.DataFrame.from_dict(d)
        returned_topics.append(Models.Topic(f'Topic {i}', df))
        i += 1

    return returned_topics

def export_topics_to_csv(nmf_model, tfidf):
    topics = get_topics(nmf_model, tfidf)
    tags = [ topic.tags for topic in topics ]
    df = pd.concat(tags, axis = 1)
    df.to_csv('topics.csv', index=True)

    

    ## exporter en csv

def extract_text_from_pdf(file_path):
    
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        txt = ''
        for i in range(0, pdf_reader.getNumPages()):
            txt += pdf_reader.getPage(i).extractText()
    return txt
