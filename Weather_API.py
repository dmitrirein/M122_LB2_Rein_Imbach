import requests

#API_Key = "6cba7b191454e2da0f71bd1a674b32db"

#lat = 47.376888
#lon = 8.541694

URL = "https://api.openweathermap.org/data/2.5/forecast?lat=47.376888&lon=8.541694&appid=6cba7b191454e2da0f71bd1a674b32db"

response = requests.get(URL)

if response.status_code == 200:
    wetter_daten = response.json()
else:
    print ("Es gab leider einen Fehler!")


temperaturen = [round(wetter_daten["list"][i]["main"]["temp_max"]-273.15, 1) for i in [0, 8, 16, 24, 32, 39]]

daten = [i["dt_txt"].split(" ")[0] for i in wetter_daten["list"]]

daten = list(set(daten))

daten.sort()

# beinhaltet daten und die zugehorige maximale temperatur
max_temp_pro_tag = {}

for datum in daten:
    # alle temeraturen vom tag
    tag_temperaturen = []

    # geht durh jeder element im wetter_daten und addiert alle temperaturen die zum tag gehoren
    for element in wetter_daten["list"]:
        if element["dt_txt"].split(" ")[0] == datum:
            temperatur = round(element["main"]["temp_max"]-273.15, 1)
            tag_temperaturen.append(temperatur)

    # maximaler wert in tag_temperaturen
    max_temp = max(tag_temperaturen)

    max_temp_pro_tag.update({datum:max_temp})


print(max_temp_pro_tag)

# for datum in
    