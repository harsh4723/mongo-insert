import json
import requests

URL = "mongodb://hodor-mongo:27017"

f = open('express_products2.json')
data = json.load(f)
print("len of tot data", len(data))
concated_data = data[:500]

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
print(len(concated_data))
print(len(list_stores))


# with open("products.json", "w") as file:
#     json.dump(concated_data,file)

# with open("stores.json", "w") as file:
#     json.dump(list_stores,file)

store_payload = json.dumps(list_stores)
products_payload = json.dumps(concated_data)

productsUrl = "http://localhost:7171/v2/sites/test-unbxd_213213/products/_insertbatch"
storeUrl = "http://localhost:7171/sites/test-unbxd_213213/stores/_insertbatch"
headers = {'Content-Type': 'application/json'}

response = requests.post(storeUrl, data=store_payload, headers=headers)
print("Status Code store insert", response.status_code)
print("Response Content:", response.text)

response = requests.post(productsUrl, data=products_payload, headers=headers)
print("Status Code for product insert", response.status_code)
print("Response Content:", response.text)


