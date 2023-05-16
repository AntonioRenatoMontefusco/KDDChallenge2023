import pandas as pd
from tqdm.auto import tqdm
from multiprocessing import Pool, cpu_count
import ast
import numpy as np
from functools import partial

def to_map(df):
    df['tmp'] = df['title'] + " " + df['brand'].fillna("")
    return df.set_index(df['id'] + "" + df['locale'])['tmp'].to_dict()

def get_output_dataset(sessions, products):
    outputDataset = pd.DataFrame(columns=["items", "prediction"])
    for index in tqdm(range(0,len(sessions))):
        sessions["prev_items"][index] = sessions["prev_items"][index].replace("[", "").replace("]", "").replace("'", "")
        sessions["prev_items"][index] = sessions["prev_items"][index].split()
        tmp = ""
        for item in sessions["prev_items"][index]:
            product = products.get(item + "" + sessions["locale"][index])
            if isinstance(product,str) or not np.isnan(product):
                tmp += product + "; "
        next_product = products.get(str(sessions["next_item"][index]) + "" + str(sessions["locale"][index]))
        outputDataset = outputDataset.append({"items": tmp, "prediction": next_product}, ignore_index=True)
    return outputDataset

if __name__ == '__main__':
    sessions = pd.read_csv('datasets/da_cancellare.csv')
    products = to_map(pd.read_csv('datasets/products_train_cleaned.csv'))

    num_processes = cpu_count() * 60 // 100
    chunk_size = len(sessions) // num_processes
    chunks = pd.read_csv('datasets/da_cancellare.csv', chunksize=chunk_size)
    pool = Pool(processes=num_processes)

    get_output_dataset_partial = partial(get_output_dataset, products=products)
    out_chunks = pool.map(get_output_dataset_partial, chunks)
    output=pd.concat(out_chunks)
    output.to_csv("datasets/train.csv",index=False)
    print(sessions["prev_items"])

