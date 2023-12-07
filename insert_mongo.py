import json
import pymongo

URL = "mongodb://hodor-mongo:27017"

f = open('express_products2.json')
data = json.load(f)
concated_data = data[:1000]

stores = {}

variants = []

products = []
for x in concated_data:
    product_dict = {key: value for key, value in x.items() if key != "variants"}
    products.append(product_dict)
    for y in x["variants"]:
        y["productId"] = x["uniqueId"]
        variants.append(y)
        for z in y["v_storeIds"]:
            new_dict = {key: value for key, value in y.items() if key != "v_storeIds"}

            if z in stores:
                stores[z]["variants"].append(new_dict)
            else:
                stores[z]={"storeId":z,"variants":[new_dict]}

list_stores = list(stores.values())
print(len(variants))


# with open("onsefeed2.json", "w") as file:
#     json.dump(list_stores,file)


def insert_to_collection(collection, data_array):
    result = collection.insert_many(data_array)
    print("Inserted document IDs:", result.inserted_ids)


client = pymongo.MongoClient(URL)

db = client["products"]

collection = db["s_h-test"]
insert_to_collection(collection,stores)

collection = db["h-test"]
insert_to_collection(collection,products)

collection = db["v_h-test"]
insert_to_collection(collection,variants)


