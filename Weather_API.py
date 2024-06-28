import request
import os
from dotenv import load_dotenv

load_dotenv()


API_Key = os.getenv("api_key")

#lat = 47.376888
#lon = 8.541694

URL = "https://api.openweathermap.org/data/2.5/forecast?lat=47.376888&lon=8.541694&appid=" + API_Key

response = requests.get(URL)

if response.status_code == 200:
    daten = response.json()

else:
    print ("Es gab leider einen Fehler!")
     return None




