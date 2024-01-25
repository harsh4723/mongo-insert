import json
import requests
import datetime

URL = "mongodb://hodor-mongo:27017"

f = open('express_products3.json')
data = json.load(f)

concated_data = data["feed"]["catalog"]["add"]["items"][4000:]
# concated_data = data
# with open("express_products4.json", "w") as file:
#     json.dump(concated_data,file)

stores = {}

variants = []

product_key_map = {}

for x in concated_data:
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
    # for k,v in stores.items():
    #     vari = stores[k]["variants"]
    #     if "products" in stores[k]:
    #       stores[k]["products"].append({"uniqueId":x["uniqueId"],"variants":vari })
    #     else:
    #         stores[k]["products"] = [{"uniqueId":x["uniqueId"],"variants":vari }]

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
for x in concated_data:
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


# with open("products.json", "w") as file:
#     json.dump(products,file)

# with open("stores.json", "w") as file:
#     json.dump(list_stores,file)

store_payload = json.dumps(list_stores)
products_payload = json.dumps(products)

productsUrl = "http://localhost:5001/v3/products/insertbatch"
storeUrl = "http://localhost:5001/v3/stores/insertbatch"
headers = {'Content-Type': 'application/json'}

start = datetime.datetime.now()

response = requests.post(storeUrl, data=store_payload, headers=headers)
print("Status Code store insert", response.status_code)
print("Response Content:", response.text)

response = requests.post(productsUrl, data=products_payload, headers=headers)
print("Status Code for product insert", response.status_code)
print("Response Content:", response.text)

time_clocked = datetime.datetime.now() - start
time_taken = int(time_clocked.total_seconds() * 1000)

print("Insertion time taken", time_clocked)
