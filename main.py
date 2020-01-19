import requests
import json
import time
import os
import spoonacular as sp
import webbrowser

# -----------------------------------------------------------------------------------------------------
#Ingredients indicator and recipe finder

api = sp.API("32705ed053d745d3b9cfe60f248d1ee4")

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
    enter=input(' ')

    #Write down the missing ingridients to the shopping list
    convertMissingToTXT(missingIngInfoList)
    


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

# -----------------------------------------------------------------------------------------------------
# Main Program

user_command = "nothing"
promptRecipe()

while (user_command != 5):

    os.system('cls')      

    
    print('-------------------------------------------')
    print('Please choose a purchasing option to top up your food at home:')
    print("1: Online Store\n2: Market")

    user_command = int(input('Enter choice here: '))

    if (user_command==1):
        url = r'C:\Users\Asus\Desktop\HackCambridge20\Amazon_test.html'
        webbrowser.open(url, new=2)  # open in new tab
    
    elif (user_command==2):
        #Supermarket/market loctor using Google Maps API
        class GooglePlaces(object):
            def __init__(self, apiKey):
                super(GooglePlaces, self).__init__()
                self.apiKey = apiKey

            def search_places_by_coordinate(self, location, radius, types):
                endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                places = []
                params = {
                    'location': location,
                    'radius': radius,
                    'types': types,
                    'key': self.apiKey
                }
                res = requests.get(endpoint_url, params = params)
                results =  json.loads(res.content)
                places.extend(results['results'])
                time.sleep(2)
                while "next_page_token" in results:
                    params['pagetoken'] = results['next_page_token'],
                    res = requests.get(endpoint_url, params = params)
                    results = json.loads(res.content)
                    places.extend(results['results'])
                    time.sleep(2)
                print (places)
                return places

            def get_place_details(self, place_id, fields):
                endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
                params = {
                    'placeid': place_id,
                    'fields': ",".join(fields),
                    'key': self.apiKey
                }
                res = requests.get(endpoint_url, params = params)
                place_details =  json.loads(res.content)
                return place_details

        if __name__ == '__main__':
            api = GooglePlaces('AIzaSyB6VQWBlXGKUQo4LS4OIjg3GoMUHClD218')
            places = api.search_places_by_coordinate("52.204450, 0.119000", "400", "supermarket")
            output = ['name', 'formatted_address', 'international_phone_number', 'website', 'rating', 'review']
            f = open('trial.txt', 'w+')
            for place in places:
                details = api.get_place_details(place['place_id'], output)
                # try:
                #     website = details['result']['website']
                # except KeyError:
                #     website = ""

                try:
                    name = details['result']['name']
                    print(name)
                except KeyError:
                    name = ""

                try:
                    address = details['result']['formatted_address']
                    print(address)
                except KeyError:
                    address = ""
                    
                f.write(name)
                f.write('\n')
                f.write(address)
                
            f.close()
            enter=input(" ")
print('Exiting application')

        
