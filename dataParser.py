import spoonacular as sp
api = sp.API("ec9eb3bb895e4078bb61b9e7b9cf05e7")

unwantedUnits = ['large', 'larges', 'serving', 'servings','smalls','small']


def loadFridgeContent():
    with open("exampleFridgeContent.txt","r") as f:
        data = f.readlines()

    contents = {}

    for rawData in data:
        spl = rawData.split("$")
        contName = spl[0]
        contAmount = spl[1]
        contUnit = spl[2]
        contents[contName] = [contAmount,contUnit]
    return contents


def generateRecipes(contents):
    ingList = ""
    for item in contents:
        ingList += item + ","
    ingList = ingList[0:(len(ingList)-2)]
    recipesJsonList = api.search_recipes_by_ingredients(ingredients=ingList,number=5,ranking=1).json()

    recipes = []


    for recipeJson in recipesJsonList:
        id = recipeJson['id']
        name = recipeJson['title']
        usedIngrJsonList = recipeJson['usedIngredients']
        missedIngrJsonList = recipeJson['missedIngredients']
        recipeLink = api.get_recipe_information(id).json()['sourceUrl']


        ingInfoList = []
        for ingrd in usedIngrJsonList:
            ingrdUnit = ingrd['unitLong']
            ingrdName = ingrd['name']
            ingrdAmount = ingrd['amount']
            ingInfoList.append({'name':ingrdName,'amount':ingrdAmount,'unitLong':ingrdUnit})

        missedIngInfoList = []
        for ingrd in missedIngrJsonList:
            ingrdUnit = ingrd['unitLong']
            ingrdName = ingrd['name']
            ingrdAmount = ingrd['amount']
            missedIngInfoList.append({'name': ingrdName, 'amount': ingrdAmount, 'unitLong': ingrdUnit})

        recipes.append({'name': name, 'link': recipeLink,'ingList':ingInfoList,'uingList':missedIngInfoList})
    return recipes


def promptRecipe():
    contents = loadFridgeContent()
    recipes = generateRecipes(contents)
    print("Recommended recipes:")
    for i in range(len(recipes)):
        print((str(i+1)+"."),recipes[i]['name'],"-",recipes[i]['link'])

    choose = int(input("Enter choice (Enter number between 1-5): "))
    missingIngInfoList = recipes[choose-1]['uingList']
    print(recipes[choose-1]['name'],"-",recipes[choose-1]['link'])

    #Write down the missing ingridients to the shopping list
    convertMissingToTXT(missingIngInfoList)
    localOrOnline = int(input("Online or local?"))



#TODO: Finish this so fridge emptied
def takeOutFromFridge(ingList):
    with open("exampleFridgeContent.txt", "r") as f:
        data = f.readlines()
    splitted = map((lambda x : x.split("$")), data)

    names = [splitted[i][0] for i in range(len(data))]

    for ing in ingList:
        ingN = ing['name']
        ingAmt = ing['amount']
        intUnt = ing['unitLong']
        if ingN in names:
            pass

    f = open("exampleFridgeContent.txt","w")
    f.close()


def convertMissingToTXT(missingIngInfoList):
    f = open("shoppingListNew.txt","a")
    for ing in missingIngInfoList:
        f.write('\n'+ing['name']+'$'+str(ing['amount'])+'$'+removeBadUnit(ing['unitLong']))
    f.close()


def removeBadUnit(unit):
    if unit in unwantedUnits:
        return ""
    else:
        return unit






promptRecipe()
