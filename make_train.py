import pandas as pd


if __name__ == '__main__':

    sessions = pd.read_csv('datasets/sessions_train.csv')
    products = pd.read_csv('datasets/products_train_cleaned.csv')
    outputDataset=pd.DataFrame(columns=["items","prediction"])
    #   Remove [,],'
    for index, s in sessions.iterrows():
        sessions["prev_items"][index] = sessions["prev_items"][index].replace("[", "").replace("]", "").replace("'", "")
        sessions["prev_items"][index] = sessions["prev_items"][index].split()

        tmp=""

        for item in sessions["prev_items"][index] :
            ob = products[(products["id"] == item) & (products["locale"] == sessions["locale"][index])]
            tmp += (ob["title"]+" "+ob["brand"]).astype(str).str.cat(sep=' ')+"; "

        next_product=products[(products["id"]==sessions["next_item"][index])&(products["locale"]==sessions["locale"][index])]
        next_tmp=(next_product["title"]+" "+next_product["brand"]).astype(str).str.cat(sep=' ')+"; "
        outputDataset=outputDataset.append({"items":tmp,"prediction":next_tmp},ignore_index=True)
    outputDataset.to_csv("datasets/train.csv",index=False)
    print(sessions["prev_items"])

