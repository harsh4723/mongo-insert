import json
f = open('express_products2.json')

data = json.load(f)

#print(len(data["feed"]["catalog"]["add"]["items"]))

#print(data["feed"]["catalog"]["add"]["items"][2])

# with open("express_products2.json", "w") as file:
#     json.dump(data["feed"]["catalog"]["add"]["items"][:2000], file)


concated_data = data[:1000]

stores = {}

for x in concated_data:
    for y in x["variants"]:
        for z in y["v_storeIds"]:
            new_dict = {key: value for key, value in y.items() if key != "v_storeIds"}

            if z in stores:
                stores[z]["variants"].append(new_dict)
            else:
                stores[z]={"storeId":z,"variants":[new_dict]}

print(len(list(stores.values())))
with open("onsefeed2.json", "w") as file:
    json.dump(list(stores.values()),file)