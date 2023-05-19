import pandas as pd

if __name__ == '__main__':
    dataset = pd.read_csv('datasets/train.csv')
    dataset_length = len(dataset)

    # Calcola l'indice a cui dividere il dataset a metà
    split_index = dataset_length // 2

    # Suddividi il dataset a metà
    dataset_1 = dataset.iloc[:split_index]
    dataset_2 = dataset.iloc[split_index:]
    dataset_1.to_csv("output/train.csv", index=False)
    dataset_2.to_csv("output/val.csv", index=False)

