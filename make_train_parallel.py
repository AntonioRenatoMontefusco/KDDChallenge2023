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
        sessions["prev_items"].iloc[index] = sessions["prev_items"].iloc[index].replace("[", "").replace("]", "").replace("'", "")
        sessions["prev_items"].iloc[index] = sessions["prev_items"].iloc[index].split()
        tmp = ""
        for item in sessions["prev_items"].iloc[index]:
            product = products.get(item + "" + sessions["locale"].iloc[index])
            if isinstance(product, str) or not np.isnan(product):
                tmp += product + "; "
        next_product = products.get(str(sessions["next_item"].iloc[index]) + "" + str(sessions["locale"].iloc[index]))
        new_row = {'items': tmp, 'prediction': next_product}
        outputDataset = pd.concat([outputDataset, pd.DataFrame([new_row])], ignore_index=True)
    return outputDataset

if __name__ == '__main__':
    sessions = pd.read_csv('datasets/sessions_train.csv')
    products = to_map(pd.read_csv('datasets/products_train_cleaned.csv'))

    #Single Thread execution
    #output=get_output_dataset(sessions,products)


    # Multi Thread execution
    num_processes = cpu_count() * 60 // 100
    chunk_size = len(sessions) // num_processes
    chunks = pd.read_csv('datasets/sessions_train.csv', chunksize=chunk_size)
    pool = Pool(processes=num_processes)

    get_output_dataset_partial = partial(get_output_dataset, products=products)

    out_chunks = pool.map(get_output_dataset_partial, chunks)
    output = pd.concat(out_chunks)



    #Print Output and make CSV file
    output.to_csv("datasets/train.csv", index=False)
    print(sessions["prev_items"])

