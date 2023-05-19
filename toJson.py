import pandas as pd

if __name__ == '__main__':
    dataframe=pd.read_csv("datasets/train.csv")
    dataframe['instruction']="From the user session in input, made by items separated by semi-colon get in output the next item that user could search."
    dataframe.rename(columns={'items':'input','prediction':'output'},inplace=True)
    dataframe.to_json(r'output/train.json',orient='records')
