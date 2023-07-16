import pandas as pd







def toLineJson(str):
    json=pd.read_json(str)
    json.to_json(r'output/train.jl',orient='records',lines=True)


def toJson(str):
    dataframe=pd.read_csv(str)
    dataframe['instruction']="From the user session in input, made by items separated by semi-colon get in output the next item that user could search."
    dataframe.rename(columns={'items':'input','prediction':'output'},inplace=True)
    dataframe.to_json(r'output/test_da_cancellare.json',orient='records')


if __name__=="__main__":
    toJson("datasets/test_da_cancellare.csv")
