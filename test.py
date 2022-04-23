

def check(target_dict,key):
    if isinstance(target_dict,dict):
        return target_dict[key] if key in target_dict else "N/A"
    return "N/A"

a = {"Name":"John Cena","age":16,"address":{"state":"Kepong","Jalan":"Desa Aman Puri"}}

a = "N/A"

# print(isinstance(a,dict))

print(check(a,"Name"))
print(check(a["address"],"state"))
print(check(a,"hahaha"))