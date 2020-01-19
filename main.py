import dataParser
from dataParser import promptRecipe
import google_maps_access
from google_maps_access import GooglePlaces
import os

user_command = "nothing"

while (user_command != 5):

    #os.system('cls')                                                                                

    #promptRecipe()

    print('-------------------------------------------')
    print('Please choose a purchasing option to top up your food at home:')
    print("1: Online Store\n2: Market")

    user_command = int(input('Enter choice here: '))

    if (user_command==1):
        print(1)
    
    elif (user_command==2):
        api = GooglePlaces('AIzaSyB6VQWBlXGKUQo4LS4OIjg3GoMUHClD218')

        places = api.search_places_by_coordinate("52.204450, 0.119000", "400", "supermarket")
        print(places)

print('Exiting application')

        

