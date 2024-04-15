import json
import requests
import datetime
import random
import copy

URL = "mongodb://hodor-mongo:27017"

f = open('express_products4.json')
data = json.load(f)

concated_data = data

l = len(concated_data)
print(l)
c = 0
c1 = 0
all_data = []
for _ in range(3):
    for i in range(0,l):
        concated_data[i]["uniqueId"] = str(c1)
        c1+=1
        for j in range(0, len(concated_data[i]["variants"])):
            concated_data[i]["variants"][j]["variantId"] = str(c)
            c+=1
    all_data.extend(copy.deepcopy(concated_data))

print(len(all_data))
print(c1)
print(c)
for x in all_data:
    for y in x["variants"]:
        y["v_storeIds"] = [str(random.randint(1000000, 1000500)) for _ in range(20)]

# with open("express_data.json", "w") as file:
#     json.dump(all_data,file)

stores = {}

variants = []

product_key_map = {}

for x in all_data:
    product_key_map[x["uniqueId"]] = x
    for y in x["variants"]:
        for z in y["v_storeIds"]:
            new_dict = {"s_"+key: value for key, value in y.items() if key in ["v_displayable","v_size", "v_redline", "v_giftCard","v_onSale","v_storeAvailability"]}
            new_dict["variantId"] = y["variantId"]
            new_dict["productId"] = x["uniqueId"]
            #new_dict2 = {"uniqueId":x["uniqueId"],"variants":[new_dict] }
            if z in stores:
                stores[z]["variants"].append(new_dict)
            else:
                stores[z]={"storeId":z,"name":"A2Z store","location":"blr","variants":[new_dict]}

for k,v in stores.items():
    pro = {}
    for x in stores[k]["variants"]:
        if x["productId"] in pro:
            pro[x["productId"]].append(x)
        else:
            pro[x["productId"]] = [x]
    for k1, v1 in pro.items():
        if "products" in stores[k]:
            stores[k]["products"].append({"uniqueId":k1,"s_p_selling_price":product_key_map[k1]["selling_price"],"s_p_availability":product_key_map[k1]["availability"],"s_p_size":product_key_map[k1]["size"],"s_p_color":product_key_map[k1]["color"], "variants":v1})# add "variants":v1 to include variants
        else:
            stores[k]["products"]= [{"uniqueId":k1,"s_p_selling_price":product_key_map[k1]["selling_price"],"s_p_availability":product_key_map[k1]["availability"],"s_p_size":product_key_map[k1]["size"],"s_p_color":product_key_map[k1]["color"], "variants":v1}] # add "variants":v1 to include variants
    del stores[k]["variants"]



products = []
for x in all_data:
    product_dict = {key: value for key, value in x.items() if key in ["uniqueId","description","pattern","size","catlevel2","productImage","imageUrl","newProduct","productInventory","color","colorName"]}
    variants_arr = []
    for y in x["variants"]:
        new_dict = {key: value for key, value in y.items() if key in ["v_color","v_colorCode", "v_currentPrice","v_originalPrice","v_displayMSRP","v_unbxd_color_mapping","variantId"]}
        variants_arr.append(new_dict)
    product_dict["variants"] = variants_arr
    products.append(product_dict)


list_stores = list(stores.values())
print(len(products))
print(len(list_stores))

# with open("products1.json", "w") as file:
#     json.dump(products,file)

# with open("stores1.json", "w") as file:
#     json.dump(list_stores,file)

start = datetime.datetime.now()

print("len store",len(list_stores))
print("len products",len(products))

productsUrl = "http://34.86.235.188/v2/sites/test_store_site/products/_insertbatch"
storeUrl = "http://34.86.235.188/sites/test_store_site/stores/_insertbatch"
headers = {'Content-Type': 'application/json'}

batch_size = 5000
for i in range(0, len(products), batch_size):
    batch = products[i:i + batch_size]
    response = requests.post(productsUrl, json=batch, headers=headers)
    print("Status Code for product insert", response.status_code)

batch_size_store = 50
for i in range(0, len(list_stores), batch_size_store):
    batch = list_stores[i:i + batch_size_store]
    response = requests.post(storeUrl, json=batch, headers=headers)
    print("Status Code for store insert", response.status_code)


# store_payload = json.dumps(list_stores)
# products_payload = json.dumps(products)


# response = requests.post(storeUrl, data=store_payload, headers=headers)
# print("Status Code store insert", response.status_code)
# print("Response Content:", response.text)

# response = requests.post(productsUrl, data=products_payload, headers=headers)
# print("Status Code for product insert", response.status_code)
# print("Response Content:", response.text)

time_clocked = datetime.datetime.now() - start
time_taken = int(time_clocked.total_seconds() * 1000)

print("Insertion time taken", time_clocked)




# uniqueColor = []
# for x in products:
#     for color in x["color"]:
#         if color not in uniqueColor:
#             uniqueColor.append(color)

# print("tot unique color",len(uniqueColor))
# print(uniqueColor)

# with open("product_color.json", "w") as file:
#     json.dump(uniqueColor, file)

# uniqueColorStorePro = []
# for store in list_stores:
#     for pro in store["products"]:
#         for color in pro["s_p_color"]:
#             if color not in uniqueColorStorePro:
#                 uniqueColorStorePro.append(color)


# print("tot unique color",len(uniqueColorStorePro))

# with open("store_product_color.json", "w") as file:
#     json.dump(uniqueColorStorePro, file)
