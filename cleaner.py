import os
import math
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from multiprocessing import Pool, cpu_count

#import tensorflow as tf
#from transformers import BertTokenizer
#from transformers import TFBertForSequenceClassification
#from official.nlp import optimization

import ftfy
from bs4 import BeautifulSoup
import nltk
from stopwordsiso import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer

"""# Data preparation
### Steps
* Remove html tags from product attributes
* Remove mispelling 
* Since the descriptive text does not contain negative verbs that could change the semantics, the last step is to remove stopwords
"""

def dropUselessColumns(product_df):
    # Rimuovo le colonne che non mi servono
    product_df.drop(['price'], axis=1, inplace=True)
    return product_df

#Funzione per rimuovere i tag html
def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        data.decompose()

    return ' '.join(soup.stripped_strings)
#Converte una lista in una stringa
def listToString(s):
    str1 = " "
    return (str1.join(s))
#Pulizia del DataSet
def cleanDataset(product_df):
    #Array contenente le stopwords delle lingue del dataset
    product_df= dropUselessColumns(product_df)
    stop_words = stopwords(["ja","en","es","it","de","fr"])
    tokenizer = RegexpTokenizer(r'\w+')
    for index in tqdm(range(0, len(product_df))):
        for col in range(2,7):
            # Eseguo azioni solo sui valori not NaN
            if not (pd.isnull(product_df.iloc[index, col])):
                # Rimuovo i tag html
                if bool(BeautifulSoup(product_df.iloc[index, col], "html.parser").find()):
                    product_df.iloc[index, col] = remove_tags(product_df.iloc[index, col])
                # Rimuovo i mispelling
                product_df.iloc[index, col] = ftfy.fix_text(product_df.iloc[index, col])
                # Rimuovo le stopwords
                word_tokens = tokenizer.tokenize(product_df.iloc[index, col])
                product_df.iloc[index, col] = listToString([w for w in word_tokens if not w.lower() in stop_words])

    return product_df

"""# Load Dataset"""
if __name__ == '__main__':
    train_df = pd.read_csv('datasets/products_train.csv')
    #Utilizziamo l'60% dei processori disponibili
    num_processes = cpu_count()*60//100
    chunk_size = len(train_df)//num_processes

    chunks= pd.read_csv('datasets/products_train.csv', chunksize=chunk_size)
    #Generiamo la pool dei processi
    pool= Pool(processes=num_processes)

    cleaned_chunks = pool.map(cleanDataset, chunks)

    cleaned_df= pd.concat(cleaned_chunks)

    """## Saving cleaning dataset to csv"""

    cleaned_df.to_csv('datasets/products_train_cleaned.csv', index=False)

    cleaned_df.info()

