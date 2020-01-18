import spoonacular as sp
api = sp.API("ec9eb3bb895e4078bb61b9e7b9cf05e7")

with open("exampleFridgeContent.txt","r") as f:
    data = f.readlines()

contents = {}

for rawData in data:
    dataExtract = api.parse_ingredients(rawData.strip("\n")).json()[0]
    contents[dataExtract['name']] = [dataExtract['amount'],dataExtract['unitLong']]


print(contents)


ingList = ""
for item in contents:
    print(item)
    ingList += item + ","

ingList = ingList[0:(len(ingList)-2)]

print(ingList)

suggestion = api.search_recipes_by_ingredients(ingredients=ingList,number=1,ranking=1).json()
print(suggestion)




