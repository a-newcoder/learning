import json
a={"我":"name"}
with open("one.json","a",encoding="utf-8") as file:
    json.dump(a,file)
with open("one.json","r",encoding="utf-8") as file:
    b=json.load(file)
    print(b)
