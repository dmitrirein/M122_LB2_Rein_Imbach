import requests

#API_Key = "6cba7b191454e2da0f71bd1a674b32db"

#lat = 47.376888
#lon = 8.541694

URL = "https://api.openweathermap.org/data/2.5/forecast?lat=47.376888&lon=8.541694&appid=6cba7b191454e2da0f71bd1a674b32db"

response = requests.get(URL)

if response.status_code == 200:
    daten = response.json()

else:
    print ("Es gab leider einen Fehler!")


