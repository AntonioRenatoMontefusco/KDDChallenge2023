import matplotlib.pyplot as plt
import pandas as pd




product_df = pd.read_csv('datasets/products_train.csv')
sessions_df = pd.read_csv('datasets/sessions_test_task3.csv')

# for index, s in sessions_df.iterrows():
#     sessions_df["prev_items"][index] = sessions_df["prev_items"][index].replace("[", "").replace("]", "").replace("'", "")
#     sessions_df["prev_items"][index] = sessions_df["prev_items"][index].split()
#     sessions_df["prev_items"][index] = len(sessions_df["prev_items"][index])
#
# print(sessions_df)
#
# plt.hist(sessions_df["prev_items"])
# plt.xlabel("length")
# plt.ylabel("count")
# plt.title("Length of sessions")
# plt.show()
#



for index, s in product_df.iterrows():
    product_df["title"][index] = len(str(product_df["title"][index]).strip())
print(product_df)

plt.hist(product_df["title"])
plt.xlabel("length")
plt.ylabel("count")
plt.title("Length of titles")
plt.show()



for index, s in product_df.iterrows():
    product_df["brand"][index] = len(str(product_df["brand"][index]).strip())


print(product_df)

plt.hist(product_df["brand"])
plt.xlabel("length")
plt.ylabel("count")
plt.title("Length of brands")
plt.show()
