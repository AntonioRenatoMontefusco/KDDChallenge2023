from multiprocessing import Pool, cpu_count

import demoji
import ftfy
import pandas as pd
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from stopwordsiso import stopwords
from tqdm.auto import tqdm

# import tensorflow as tf
# from transformers import BertTokenizer
# from transformers import TFBertForSequenceClassification
# from official.nlp import optimization


"""# Data preparation
### Steps
* Rimuovere tag html dagli attributi dei prodotti
* Rimuovere mispelling 
* Rimuovere emoji
* Rimuovere stopwords
"""

"""
Funzione per eliminare le emoji
"""
def remove_emojis(data):
    dem = demoji.findall(data)
    for item in dem.keys():
        data = data.replace(item, '')
    return data

"""Eliminiamo la colonna del prezzo"""
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
        for col in range(2,10):
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
                # Rimuovo le emojis
                product_df.iloc[index, col] = remove_emojis(product_df.iloc[index, col])

    return product_df
#Implementazione multiprocesso per velocizzare la pulizia del dataset sfruttando i core della cpu
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

