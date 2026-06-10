import json
from datetime import datetime

with open("tgl_merah.json") as file:
    data_dict = json.load(file)

# select field
selected_fields = [{item["name"], item["date"]} for item in data_dict]
print(selected_fields)
# tgl_merah = [item for item in data_dict]
# print(tgl_merah)
# print(data_dict)
